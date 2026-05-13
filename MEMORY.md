# MEMORY.md - MCP Designer Project Decisions & Context

**Project:** MCP Designer  
**Owner:** Anu L Sasidharan (OrionVexa)  
**Last Updated:** May 13, 2026

---

## Document Purpose

This file serves as the project's institutional memory, capturing:
- **Key technical decisions** and their rationale
- **Architecture choices** and trade-offs
- **Lessons learned** from development
- **Context** for future developers (including future you)
- **Abandoned approaches** and why they didn't work

Update this file whenever making significant decisions or learning important lessons.

---

## Project Genesis

### Why This Project Was Created

**Date:** May 13, 2026  
**Context:** After building ArchDLoom (AI system design generator) and multiple AI-powered applications, identified a gap in the MCP ecosystem.

**Market Observation:**
- MCP protocol adoption growing rapidly with Claude and other LLMs
- No visual tooling exists for MCP server development
- Developers manually writing boilerplate for every server
- High barrier to entry for non-expert developers

**Personal Motivation:**
- Leverage RAG Designer experience in building dev tools
- Portfolio piece demonstrating AI/ML platform engineering skills
- Strong talking point for AI engineering job interviews
- Potential commercial product opportunity

**Alternative Considered:**
- Contributing to existing MCP tools → No visual designers exist
- Building CLI generator only → Less differentiation, lower market impact
- Focusing solely on templates → Doesn't solve the full workflow problem

**Decision:** Build full visual designer with code generation, testing, and deployment.

---

## Major Architectural Decisions

### AD-001: Monorepo vs Separate Repositories

**Date:** May 13, 2026  
**Decision:** Use separate repositories for frontend and backend  
**Status:** ✅ Decided

**Context:**
- Need to deploy frontend (Next.js) and backend (FastAPI) independently
- Different deployment targets (Vercel vs Cloud Run)
- Separate CI/CD pipelines

**Options Considered:**

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Monorepo (Turborepo/Nx) | Single source, shared types, easier local dev | Complex CI/CD, all-or-nothing deploys | ❌ Rejected |
| Separate repos | Independent deploys, simpler CI/CD | Type sharing harder, more repos to manage | ✅ Selected |
| Monorepo with independent deploys | Best of both | Complex tooling, overkill for 2 projects | ❌ Rejected |

**Rationale:**
- Frontend and backend have different lifecycles
- Simpler deployment story (Next.js → Vercel, FastAPI → Cloud Run)
- Can share types via npm package if needed later
- Easier to open-source backend separately

**Implementation:**
```
github.com/orionvexa/mcp-designer-frontend  (Next.js)
github.com/orionvexa/mcp-designer-backend   (FastAPI)
github.com/orionvexa/mcp-designer-templates (Shared templates)
```

**Review Date:** After MVP completion

---

### AD-002: Code Generation Approach

**Date:** May 13, 2026  
**Decision:** Use Jinja2 template-based generation (not AST manipulation)  
**Status:** ✅ Decided

**Context:**
- Need to generate TypeScript and Python MCP servers
- Code must be readable, maintainable, and production-ready
- Users should be able to customize generated code

**Options Considered:**

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Jinja2 Templates | Simple, maintainable, easy to customize | String manipulation risks | ✅ Selected |
| AST Manipulation (ts-morph, ast) | Guaranteed valid code, precise control | Complex, hard to maintain | ❌ Rejected |
| AI Generation (GPT-4) | Most flexible | Unpredictable, costs, latency | ❌ Rejected |
| Hybrid (Templates + AST) | Best of both | Increased complexity | 🔄 Future consideration |

**Rationale:**
- Templates are easier to understand and modify
- Can validate generated code with linters before saving
- Fast generation (no API calls, no complex AST walking)
- Users can customize templates directly
- Similar approach used successfully by FastAPI, Django, Rails

**Mitigation for String Manipulation Risks:**
- Comprehensive test suite for all templates
- Linting validation on generated code (eslint, black)
- User can preview before accepting
- Template versioning for backwards compatibility

**Code Example:**
```python
# backend/core/codegen/templates/typescript/tool.ts.j2
export async function {{ tool_name }}(args: {{ tool_name }}Args): Promise<ToolResult> {
  try {
    // Input validation
    const validated = {{ tool_name }}ArgsSchema.parse(args);
    
    {{ handler_code | indent(4) }}
    
    return { success: true, data: result };
  } catch (error) {
    return { success: false, error: error.message };
  }
}
```

**Review Date:** After generating 100+ servers successfully

---

### AD-003: Frontend State Management

**Date:** May 13, 2026  
**Decision:** Use Zustand for local state, React Query for server state  
**Status:** ✅ Decided

**Context:**
- Complex UI state (designer, editor, testing console)
- Need to sync with backend (projects, tools, templates)
- Performance critical (large flow diagrams)

**Options Considered:**

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Redux Toolkit | Industry standard, dev tools | Boilerplate, overkill for this | ❌ Rejected |
| Zustand | Simple, small, performant | Less ecosystem | ✅ Selected (local) |
| React Context | Built-in, simple | Performance issues at scale | ❌ Rejected |
| React Query | Perfect for server state | Not for local state | ✅ Selected (server) |
| tRPC + Zustand | Type-safe, best of both | Learning curve | 🔄 Consider for v2 |

**Rationale:**
- **Zustand for local UI state:**
  - Designer node positions
  - Editor selections
  - UI panel visibility
  - Form state before submission

- **React Query for server state:**
  - Projects, tools, templates from API
  - Automatic caching and revalidation
  - Optimistic updates for better UX
  - Background refetching

**Implementation Pattern:**
```typescript
// Local state (Zustand)
const useDesignerStore = create<DesignerState>((set) => ({
  nodes: [],
  edges: [],
  selectedNode: null,
  addNode: (node) => set((state) => ({ nodes: [...state.nodes, node] })),
}));

// Server state (React Query)
const { data: projects } = useQuery({
  queryKey: ['projects'],
  queryFn: fetchProjects,
});
```

**Review Date:** After MVP, evaluate if tRPC adds enough value

---

### AD-004: Testing Strategy

**Date:** May 13, 2026  
**Decision:** Docker sandbox for MCP server execution  
**Status:** ✅ Decided

**Context:**
- Need to safely execute user-generated MCP server code
- Must support both TypeScript and Python
- Security is critical (code injection, resource abuse)

**Options Considered:**

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Docker Containers | Strong isolation, standard | Overhead, complexity | ✅ Selected |
| VM-based (Firecracker) | Stronger isolation | Overkill, more complex | ❌ Rejected |
| Process Sandboxing (chroot) | Lighter weight | Weaker isolation | ❌ Rejected |
| Cloud Functions (ephemeral) | No local infrastructure | Latency, costs | 🔄 Future option |

**Rationale:**
- **Security:** Container isolation prevents file system access, network abuse
- **Resource Limits:** CPU, memory, time limits easily configured
- **Standard:** Docker is universal, well-understood
- **Testing:** Easy to test sandbox itself
- **Consistency:** Same environment as production deployments

**Implementation:**
```python
# backend/core/sandbox/docker_runner.py
class MCPServerSandbox:
    def __init__(self, server_code: str, runtime: str):
        self.image = f"mcp-sandbox-{runtime}"  # typescript or python
        self.limits = {
            'cpus': 0.5,
            'memory': '512m',
            'network': 'none',  # No external network access
            'timeout': 30,  # seconds
        }
    
    async def execute_tool(self, tool_name: str, args: dict) -> dict:
        # Create ephemeral container
        # Execute tool
        # Capture output
        # Destroy container
        pass
```

**Security Layers:**
1. No network access (except to Claude API via proxy)
2. Read-only filesystem (except temp directory)
3. Resource limits (CPU, memory, time)
4. Non-root user inside container
5. Seccomp profile to restrict syscalls

**Review Date:** After security audit

---

### AD-005: Database Choice

**Date:** May 13, 2026  
**Decision:** PostgreSQL for primary database  
**Status:** ✅ Decided

**Context:**
- Need relational data (projects, tools, users)
- JSONB support for flexible schemas (tool configs)
- Full-text search for templates
- GCP Cloud SQL integration

**Options Considered:**

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| PostgreSQL | JSONB, full-text search, mature | Vertical scaling limits | ✅ Selected |
| MongoDB | Flexible schema, horizontal scaling | No transactions, complex queries | ❌ Rejected |
| MySQL | Popular, good support | Weaker JSON support | ❌ Rejected |
| SQLite | Simple, embedded | Not for production | ❌ For local dev only |

**Rationale:**
- JSONB for tool configurations (variable schemas)
- Full-text search for template discovery
- GCP Cloud SQL has great PostgreSQL support
- Mature ecosystem, excellent with SQLAlchemy
- ACID transactions for data integrity

**Schema Design Principles:**
- Relational for structured data (users, projects)
- JSONB for flexible/nested data (tool configs, schemas)
- Indexes on commonly queried fields
- Foreign keys with CASCADE deletes
- Timestamps on all tables (created_at, updated_at)

**Review Date:** When scaling issues appear (unlikely in MVP)

---

### AD-006: Authentication Strategy

**Date:** May 13, 2026  
**Decision:** JWT-based auth with httpOnly cookies  
**Status:** ✅ Decided

**Context:**
- Need secure authentication for web and API
- Support for future mobile app
- Session management for testing console

**Options Considered:**

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| JWT in httpOnly cookies | Secure, stateless | Can't revoke easily | ✅ Selected |
| Session cookies + DB | Can revoke, simple | Stateful, scaling issues | ❌ Rejected |
| OAuth2 only | Standard, no password management | Complex, dependency on providers | 🔄 Add later |
| API keys only | Simple for API | Not suitable for web | 🔄 Add for deployments |

**Rationale:**
- **httpOnly cookies:** XSS protection
- **JWT:** Stateless, works with Cloud Run autoscaling
- **Refresh tokens:** Can implement revocation if needed
- **Simple for MVP:** Email/password, add OAuth2 later

**Implementation:**
```python
# Access token: 15 minutes, stored in httpOnly cookie
# Refresh token: 7 days, stored in httpOnly cookie
# Token payload: { user_id, email, tier }

@app.post("/api/auth/login")
async def login(credentials: LoginRequest, response: Response):
    user = authenticate(credentials)
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # HTTPS only
        samesite="lax"
    )
    return {"user": user}
```

**Security Considerations:**
- HTTPS only in production
- Token rotation on refresh
- Blacklist for logged-out tokens (Redis)
- Rate limiting on auth endpoints

**Review Date:** When adding team features

---

## Design Patterns & Conventions

### DP-001: API Response Format

**Decision:** Standardized JSON response envelope

**Format:**
```typescript
// Success
{
  "success": true,
  "data": { ... },
  "meta": {
    "timestamp": "2026-05-13T12:00:00Z",
    "requestId": "uuid"
  }
}

// Error
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "User-friendly message",
    "details": { ... }
  },
  "meta": { ... }
}
```

**Rationale:**
- Consistent error handling on frontend
- Easy to add metadata (pagination, timing)
- Type-safe with TypeScript

---

### DP-002: Component Organization

**Decision:** Feature-based folder structure

**Structure:**
```
frontend/components/
├── designer/          # Designer-specific components
│   ├── ToolNode.tsx
│   ├── ResourceNode.tsx
│   └── ConnectionLine.tsx
├── editor/           # Code editor components
│   ├── MonacoEditor.tsx
│   └── ValidationPanel.tsx
├── testing/          # Testing console components
│   ├── TestRunner.tsx
│   └── LogViewer.tsx
└── ui/               # Shared UI components (shadcn)
    ├── button.tsx
    └── dialog.tsx
```

**Rationale:**
- Easy to find related components
- Clear feature boundaries
- Shared UI components separate

---

### DP-003: Error Handling Pattern

**Decision:** Comprehensive error handling at boundaries

**Backend:**
```python
from fastapi import HTTPException

@app.post("/api/projects")
async def create_project(data: ProjectCreate):
    try:
        project = await db.create_project(data)
        return {"success": True, "data": project}
    except ValidationError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create project: {e}")
        raise HTTPException(500, detail="Internal server error")
```

**Frontend:**
```typescript
const { mutate: createProject } = useMutation({
  mutationFn: api.projects.create,
  onError: (error) => {
    toast.error(error.message);
    logger.error('Project creation failed', error);
  },
  onSuccess: (data) => {
    toast.success('Project created');
    queryClient.invalidateQueries(['projects']);
  },
});
```

---

## Technology Choices

### TC-001: Why Next.js 14 (App Router)?

**Pros:**
- Server components for better performance
- Built-in API routes (if needed)
- Great DX with Fast Refresh
- TypeScript first-class support
- Easy deployment to Vercel

**Cons:**
- App Router still evolving
- Some libraries not compatible yet

**Decision:** Use it. App Router is the future of Next.js, and we want modern patterns.

---

### TC-002: Why FastAPI over Node.js?

**Pros:**
- Python for code generation (Jinja2 native)
- Async support (same as Node.js)
- Pydantic validation (better than Zod)
- Familiar to you (Python background)

**Cons:**
- Cold start on Cloud Run (mitigated with min instances)
- Not as many MCP examples in Python

**Decision:** FastAPI. Jinja2 + Python for code gen is simpler than TypeScript templating.

---

### TC-003: Why React Flow over Custom Canvas?

**Pros:**
- Production-ready, battle-tested
- Built-in features (zoom, pan, minimap)
- Good performance
- Active community

**Cons:**
- Learning curve
- Opinionated patterns

**Decision:** Use React Flow. Don't reinvent the wheel for node-based UI.

---

## Abandoned Approaches

### AB-001: AI-Generated Code (GPT-4)

**Date:** May 13, 2026  
**Why Considered:** Most flexible code generation

**Why Abandoned:**
- **Unpredictable output:** Hard to guarantee quality
- **Cost:** Every generation costs money
- **Latency:** Slower than templates
- **Dependency:** Requires external API
- **Debugging:** Hard to debug AI-generated issues

**Lesson:** AI is great for creative tasks, but templates are better for deterministic code generation.

**Future Consideration:** Use AI for natural language → tool definition, but not final code generation.

---

### AB-002: GraphQL API

**Date:** May 13, 2026  
**Why Considered:** Flexible querying, type-safe

**Why Abandoned:**
- **Overkill for MVP:** REST is simpler
- **Caching complexity:** REST + React Query is easier
- **Tooling:** Less familiar than REST
- **tRPC alternative:** If type safety needed, tRPC is simpler

**Lesson:** GraphQL is powerful but adds complexity. REST is sufficient for MVP.

**Future Consideration:** Evaluate tRPC in v2 for end-to-end type safety.

---

### AB-003: WebAssembly for Code Execution

**Date:** May 13, 2026  
**Why Considered:** Client-side code execution, no sandbox needed

**Why Abandoned:**
- **Limited language support:** Good for Rust/C++, poor for Python/TS
- **Security risks:** Still need sandboxing in browser
- **Complexity:** Harder to implement than Docker
- **Claude API access:** Can't call from browser (CORS, API keys)

**Lesson:** WASM is promising but not ready for this use case. Docker is proven.

---

## Key Learnings

### KL-001: MCP Protocol Insights

**Date:** May 13, 2026  
**Context:** Deep dive into MCP specification

**Key Insights:**
1. **Transport matters:** stdio for CLI, SSE for web clients
2. **JSON Schema is critical:** Claude needs correct schema for tool discovery
3. **Error handling is part of protocol:** Use structured errors
4. **Resources are underutilized:** Most servers only implement tools

**Impact on Design:**
- MVP focuses on tools (most common use case)
- Resources and prompts added in v2
- Schema validation is non-negotiable
- Transport selection affects deployment options

---

### KL-002: Code Generation Complexity

**Date:** May 13, 2026  
**Context:** Initial template design

**Key Insights:**
1. **Imports are tricky:** Need to track all dependencies
2. **Formatting matters:** Use prettier/black on generated code
3. **Testing is critical:** Can't ship templates without extensive tests
4. **Documentation generation:** README and inline docs are must-haves

**Impact on Design:**
- Import tracker in code generator
- Post-generation formatting step
- Template test coverage > 90%
- Auto-generated README with examples

---

### KL-003: Visual Designer UX

**Date:** May 13, 2026  
**Context:** Studying other visual tools (Retool, Zapier, n8n)

**Key Insights:**
1. **Simplicity wins:** Too many options overwhelm users
2. **Smart defaults:** Pre-fill common values
3. **Progressive disclosure:** Hide advanced options initially
4. **Real-time feedback:** Validate as user types
5. **Undo/redo is critical:** Users experiment, need to backtrack

**Impact on Design:**
- Minimal UI with "advanced" toggles
- Templates provide smart defaults
- Validation on blur/change
- Command history for undo/redo

---

## Performance Optimizations

### PO-001: React Flow Performance

**Problem:** Slow rendering with 20+ nodes  
**Solution:** Memoization and virtual scrolling

**Implementation:**
```typescript
// Memoize node components
const ToolNode = memo(({ data }) => {
  // Component logic
}, (prev, next) => prev.data.id === next.data.id);

// Virtual scrolling for node list
import { VirtualList } from 'react-window';
```

---

### PO-002: Code Generation Caching

**Problem:** Regenerating code on every small change  
**Solution:** Cache generated code by config hash

**Implementation:**
```python
import hashlib
import json

def generate_code(config: dict) -> str:
    config_hash = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()
    
    # Check cache
    cached = redis_client.get(f"codegen:{config_hash}")
    if cached:
        return cached
    
    # Generate
    code = template.render(config)
    
    # Cache for 1 hour
    redis_client.setex(f"codegen:{config_hash}", 3600, code)
    return code
```

---

## Security Decisions

### SD-001: User Code Execution

**Threat:** Malicious code in tool handlers

**Mitigations:**
1. Docker sandbox with no network access
2. Resource limits (CPU, memory, time)
3. Read-only filesystem (except /tmp)
4. Static analysis on generated code (optional warning)
5. User acknowledges risk before testing

**Implementation:** See AD-004

---

### SD-002: API Key Storage

**Threat:** User API keys in generated code

**Decision:** Never store API keys in database

**Implementation:**
- User provides API keys during deployment
- Stored in GCP Secret Manager (for Cloud Run deployments)
- Env variables for local development
- Never in generated code or database

---

## Future Considerations

### FC-001: Real-Time Collaboration

**Idea:** Multiple users editing same project simultaneously

**Challenges:**
- Conflict resolution (CRDTs or OT)
- WebSocket infrastructure
- Performance at scale

**Decision:** Post-MVP. Nice-to-have, not critical for v1.

---

### FC-002: Template Marketplace

**Idea:** Community-contributed templates

**Requirements:**
- Template validation and security review
- Rating and review system
- Monetization for creators
- Quality standards

**Decision:** v2 feature. Need user base first.

---

### FC-003: AI-Assisted Design

**Idea:** Natural language → tool definition

**Example:** "Create a tool to search GitHub repositories"  
**Output:** Pre-filled tool builder with reasonable defaults

**Challenges:**
- Prompt engineering for consistent output
- Cost per generation
- User expectations vs reality

**Decision:** Experiment post-MVP. Could be killer feature.

---

## Open Questions

### OQ-001: Pricing Model

**Question:** Should we charge per project, per user, or per generation?

**Options:**
- Per user (SaaS standard)
- Per project (limits growth)
- Per generation (usage-based)
- Freemium (free tier + paid)

**Current Thinking:** Freemium with per-user pricing. Need market validation.

---

### OQ-002: Self-Hosted vs Cloud-Only

**Question:** Offer self-hosted version for enterprises?

**Pros:**
- Enterprise requirement for security/compliance
- Higher price point
- Differentiation from competitors

**Cons:**
- Support burden
- Installation complexity
- Update management

**Current Thinking:** Cloud-only for MVP, self-hosted for enterprise deals later.

---

## Changelog

### 2026-05-13
- Initial document creation
- Documented all major architectural decisions
- Captured key learnings from research phase
- Established patterns and conventions

### [Future dates]
- Update with new decisions as project progresses
- Document lessons learned during development
- Track performance optimizations
- Record security findings

---

## Review Schedule

**Weekly:** Review and update during development  
**Phase Transitions:** Major review (MVP → v2 → Enterprise)  
**Retrospectives:** After key milestones

---

## Related Documents

- **CLAUDE.md** - Project overview and architecture
- **SKILLS.md** - Required skills and learning resources
- **PLAN.md** - Project roadmap and phases
- **PLAN_PHASE.md** - Current phase execution details

---

**Last Updated:** May 13, 2026  
**Next Review:** After Week 1 of MVP development
