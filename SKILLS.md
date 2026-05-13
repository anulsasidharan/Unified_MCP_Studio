# SKILLS.md - MCP Designer Required Skills & Learning Resources

**Project:** MCP Designer  
**Owner:** Anu L Sasidharan (OrionVexa)  
**Last Updated:** May 13, 2026

---

## Overview

This document outlines the technical skills required for developing MCP Designer, your current proficiency levels, areas for learning, and curated resources for skill development.

---

## Skill Matrix

### Current Skill Assessment

| Skill Category | Specific Skill | Current Level | Required Level | Priority | Gap |
|---------------|----------------|---------------|----------------|----------|-----|
| **Frontend** | Next.js 14 (App Router) | Advanced | Advanced | High | ✅ None |
| | TypeScript | Advanced | Advanced | High | ✅ None |
| | React Flow / Xyflow | Beginner | Intermediate | High | 📚 Learn |
| | shadcn/ui + Tailwind | Intermediate | Advanced | Medium | 📖 Practice |
| | Monaco Editor Integration | Beginner | Intermediate | High | 📚 Learn |
| | Zustand State Management | Beginner | Intermediate | Medium | 📖 Learn |
| | tRPC | Beginner | Intermediate | Medium | 📚 Learn |
| **Backend** | FastAPI | Advanced | Advanced | High | ✅ None |
| | Python 3.11+ | Advanced | Advanced | High | ✅ None |
| | Jinja2 Templating | Intermediate | Advanced | High | 📖 Practice |
| | Pydantic V2 | Intermediate | Advanced | Medium | 📖 Practice |
| | Celery + Redis | Intermediate | Intermediate | Medium | ✅ None |
| | SQLAlchemy | Advanced | Advanced | Medium | ✅ None |
| **MCP Protocol** | MCP Specification | Beginner | Advanced | Critical | 📚 Learn |
| | MCP TypeScript SDK | Beginner | Advanced | High | 📚 Learn |
| | MCP Python SDK | Beginner | Advanced | High | 📚 Learn |
| | Tool Calling Patterns | Intermediate | Advanced | High | 📖 Learn |
| **Code Gen** | Jinja2 Advanced Features | Intermediate | Advanced | High | 📖 Practice |
| | Abstract Syntax Trees | Beginner | Intermediate | Low | 📖 Optional |
| | TypeScript Code Generation | Beginner | Intermediate | High | 📚 Learn |
| | Python Code Generation | Intermediate | Advanced | High | 📖 Practice |
| **DevOps** | Docker Containerization | Advanced | Advanced | High | ✅ None |
| | GCP Cloud Run | Advanced | Advanced | High | ✅ None |
| | GitHub Actions CI/CD | Intermediate | Advanced | Medium | 📖 Practice |
| | PostgreSQL Administration | Advanced | Advanced | Medium | ✅ None |
| **Security** | Sandboxed Execution | Beginner | Intermediate | High | 📚 Learn |
| | Input Validation | Intermediate | Advanced | High | 📖 Practice |
| | JWT Authentication | Advanced | Advanced | Medium | ✅ None |
| **Testing** | Playwright E2E | Beginner | Intermediate | Medium | 📚 Learn |
| | pytest + FastAPI Testing | Intermediate | Advanced | Medium | 📖 Practice |
| | React Testing Library | Intermediate | Intermediate | Low | ✅ None |

**Legend:**
- ✅ None: No skill gap, ready to use
- 📖 Practice: Need hands-on practice and deeper exploration
- 📚 Learn: Need dedicated learning time before implementation

---

## Critical Learning Path (Pre-Development)

### Week 1: MCP Protocol Deep Dive (20 hours)

**Goal:** Master MCP protocol specification and SDK usage

#### Day 1-2: Protocol Fundamentals (6 hours)
- [ ] Read Anthropic MCP Documentation cover-to-cover
- [ ] Understand the three MCP primitives (Tools, Resources, Prompts)
- [ ] Study transport layers (stdio vs SSE)
- [ ] Review JSON-RPC 2.0 specification (MCP foundation)

**Resources:**
- Official Docs: https://modelcontextprotocol.io/docs
- MCP Spec: https://spec.modelcontextprotocol.io/
- JSON-RPC 2.0: https://www.jsonrpc.org/specification

**Practice:**
```bash
# Hands-on: Build a minimal MCP server manually
# Create a "weather" tool that returns mock data
# Test with Claude Desktop or official client
```

#### Day 3-4: TypeScript SDK Mastery (6 hours)
- [ ] Clone MCP TypeScript SDK repository
- [ ] Study example servers in /examples directory
- [ ] Understand Server, Transport, and Request Handler patterns
- [ ] Build 3 custom tools from scratch

**Resources:**
- GitHub: https://github.com/modelcontextprotocol/typescript-sdk
- Examples: Study calculator, filesystem, and fetch servers

**Practice Project:**
```typescript
// Build a GitHub API MCP server
// Tools: create_issue, list_repos, search_code
// Test all tools with actual GitHub API
```

#### Day 5-6: Python SDK Mastery (6 hours)
- [ ] Clone MCP Python SDK repository
- [ ] Compare patterns with TypeScript SDK
- [ ] Understand async/await patterns in MCP context
- [ ] Build equivalent Python version of GitHub server

**Resources:**
- GitHub: https://github.com/modelcontextprotocol/python-sdk
- Python Async Docs: https://docs.python.org/3/library/asyncio.html

#### Day 7: Resources & Prompts (2 hours)
- [ ] Study resource URI patterns and templates
- [ ] Understand prompt argument substitution
- [ ] Build server with all three primitives (tools, resources, prompts)

---

### Week 2: React Flow & Visual Designer (15 hours)

**Goal:** Build interactive node-based UI for MCP designer

#### Day 1-3: React Flow Fundamentals (9 hours)

**Core Concepts to Master:**
- Nodes and Edges
- Custom Node Components
- Connection Validation
- Layout Algorithms
- State Management with Flow

**Resources:**
- Docs: https://reactflow.dev/learn
- Examples: https://reactflow.dev/examples
- Tutorial: https://www.youtube.com/watch?v=a6P8gv-9pRo

**Practice:**
```tsx
// Build a mini workflow designer
// Nodes: Input, Transform, Output
// Edges: Data flow connections
// Features: Drag-drop, validation, export JSON
```

#### Day 4-5: Monaco Editor Integration (6 hours)

**Integration Tasks:**
- Embed Monaco in React components
- Configure TypeScript/Python language support
- Implement auto-completion
- Add validation and error markers

**Resources:**
- Docs: https://microsoft.github.io/monaco-editor/
- React Integration: https://github.com/suren-atoyan/monaco-react

**Practice:**
```tsx
// Create code editor component with:
// - Syntax highlighting for TS/Python
// - Real-time validation
// - Auto-save with debounce
```

---

### Week 3: Code Generation Engine (12 hours)

**Goal:** Master template-based code generation with Jinja2

#### Day 1-2: Jinja2 Advanced Patterns (6 hours)

**Topics:**
- Template inheritance and blocks
- Macros and includes
- Filters and custom functions
- Whitespace control
- Error handling

**Resources:**
- Docs: https://jinja.palletsprojects.com/
- Tutorial: https://realpython.com/primer-on-jinja-templating/

**Practice:**
```python
# Build a FastAPI code generator
# Input: API spec (JSON)
# Output: Complete FastAPI app with routes, models, docs
```

#### Day 3-4: TypeScript Code Generation (6 hours)

**Challenges:**
- Type definitions generation
- Import statement management
- Code formatting (Prettier integration)
- Validation and error handling

**Practice:**
```python
# Build TypeScript MCP server generator
# Input: Tool definitions (JSON)
# Output: Complete working MCP server
# Include: types, tests, README
```

---

## Skill Development Resources

### 1. MCP Protocol & Ecosystem

**Official Documentation:**
- MCP Specification: https://spec.modelcontextprotocol.io/
- Getting Started: https://modelcontextprotocol.io/quickstart
- SDK Reference: https://github.com/modelcontextprotocol

**Community Resources:**
- Anthropic Discord: MCP channel
- GitHub Discussions: MCP SDK repositories
- Example Servers: Study production implementations

**Learning Projects:**
```
Project 1: Database Query MCP Server
- Tools: query, list_tables, describe_table
- Resources: table schemas, query history
- Test with PostgreSQL and Claude

Project 2: Email MCP Server
- Tools: send_email, search_inbox, get_thread
- Integration: Gmail API or SMTP
- Authentication: OAuth2 flow

Project 3: File System MCP Server
- Tools: read, write, search, list
- Resources: file contents, directory trees
- Security: Sandbox paths, size limits
```

### 2. Frontend Development

**React Flow:**
- Official Docs: https://reactflow.dev
- Examples Gallery: https://reactflow.dev/examples
- Pro Examples: https://pro.reactflow.dev

**Monaco Editor:**
- Official Docs: https://microsoft.github.io/monaco-editor/
- React Wrapper: https://github.com/suren-atoyan/monaco-react
- Language Services: TypeScript/Python config

**shadcn/ui:**
- Component Library: https://ui.shadcn.com
- Themes: https://ui.shadcn.com/themes
- Examples: https://ui.shadcn.com/examples

**tRPC:**
- Docs: https://trpc.io/docs
- Next.js Integration: https://trpc.io/docs/nextjs
- End-to-end Type Safety patterns

### 3. Backend Development

**FastAPI Advanced:**
- Dependency Injection: https://fastapi.tiangolo.com/tutorial/dependencies/
- Background Tasks: https://fastapi.tiangolo.com/tutorial/background-tasks/
- WebSockets: https://fastapi.tiangolo.com/advanced/websockets/

**Pydantic V2:**
- Migration Guide: https://docs.pydantic.dev/latest/migration/
- JSON Schema: https://docs.pydantic.dev/latest/usage/json_schema/
- Validation: https://docs.pydantic.dev/latest/usage/validators/

**Celery:**
- Docs: https://docs.celeryproject.org/
- FastAPI Integration: https://fastapi.tiangolo.com/tutorial/background-tasks/
- Redis Backend: https://docs.celeryproject.org/en/stable/getting-started/backends-and-brokers/redis.html

### 4. Code Generation

**Jinja2:**
- Template Designer Docs: https://jinja.palletsprojects.com/templates/
- API: https://jinja.palletsprojects.com/api/
- Extensions: https://jinja.palletsprojects.com/extensions/

**TypeScript Generation:**
- TypeScript Handbook: https://www.typescriptlang.org/docs/handbook/
- ts-morph (AST manipulation): https://ts-morph.com/

**Python Generation:**
- ast module: https://docs.python.org/3/library/ast.html
- black (formatting): https://black.readthedocs.io/

### 5. Testing

**Playwright:**
- Docs: https://playwright.dev/
- Next.js Testing: https://nextjs.org/docs/pages/building-your-application/testing/playwright
- Best Practices: https://playwright.dev/docs/best-practices

**pytest:**
- FastAPI Testing: https://fastapi.tiangolo.com/tutorial/testing/
- Fixtures: https://docs.pytest.org/en/stable/fixture.html
- Async Tests: https://pytest-asyncio.readthedocs.io/

### 6. DevOps & Deployment

**Docker:**
- Multi-stage Builds: https://docs.docker.com/build/building/multi-stage/
- Security: https://docs.docker.com/engine/security/
- Best Practices: https://docs.docker.com/develop/dev-best-practices/

**GCP Cloud Run:**
- Docs: https://cloud.google.com/run/docs
- Containers: https://cloud.google.com/run/docs/deploying
- CI/CD: https://cloud.google.com/run/docs/continuous-deployment

---

## Hands-On Learning Projects

### Project 1: Mini MCP Designer (Week 1-2)

**Goal:** Build a simplified version with one tool builder

**Features:**
- Visual tool parameter builder (React Flow)
- Code editor for handler (Monaco)
- Code generation (Jinja2)
- Testing with Claude API

**Tech Stack:**
- Next.js + React Flow + Monaco
- FastAPI + Jinja2
- No database (in-memory)

**Learning Outcomes:**
- End-to-end MCP server generation
- Visual designer patterns
- Code generation workflow

### Project 2: MCP Template Generator (Week 3)

**Goal:** CLI tool for generating MCP servers from templates

**Features:**
- Interactive CLI (click or inquirer)
- 5 templates (API, DB, FS, GitHub, Slack)
- Variable substitution
- Test generation

**Tech Stack:**
- Python CLI
- Jinja2 templates
- pytest for template testing

**Learning Outcomes:**
- Template architecture
- CLI UX patterns
- Test generation strategies

### Project 3: MCP Testing Sandbox (Week 4)

**Goal:** Docker-based sandbox for MCP server testing

**Features:**
- Docker container isolation
- Resource limits (CPU, memory)
- Claude API integration
- Request/response logging

**Tech Stack:**
- Docker
- FastAPI
- Anthropic SDK

**Learning Outcomes:**
- Sandboxed execution
- Security best practices
- Testing infrastructure

---

## Common Pitfalls & Solutions

### MCP Protocol

**Pitfall 1: Incorrect JSON Schema**
- Problem: Tools not recognized by Claude
- Solution: Validate against JSON Schema Draft 7
- Tool: https://www.jsonschemavalidator.net/

**Pitfall 2: Transport Layer Issues**
- Problem: Server not responding
- Solution: Check stdio/SSE configuration, test with official clients
- Debug: Add extensive logging

**Pitfall 3: Error Handling**
- Problem: Cryptic errors crash server
- Solution: Wrap all handlers with try-catch, return structured errors

### Code Generation

**Pitfall 1: Template Complexity**
- Problem: Templates become unmaintainable
- Solution: Use template inheritance, break into smaller components
- Pattern: Base template + specialized overrides

**Pitfall 2: Invalid Generated Code**
- Problem: Syntax errors in output
- Solution: Validate generated code with linters before saving
- Tools: eslint (TS), black (Python)

**Pitfall 3: Missing Dependencies**
- Problem: Generated code references unavailable packages
- Solution: Template includes package.json/requirements.txt generation
- Validation: Check all imports against declared dependencies

### React Flow

**Pitfall 1: Performance Issues**
- Problem: Slow rendering with many nodes
- Solution: Use React Flow's built-in optimization, memoization
- Reference: https://reactflow.dev/learn/advanced-use/performance

**Pitfall 2: State Synchronization**
- Problem: Flow state out of sync with backend
- Solution: Single source of truth, optimistic updates
- Pattern: Zustand store + React Query

---

## Skill Development Timeline

### Pre-MVP (4 weeks)

**Week 1: MCP Protocol Mastery**
- Study specification (6 hours)
- Build 3 practice servers (10 hours)
- Test with Claude (4 hours)

**Week 2: Frontend Skills**
- React Flow deep dive (9 hours)
- Monaco integration (6 hours)

**Week 3: Code Generation**
- Jinja2 advanced (6 hours)
- TypeScript generation (6 hours)

**Week 4: Integration**
- Build Mini MCP Designer (15 hours)
- End-to-end testing (5 hours)

### During MVP (6-8 weeks)

**Continuous Learning:**
- Read MCP ecosystem updates weekly
- Study other MCP servers for patterns
- Participate in Anthropic Discord discussions
- Document learnings in MEMORY.md

---

## Recommended Learning Schedule

### Daily (During MVP Development)

**Morning (1 hour before coding):**
- Review related documentation
- Study example code from MCP ecosystem
- Plan day's implementation

**During Development:**
- Reference documentation actively
- Experiment with new patterns
- Document decisions in MEMORY.md

**Evening (30 minutes after coding):**
- Review code quality
- Update learning journal
- Prepare next day's focus

### Weekly

**Saturday (2 hours):**
- Study advanced topics
- Build mini experiments
- Update SKILLS.md with progress

**Sunday (1 hour):**
- Review week's learnings
- Plan next week's skill focus
- Research new patterns

---

## Skill Assessment Checkpoints

### After Week 1
- [ ] Can explain MCP protocol primitives
- [ ] Built 3 working MCP servers manually
- [ ] Understand transport layers
- [ ] Comfortable with both TS and Python SDKs

### After Week 2
- [ ] Created custom React Flow designer
- [ ] Integrated Monaco editor
- [ ] Implemented node validation
- [ ] Built basic state management

### After Week 3
- [ ] Generated working TypeScript code from templates
- [ ] Implemented code validation pipeline
- [ ] Created 5+ Jinja2 templates
- [ ] Tested generated code successfully

### After Week 4
- [ ] Built end-to-end Mini MCP Designer
- [ ] Generated and tested MCP servers
- [ ] Implemented Claude API integration
- [ ] Ready to start MVP development

---

## Advanced Topics (Post-MVP)

### Phase 2 Learning

**SSE Transport:**
- Server-Sent Events specification
- Long-polling vs SSE vs WebSockets
- Production SSE deployment patterns

**Multi-Agent Patterns:**
- Tool chaining and composition
- Agent-to-agent communication via MCP
- Workflow orchestration

**Advanced Security:**
- OAuth2 flows in MCP servers
- Rate limiting and abuse prevention
- Secrets management in generated code

### Enterprise Features

**Self-Hosted Deployment:**
- Kubernetes deployment
- High availability patterns
- Monitoring and observability

**Team Collaboration:**
- Real-time collaborative editing
- Version control integration
- Conflict resolution

---

## Resources Repository

### Bookmarks

```
MCP Protocol:
- Spec: https://spec.modelcontextprotocol.io/
- TypeScript SDK: https://github.com/modelcontextprotocol/typescript-sdk
- Python SDK: https://github.com/modelcontextprotocol/python-sdk

Frontend:
- React Flow: https://reactflow.dev
- Monaco: https://microsoft.github.io/monaco-editor/
- shadcn/ui: https://ui.shadcn.com

Backend:
- FastAPI: https://fastapi.tiangolo.com
- Jinja2: https://jinja.palletsprojects.com
- Celery: https://docs.celeryproject.org

Testing:
- Playwright: https://playwright.dev
- pytest: https://docs.pytest.org

DevOps:
- Cloud Run: https://cloud.google.com/run/docs
- Docker: https://docs.docker.com
```

### GitHub Repositories to Study

```
Official MCP Servers:
- https://github.com/modelcontextprotocol/servers

Community Examples:
- Search GitHub: topic:mcp-server
- Filter by: Most stars, Recent activity

Code Generation Examples:
- https://github.com/tiangolo/fastapi/tree/master/scripts
- https://github.com/swagger-api/swagger-codegen
```

---

## Skill Development Tracking

### Learning Journal Template

```markdown
## [Date] - [Skill Area]

### What I Learned:
- [Key concept or pattern]
- [New technique or tool]

### What I Built:
- [Practice project or experiment]
- [Code snippet or example]

### Challenges:
- [Problem encountered]
- [How I solved it]

### Next Steps:
- [What to learn next]
- [Practice needed]

### Resources Used:
- [Links to docs or tutorials]
```

### Weekly Review Template

```markdown
## Week [N] Review

### Skills Practiced:
- [Skill 1]: [Hours spent]
- [Skill 2]: [Hours spent]

### Projects Completed:
- [Project name]: [Description]

### Key Learnings:
- [Top 3 insights]

### Areas Needing More Work:
- [Skill gap identified]

### Plan for Next Week:
- [Focus area]
- [Learning goals]
```

---

## Contact for Learning Support

**Questions or Blockers:**
- Anthropic Discord: MCP channel
- GitHub Discussions: SDK repositories
- Stack Overflow: #mcp-protocol tag

**Code Review:**
- Post in Anthropic community
- Share WIP in GitHub discussions
- Request feedback from AI engineering peers

---

**Last Updated:** May 13, 2026  
**Next Review:** After Week 4 of learning
