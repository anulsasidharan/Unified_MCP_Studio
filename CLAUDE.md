# CLAUDE.md - Unified MCP Studio

**Project Name:** Unified MCP Studio  
**Also referred to as:** MCP Designer (early docs / feasibility report)  
**Project Type:** AI-Powered Developer Tool — Visual MCP Server Builder  
**Owner:** Anu L Sasidharan (OrionVexa)  
**Version:** 1.0.0  
**Last Updated:** May 13, 2026

---

## Project Overview

**Unified MCP Studio** is a visual development environment for creating, testing, and deploying Model Context Protocol (MCP) servers without requiring deep protocol knowledge. It enables developers to build AI tool integrations through a drag-and-drop interface with automatic code generation, built-in testing, and one-click deployment.

### Vision Statement

Democratize MCP server development by providing an intuitive visual interface that reduces development time from hours to minutes, making AI tool integration accessible to developers of all skill levels.

### Core Value Proposition

- **Visual Design**: Drag-and-drop tool, resource, and prompt builder
- **Auto Code Generation**: Production-ready TypeScript/Python MCP servers
- **Integrated Testing**: Built-in Claude API testing environment
- **Template Library**: Pre-built patterns for common integrations
- **One-Click Deploy**: Automated deployment to GCP, AWS, or local environments

---

## Project Context

### Why This Project?

1. **Market Gap**: No visual designers exist for MCP server development
2. **Developer Pain**: Manual MCP server creation is time-consuming and error-prone
3. **Growing Ecosystem**: MCP adoption accelerating with Claude and other LLMs
4. **Portfolio Value**: Demonstrates AI/ML engineering capabilities and innovation
5. **Career Impact**: Strong talking point for AI engineering interviews

### Target Users

- AI engineers building custom tool integrations
- Enterprise teams needing secure internal API access for LLMs
- SaaS companies creating MCP connectors for customers
- Independent developers contributing to MCP ecosystem
- Platform engineers extending AI capabilities

---

## Technical Architecture

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────┐
│                   Frontend (Next.js 14 + TS)                 │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  Visual    │  │   Schema   │  │  Testing   │            │
│  │  Designer  │  │  Builder   │  │  Console   │            │
│  │ (React Flow)│ │  (Monaco)  │  │  (Claude)  │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend API (FastAPI + Python)                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  Code Gen  │  │    MCP     │  │ Deployment │            │
│  │  Engine    │  │  Runtime   │  │  Manager   │            │
│  │ (Jinja2)   │  │  Sandbox   │  │  (Docker)  │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Data Layer (GCP/PostgreSQL)                 │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ PostgreSQL │  │   Redis    │  │   GCS/S3   │            │
│  │ (Projects) │  │  (Cache)   │  │ (Artifacts)│            │
│  └────────────┘  └────────────┘  └────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Frontend:**
- Framework: Next.js 14 (App Router) + TypeScript
- UI Library: shadcn/ui + Tailwind CSS
- Visualization: React Flow (node-based designer)
- Code Editor: Monaco Editor (VS Code editor)
- State: Zustand (lightweight state management)
- API Client: tRPC (end-to-end type safety)

**Backend:**
- API Framework: FastAPI (Python 3.11+)
- Code Generation: Jinja2 templates
- MCP Runtime: subprocess with resource limits
- Task Queue: Celery + Redis (async operations)
- Validation: Pydantic models + JSON Schema

**Data:**
- Primary DB: PostgreSQL 15 (projects, users, templates)
- Cache: Redis 7 (sessions, rate limiting)
- Object Storage: Google Cloud Storage (generated code, logs)
- Search: PostgreSQL full-text search

**Infrastructure:**
- Cloud: Google Cloud Platform (GCP)
- API Hosting: Cloud Run (serverless containers)
- Database: Cloud SQL PostgreSQL
- Storage: Cloud Storage
- CI/CD: GitHub Actions
- Monitoring: Sentry + Cloud Monitoring

---

## Core Features

### 1. Visual Designer (MVP Priority: High)

**Tool Builder:**
- Drag-and-drop tool creation interface
- JSON Schema form builder for parameters
- Monaco editor for handler code (Python/TypeScript)
- Real-time validation and error highlighting
- Tool metadata configuration (name, description, examples)

**Resource Builder:**
- URI template configuration
- MIME type selection
- Resource provider code editor
- Template variables and substitution

**Prompt Builder:**
- Argument definition with types
- Message template editor
- Preview with sample data

**Visual Flow:**
```
[New Tool] → [Define Metadata] → [Build Input Schema] → [Write Handler] → [Test] → [Generate Code]
```

### 2. Code Generation Engine (MVP Priority: High)

**Capabilities:**
- Template-based generation (Jinja2)
- TypeScript MCP server (stdio transport)
- Python MCP server (stdio transport)
- Docker containerization
- Error handling boilerplate
- Type definitions and interfaces
- Documentation comments

**Output Structure:**
```
generated-server/
├── package.json / pyproject.toml
├── src/
│   ├── index.ts / main.py
│   ├── tools/
│   │   └── {tool_name}.ts
│   ├── resources/
│   │   └── {resource_name}.ts
│   ├── prompts/
│   │   └── {prompt_name}.ts
│   └── types/
│       └── schemas.ts
├── tests/
│   └── {tool_name}.test.ts
├── Dockerfile
└── README.md
```

### 3. Testing Environment (MVP Priority: High)

**Interactive Testing:**
- Live MCP server instantiation in sandbox
- Claude API integration for tool calling
- Request/response inspection UI
- Error stack traces and debugging
- Performance metrics (latency, token usage)

**Test Cases:**
- Manual tool invocation with custom inputs
- Saved test scenarios
- Mock data injection for external dependencies
- Batch testing for multiple tools

### 4. Template Library (MVP Priority: Medium)

**Initial Templates (MVP):**
1. REST API Wrapper (generic HTTP client)
2. PostgreSQL Query (read-only database access)
3. File System Access (local file operations)
4. GitHub Integration (issues, PRs, commits)
5. Slack Integration (channel messages)

**Template Structure:**
```typescript
interface Template {
  id: string;
  name: string;
  description: string;
  category: 'api' | 'database' | 'filesystem' | 'integration';
  tools: ToolTemplate[];
  resources: ResourceTemplate[];
  config: TemplateConfig;
  documentation: string;
}
```

### 5. Deployment Manager (Post-MVP)

**Supported Targets:**
- Local Development (npm/pip install)
- GCP Cloud Run (container deployment)
- AWS Lambda (serverless function)
- Docker Registry (container push)
- Vercel/Netlify (SSE transport)

**Deployment Flow:**
```
[Select Target] → [Configure Env Vars] → [Deploy] → [Health Check] → [Generate URL]
```

---

## Database Schema

### Core Tables

```sql
-- Users and Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    tier VARCHAR(50) DEFAULT 'free', -- free, pro, team, enterprise
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- MCP Projects
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    runtime VARCHAR(50) NOT NULL, -- typescript, python
    transport VARCHAR(50) NOT NULL, -- stdio, sse
    config JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tools
CREATE TABLE tools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    input_schema JSONB NOT NULL,
    handler_code TEXT NOT NULL,
    handler_language VARCHAR(50) NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Resources
CREATE TABLE resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    uri VARCHAR(500) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    mime_type VARCHAR(100),
    provider_code TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Prompts
CREATE TABLE prompts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    arguments JSONB DEFAULT '[]',
    messages JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Templates
CREATE TABLE templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    is_public BOOLEAN DEFAULT true,
    author_id UUID REFERENCES users(id),
    use_count INTEGER DEFAULT 0,
    config JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Test Cases
CREATE TABLE test_cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tool_id UUID REFERENCES tools(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    input_data JSONB NOT NULL,
    expected_output JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Deployments
CREATE TABLE deployments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    target VARCHAR(100) NOT NULL, -- local, cloud_run, lambda, docker
    status VARCHAR(50) NOT NULL, -- pending, building, deployed, failed
    url VARCHAR(500),
    error_message TEXT,
    deployed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_tools_project_id ON tools(project_id);
CREATE INDEX idx_resources_project_id ON resources(project_id);
CREATE INDEX idx_prompts_project_id ON prompts(project_id);
CREATE INDEX idx_templates_category ON templates(category);
CREATE INDEX idx_deployments_project_id ON deployments(project_id);
```

---

## API Endpoints

**Base path:** `/api/v1` (see `docs/API_SPEC.md`). **Liveness:** `GET /health` (outside versioned prefix) and `GET /api/v1/health`.

### Authentication

```
POST   /api/v1/auth/register       # User registration
POST   /api/v1/auth/login          # User login
POST   /api/v1/auth/logout         # User logout
GET    /api/v1/auth/me             # Current user info
```

### Projects

```
GET    /api/v1/projects            # List user projects
POST   /api/v1/projects            # Create new project
GET    /api/v1/projects/{id}       # Get project details
PUT    /api/v1/projects/{id}       # Update project
DELETE /api/v1/projects/{id}      # Delete project
```

### Tools

```
GET    /api/v1/projects/{id}/tools    # List project tools
POST   /api/v1/projects/{id}/tools    # Create tool
GET    /api/v1/tools/{id}             # Get tool details
PUT    /api/v1/tools/{id}             # Update tool
DELETE /api/v1/tools/{id}            # Delete tool
POST   /api/v1/tools/{id}/test        # Test tool execution
```

### Resources

```
GET    /api/v1/projects/{id}/resources  # List project resources
POST   /api/v1/projects/{id}/resources  # Create resource
GET    /api/v1/resources/{id}           # Get resource details
PUT    /api/v1/resources/{id}           # Update resource
DELETE /api/v1/resources/{id}           # Delete resource
```

### Code Generation

```
POST   /api/v1/projects/{id}/generate   # Generate MCP server code
GET    /api/v1/projects/{id}/download   # Download generated code
POST   /api/v1/projects/{id}/validate   # Validate project config
```

### Templates

```
GET    /api/v1/templates               # List available templates
GET    /api/v1/templates/{id}          # Get template details
POST   /api/v1/projects/from-template  # Create project from template
```

### Testing

```
POST   /api/v1/testing/sandbox/start   # Start test sandbox
POST   /api/v1/testing/sandbox/execute # Execute tool in sandbox
POST   /api/v1/testing/sandbox/stop    # Stop test sandbox
GET    /api/v1/testing/results/{id}    # Get test results
```

### Deployment

```
POST   /api/v1/deployments            # Create deployment
GET    /api/v1/deployments/{id}       # Get deployment status
GET    /api/v1/deployments/{id}/logs  # Get deployment logs
DELETE /api/v1/deployments/{id}       # Delete deployment
```

---

## Code Generation Templates

### TypeScript MCP Server Template Structure

```typescript
// src/index.ts (Main Entry Point)
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";

// Generated tool imports
{% for tool in tools %}
import { {{ tool.name }}Tool } from "./tools/{{ tool.name }}.js";
{% endfor %}

// Server initialization
const server = new Server(
  {
    name: "{{ project_name }}",
    version: "{{ version }}",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tool registration
{% for tool in tools %}
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "{{ tool.name }}",
      description: "{{ tool.description }}",
      inputSchema: {{ tool.input_schema | tojson }},
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "{{ tool.name }}") {
    return await {{ tool.name }}Tool(request.params.arguments);
  }
  throw new Error(`Unknown tool: ${request.params.name}`);
});
{% endfor %}

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
```

### Python MCP Server Template Structure

```python
# main.py (Main Entry Point)
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Generated tool imports
{% for tool in tools %}
from tools.{{ tool.name }} import {{ tool.name }}_handler
{% endfor %}

# Server initialization
app = Server("{{ project_name }}")

# Tool definitions
{% for tool in tools %}
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="{{ tool.name }}",
            description="{{ tool.description }}",
            inputSchema={{ tool.input_schema | tojson }},
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "{{ tool.name }}":
        result = await {{ tool.name }}_handler(arguments)
        return [TextContent(type="text", text=str(result))]
    raise ValueError(f"Unknown tool: {name}")
{% endfor %}

# Main entry point
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Development Workflow

### Developer Setup

```bash
# Clone repository
git clone https://github.com/orionvexa/unified-mcp-studio.git
cd unified-mcp-studio

# Frontend setup
cd frontend
npm install
cp .env.example .env.local
npm run dev

# Backend setup
cd ../backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Database setup (from repo root)
docker compose up -d postgres redis
# After Alembic is added (Phase 1+): cd backend && alembic upgrade head
```

### Project Structure

Canonical layout matches **`docs/ARCHITECTURE.md`** (monorepo root):

```
unified-mcp-studio/
├── frontend/                 # Next.js 14 (App Router)
│   ├── src/app/             # Routes: (auth), dashboard, projects, templates, …
│   ├── src/components/      # designer/, editor/, ui/
│   ├── src/lib/             # API client, stores
│   ├── public/
│   └── Dockerfile
├── backend/                 # FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api/v1/          # routers: auth, projects, tools, …
│   │   ├── services/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── workers/         # Celery (Phase 4+)
│   │   └── core/            # security, logging, rate_limit
│   ├── tests/
│   ├── alembic/             # Phase 1+
│   ├── Dockerfile
│   └── pyproject.toml
├── templates/               # Jinja2 MCP server templates (TS / Python)
│   ├── typescript/
│   └── python/
├── docker-compose.yml
├── Makefile                 # optional dev shortcuts
├── TASKS.md
└── docs/
```

---

## Testing Strategy

### Unit Tests

**Frontend:**
- Component rendering tests (React Testing Library)
- State management tests (Zustand)
- Utility function tests (Vitest)

**Backend:**
- API endpoint tests (pytest + FastAPI TestClient)
- Code generation tests (template output validation)
- Database model tests (SQLAlchemy)

### Integration Tests

- End-to-end project creation flow
- Code generation → sandbox execution
- Template instantiation and customization
- Deployment pipeline tests

### E2E Tests

- Playwright for full user workflows
- Critical paths: signup → create project → generate → test → deploy

---

## Security Considerations

### User Input Validation

- Sanitize all user-provided code before execution
- JSON Schema validation for all API inputs
- SQL injection prevention (parameterized queries)
- XSS prevention (Content Security Policy)

### Code Execution Sandbox

- Docker container isolation for MCP server testing
- Resource limits (CPU, memory, network)
- Time limits for execution
- No file system write access

### Authentication & Authorization

- JWT-based authentication
- Role-based access control (RBAC)
- Rate limiting on all endpoints
- API key management for deployments

### Data Protection

- Encrypted passwords (bcrypt)
- HTTPS only in production
- Environment variable secrets
- No sensitive data in logs

---

## Performance Optimization

### Frontend

- Code splitting and lazy loading
- React Flow performance optimization
- Debounced auto-save
- Optimistic UI updates

### Backend

- Redis caching for templates and project metadata
- Database query optimization (proper indexes)
- Async operations for long-running tasks (Celery)
- Connection pooling for PostgreSQL

### Infrastructure

- CDN for static assets (GCS + Cloud CDN)
- Horizontal scaling for API (Cloud Run)
- Database read replicas for heavy queries

---

## Monitoring & Observability

### Metrics

- API response times (p50, p95, p99)
- Code generation success rate
- Sandbox execution failures
- User engagement metrics (DAU, MAU)

### Logging

- Structured logging (JSON format)
- Log levels (DEBUG, INFO, WARNING, ERROR)
- User action audit logs
- System error tracking (Sentry)

### Alerts

- API error rate > 5%
- Database connection failures
- Deployment failures
- High memory usage in sandbox

---

## Deployment Pipeline

### CI/CD Workflow (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          npm test
          pytest

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build frontend
        run: npm run build
      
      - name: Build backend
        run: docker build -t unified-mcp-studio-api .
      
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy unified-mcp-studio-api \
            --image gcr.io/PROJECT_ID/unified-mcp-studio-api \
            --platform managed \
            --region us-central1
```

---

## Contributing Guidelines

### Code Style

- Frontend: ESLint + Prettier (Airbnb style)
- Backend: Black + isort + flake8 (PEP 8)
- Commit messages: Conventional Commits format

### Pull Request Process

1. Create feature branch from `main`
2. Write tests for new features
3. Update documentation
4. Submit PR with description and screenshots
5. Pass CI checks and code review
6. Squash and merge

---

## License

MIT License - See LICENSE file for details

---

## Contact & Support

**Project Owner:** Anu L Sasidharan  
**Email:** anulsasidharan@gmail.com  
**GitHub:** https://github.com/anulsasidharan  
**LinkedIn:** https://linkedin.com/in/anulsasidharan  
**Website:** https://orionvexa.com

---

## Claude Code CLI Instructions

This project is optimized for development with Claude Code CLI in Cursor IDE.

### Usage Patterns

**Creating new features:**
```bash
claude-code "Add authentication middleware with JWT support"
```

**Debugging issues:**
```bash
claude-code "Fix code generation bug where TypeScript imports are incorrect"
```

**Refactoring:**
```bash
claude-code "Refactor tool builder component to use composition pattern"
```

### Context Files

- `CLAUDE.md` - This file (project overview)
- `SKILLS.md` - Skill requirements and learning resources
- `MEMORY.md` - Project decisions and rationale
- `PLAN.md` - Development roadmap
- `PLAN_PHASE.md` - Current phase execution plan

### Best Practices

1. Always reference this CLAUDE.md for architecture decisions
2. Update MEMORY.md when making significant changes
3. Keep PLAN_PHASE.md current with implementation status
4. Use existing code patterns and templates
5. Write tests alongside feature development

---

**Last Updated:** May 13, 2026  
**Version:** 1.0.0  
**Status:** Planning Phase
