# PLAN.md - MCP Designer Project Roadmap

**Project:** MCP Designer  
**Owner:** Anu L Sasidharan (OrionVexa)  
**Start Date:** May 13, 2026  
**Last Updated:** May 13, 2026

---

## Vision & Goals

### Long-Term Vision (12-18 months)

MCP Designer becomes the **de facto visual development environment** for building MCP servers, empowering developers of all skill levels to create, test, and deploy AI tool integrations in minutes instead of hours.

### Success Metrics

**Year 1 Targets:**
- 1,000+ registered users
- 100+ paying customers
- 500+ MCP servers deployed
- $10K+ MRR (Monthly Recurring Revenue)
- 85%+ first-time deployment success rate
- NPS score > 40

**Technical Metrics:**
- < 30s code generation time
- < 5% generated code error rate
- 99.9% API uptime
- < 200ms average API response time

---

## Project Phases

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 0: Learning & Validation (4 weeks)                     │
│ Phase 1: MVP Development (6-8 weeks)                         │
│ Phase 2: Beta & Iteration (4 weeks)                          │
│ Phase 3: Launch & Growth (8 weeks)                           │
│ Phase 4: Platform Enhancement (12 weeks)                     │
│ Phase 5: Enterprise Readiness (16 weeks)                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 0: Learning & Validation (4 weeks)

**Status:** 🟢 Current Phase  
**Start Date:** May 13, 2026  
**Target Completion:** June 10, 2026  
**Effort:** 20-25 hours/week

### Objectives

1. Master MCP protocol and SDKs
2. Validate market demand
3. Build proof-of-concept components
4. Finalize technical architecture
5. Establish development workflow

### Week 1: MCP Protocol Deep Dive (May 13-19)

**Goals:**
- [ ] Complete Anthropic MCP documentation
- [ ] Build 3 MCP servers manually (TypeScript)
- [ ] Build 2 MCP servers manually (Python)
- [ ] Test servers with Claude Desktop
- [ ] Join Anthropic Discord and engage with community

**Deliverables:**
- 5 working MCP servers
- Notes on protocol patterns
- List of common pitfalls
- Understanding of SDK differences (TS vs Python)

**Time Allocation:**
- Reading/Study: 8 hours
- Hands-on Building: 12 hours
- Community Engagement: 2 hours

### Week 2: Frontend Skills Development (May 20-26)

**Goals:**
- [ ] Complete React Flow tutorial
- [ ] Build mini node-based designer
- [ ] Integrate Monaco Editor
- [ ] Implement node validation logic
- [ ] Create basic state management with Zustand

**Deliverables:**
- Working node designer prototype
- Code editor integration
- State management pattern

**Time Allocation:**
- React Flow: 9 hours
- Monaco Integration: 6 hours
- State Management: 5 hours

### Week 3: Code Generation Prototyping (May 27 - June 2)

**Goals:**
- [ ] Design Jinja2 template structure
- [ ] Create TypeScript MCP server template
- [ ] Create Python MCP server template
- [ ] Build code generation engine POC
- [ ] Test generated code quality

**Deliverables:**
- 2 complete templates (TS + Python)
- Code generation script
- Generated servers that pass tests

**Time Allocation:**
- Template Design: 6 hours
- TypeScript Template: 6 hours
- Python Template: 6 hours
- Testing: 2 hours

### Week 4: Market Validation & Architecture (June 3-9)

**Goals:**
- [ ] Create landing page with email capture
- [ ] Survey 20-30 developers about MCP pain points
- [ ] Study competitor tools (Retool, n8n, Postman)
- [ ] Finalize MVP feature scope
- [ ] Write architecture decision records

**Deliverables:**
- Landing page (live)
- Survey results and insights
- Final MVP feature list
- Updated MEMORY.md with decisions

**Time Allocation:**
- Landing Page: 6 hours
- Market Research: 8 hours
- Architecture Planning: 6 hours

### Exit Criteria

- [ ] Can build MCP servers confidently without docs
- [ ] Working prototype of core components
- [ ] 50+ email signups from landing page
- [ ] Validated demand from developer surveys
- [ ] Finalized MVP scope and architecture

---

## Phase 1: MVP Development (6-8 weeks)

**Status:** ⏳ Planned  
**Target Start:** June 10, 2026  
**Target Completion:** July 29 - August 5, 2026  
**Effort:** 25-30 hours/week

### Objectives

Build and deploy a working MVP with core features:
- Visual tool builder
- TypeScript code generation
- Local testing environment
- 5-10 starter templates
- Basic authentication

### Sprint Structure

**2-week sprints:**
- Sprint 1: Foundation (June 10-23)
- Sprint 2: Designer (June 24 - July 7)
- Sprint 3: Generation (July 8-21)
- Sprint 4: Testing & Polish (July 22 - August 5)

### Sprint 1: Foundation (June 10-23)

**Goals:**
- [ ] Project scaffolding (frontend + backend repos)
- [ ] Database schema implementation
- [ ] Authentication system (JWT)
- [ ] Basic API endpoints (CRUD projects)
- [ ] CI/CD pipeline setup

**Deliverables:**
- Working auth flow (signup, login, logout)
- Projects API (create, read, update, delete)
- GitHub Actions CI/CD
- Deployed to staging (Cloud Run + Vercel)

**User Stories:**
```
As a developer, I can:
- Sign up with email/password
- Log in and see my dashboard
- Create a new MCP project
- View my project list
- Delete projects
```

**Technical Tasks:**
1. Next.js 14 project setup with TypeScript
2. FastAPI project setup with PostgreSQL
3. Database migrations (Alembic)
4. Auth endpoints (register, login, refresh)
5. Protected API routes
6. Deployment configs (Dockerfile, docker-compose)
7. CI/CD workflows (test, build, deploy)

**Time Estimate:** 60-70 hours

### Sprint 2: Visual Designer (June 24 - July 7)

**Goals:**
- [ ] React Flow integration
- [ ] Tool builder UI
- [ ] JSON Schema form builder
- [ ] Monaco editor for handler code
- [ ] Real-time validation

**Deliverables:**
- Working visual designer
- Tool creation flow
- Parameter definition interface
- Code editor with syntax highlighting

**User Stories:**
```
As a developer, I can:
- Add tools to my project via drag-and-drop
- Define tool name and description
- Add parameters with types (string, number, boolean)
- Write handler code in Monaco editor
- See validation errors in real-time
```

**Technical Tasks:**
1. React Flow canvas setup
2. Custom Tool node component
3. JSON Schema form generator
4. Monaco editor integration with TS/Python modes
5. Validation logic (schema validation)
6. Save/load designer state to backend
7. Undo/redo functionality

**Time Estimate:** 60-70 hours

### Sprint 3: Code Generation (July 8-21)

**Goals:**
- [ ] Code generation engine
- [ ] TypeScript template implementation
- [ ] Import management
- [ ] Code formatting (Prettier)
- [ ] Download generated code

**Deliverables:**
- Working code generator
- TypeScript MCP server generation
- Formatted, valid output
- Download as .zip file

**User Stories:**
```
As a developer, I can:
- Click "Generate Code" on my project
- Preview generated MCP server code
- Download complete server as .zip
- Run generated server locally
- Test with Claude Desktop
```

**Technical Tasks:**
1. Jinja2 template engine setup
2. TypeScript base template
3. Tool code generation
4. Type definitions generation
5. package.json generation
6. README generation
7. Code validation (eslint)
8. Zip file creation
9. Download API endpoint

**Time Estimate:** 60-70 hours

### Sprint 4: Testing & Polish (July 22 - August 5)

**Goals:**
- [ ] Testing console UI
- [ ] Claude API integration
- [ ] Test execution sandbox
- [ ] Template library (5 templates)
- [ ] UI/UX polish
- [ ] Documentation

**Deliverables:**
- Interactive testing console
- 5 working templates
- User documentation
- Video walkthrough

**User Stories:**
```
As a developer, I can:
- Test my tools in a sandbox environment
- See request/response for each tool call
- Use templates to quick-start projects
- Read documentation and examples
- Watch tutorial video
```

**Technical Tasks:**
1. Testing console UI
2. Docker sandbox implementation
3. Claude API integration (tool calling)
4. Test execution flow
5. Template creation (5 templates)
6. Documentation site (Next.js)
7. Tutorial video script + recording
8. UI polish pass
9. Bug fixes
10. Performance optimization

**Time Estimate:** 60-70 hours

### MVP Feature Checklist

**Must Have (P0):**
- [x] User authentication (email/password)
- [ ] Visual tool builder
- [ ] JSON Schema parameter definition
- [ ] Monaco code editor
- [ ] TypeScript code generation
- [ ] Download generated code
- [ ] Testing console with Claude API
- [ ] 5 starter templates
- [ ] Basic documentation

**Should Have (P1):**
- [ ] Project sharing (view-only link)
- [ ] Code preview before download
- [ ] Template search/filter
- [ ] Keyboard shortcuts
- [ ] Dark mode

**Nice to Have (P2):**
- [ ] Python code generation
- [ ] Resource builder
- [ ] Prompt builder
- [ ] Deployment to Cloud Run
- [ ] Team collaboration

### Exit Criteria

- [ ] All P0 features complete and tested
- [ ] Can create, generate, download, and test MCP server end-to-end
- [ ] No critical bugs
- [ ] Documentation complete
- [ ] Video tutorial published
- [ ] Deployed to production (beta)

---

## Phase 2: Beta & Iteration (4 weeks)

**Status:** ⏳ Planned  
**Target Start:** August 5, 2026  
**Target Completion:** September 2, 2026  
**Effort:** 15-20 hours/week (maintenance mode)

### Objectives

- Launch beta to early users
- Gather feedback and iterate
- Fix bugs and improve UX
- Optimize performance
- Prepare for public launch

### Week 1: Beta Launch (August 5-11)

**Goals:**
- [ ] Deploy to production
- [ ] Launch Product Hunt (beta)
- [ ] Email waitlist (from Phase 0)
- [ ] Reddit posts (r/LangChain, r/MachineLearning)
- [ ] Twitter announcement

**Metrics to Track:**
- Signups per day
- Projects created
- Code generated
- User feedback (surveys)
- NPS score

### Week 2-3: Feedback & Iteration (August 12-25)

**Activities:**
- Daily bug triage
- Weekly feature prioritization
- User interviews (5-10 users)
- Analytics review
- Quick wins implementation

**Expected Feedback Areas:**
- UI/UX improvements
- Missing features
- Template requests
- Bug reports
- Performance issues

### Week 4: Optimization (August 26 - September 2)

**Goals:**
- [ ] Performance optimization
- [ ] Code quality improvements
- [ ] Security hardening
- [ ] Analytics implementation
- [ ] Prepare for public launch

### Exit Criteria

- [ ] 50+ beta users
- [ ] 100+ projects created
- [ ] NPS score > 30
- [ ] No critical bugs
- [ ] Ready for public launch

---

## Phase 3: Launch & Growth (8 weeks)

**Status:** ⏳ Planned  
**Target Start:** September 2, 2026  
**Target Completion:** October 28, 2026  
**Effort:** 10-15 hours/week

### Objectives

- Public launch
- Grow user base to 500+
- Convert free users to paid (10%)
- Build community
- Content marketing

### Week 1-2: Public Launch (September 2-15)

**Launch Activities:**
- [ ] Product Hunt launch (full version)
- [ ] Hacker News post
- [ ] Dev.to article
- [ ] Medium article
- [ ] LinkedIn announcement
- [ ] Email all beta users

**PR Strategy:**
- Press release to tech blogs
- Reach out to AI/ML influencers
- Submit to directories and newsletters

### Week 3-4: Content Marketing (September 16-29)

**Content Creation:**
- [ ] 4 blog posts (technical deep dives)
- [ ] 2 video tutorials (YouTube)
- [ ] 5 Twitter threads (growth hacks)
- [ ] Template showcase series

**Topics:**
- "How to Build Your First MCP Server"
- "MCP Protocol Explained"
- "Integrating Claude with Your API"
- "Best Practices for Tool Design"

### Week 5-6: Community Building (September 30 - October 13)

**Activities:**
- [ ] Create Discord server
- [ ] Weekly office hours
- [ ] Respond to all feedback
- [ ] Feature user-created servers
- [ ] Guest blog posts

### Week 7-8: Monetization Launch (October 14-28)

**Launch Pricing:**
- [ ] Finalize pricing tiers
- [ ] Payment integration (Stripe)
- [ ] Billing portal
- [ ] Pro features
- [ ] Email campaign to free users

**Initial Pricing:**
- Free: 3 projects, basic templates
- Pro ($39/month): Unlimited projects, all templates, priority support
- Team ($149/month): Up to 25 users, team features

### Success Metrics

- 500+ total users
- 50+ paying customers ($2,000+ MRR)
- 20+ blog post views per day
- 500+ Discord members
- 10+ community-contributed templates

---

## Phase 4: Platform Enhancement (12 weeks)

**Status:** ⏳ Planned  
**Target Start:** October 28, 2026  
**Target Completion:** January 20, 2027

### Objectives

- Python code generation
- Resource and Prompt builders
- Cloud deployment (GCP, AWS)
- Template marketplace
- Advanced testing features

### Features (Prioritized)

**P0 (Must Have):**
1. Python code generation
2. Resource builder
3. Prompt builder
4. Cloud Run deployment
5. AWS Lambda deployment

**P1 (Should Have):**
6. Template marketplace
7. Advanced testing (mock data)
8. Team collaboration
9. Version control integration
10. API access

**P2 (Nice to Have):**
11. SSE transport support
12. Multi-agent patterns
13. AI-assisted design
14. Monitoring dashboard
15. Custom domains

### Development Sprints

**Sprint 5: Python Support (3 weeks)**
- Python code generation
- Python templates
- Python-specific testing

**Sprint 6: Resources & Prompts (3 weeks)**
- Resource builder UI
- Prompt builder UI
- Code generation updates

**Sprint 7: Cloud Deployment (3 weeks)**
- GCP Cloud Run integration
- AWS Lambda integration
- Deployment management

**Sprint 8: Marketplace (3 weeks)**
- Template submission flow
- Review and approval
- Rating and search
- Monetization for creators

---

## Phase 5: Enterprise Readiness (16 weeks)

**Status:** ⏳ Planned  
**Target Start:** January 20, 2027  
**Target Completion:** May 12, 2027

### Objectives

- Self-hosted deployment option
- Enterprise authentication (SSO/SAML)
- Advanced security features
- Compliance certifications
- Professional services

### Enterprise Features

1. Self-hosted deployment (Docker Compose / Kubernetes)
2. SSO/SAML authentication
3. Audit logging
4. Role-based access control (RBAC)
5. Custom SLAs
6. Dedicated support
7. SOC 2 compliance
8. GDPR compliance
9. Data residency options
10. Professional services (custom development)

### Target Customers

- Financial institutions
- Healthcare providers
- Government agencies
- Large enterprises (1000+ employees)

### Success Metrics

- 3+ enterprise deals
- $100K+ ARR from enterprise
- SOC 2 Type II certification
- 99.99% SLA achievement

---

## Risk Management

### High-Priority Risks

**Risk 1: Low User Adoption**
- **Probability:** Medium
- **Impact:** Critical
- **Mitigation:** 
  - Strong content marketing
  - Free tier to reduce barrier
  - Focus on UX/DX excellence
  - Active community building

**Risk 2: MCP Protocol Changes**
- **Probability:** Medium
- **Impact:** High
- **Mitigation:**
  - Stay close to Anthropic team
  - Version pinning
  - Migration tools
  - Quick update cycle

**Risk 3: Competition from Anthropic**
- **Probability:** Low-Medium
- **Impact:** Critical
- **Mitigation:**
  - Move fast, build community
  - Differentiate with features
  - Open-source components
  - Pivot if needed (consulting)

**Risk 4: Code Generation Quality Issues**
- **Probability:** Medium
- **Impact:** High
- **Mitigation:**
  - Extensive testing
  - User validation step
  - Quick bug fixes
  - Template versioning

**Risk 5: Security Vulnerabilities**
- **Probability:** Medium
- **Impact:** Critical
- **Mitigation:**
  - Regular security audits
  - Sandbox all user code
  - Bug bounty program
  - Incident response plan

---

## Resource Requirements

### Time Commitment

**Phase 0 (Learning):** 20-25 hours/week × 4 weeks = 80-100 hours  
**Phase 1 (MVP):** 25-30 hours/week × 6-8 weeks = 150-240 hours  
**Phase 2 (Beta):** 15-20 hours/week × 4 weeks = 60-80 hours  
**Phase 3 (Launch):** 10-15 hours/week × 8 weeks = 80-120 hours  

**Total for MVP to Launch:** 370-540 hours (3-6 months part-time)

### Financial Requirements

**Pre-Launch:**
- Domain: $15/year
- GCP credits: $300 free tier
- Vercel: Free tier
- Total: ~$15

**Post-Launch (Monthly):**
- GCP (Cloud Run, SQL, Storage): $50-100
- Vercel Pro: $20
- Domain + Email: $5
- Monitoring (Sentry): $26
- Total: ~$100/month

**Break-even:** 3-5 Pro subscribers

---

## Success Criteria by Phase

### Phase 0: Learning
- ✅ Master MCP protocol
- ✅ Build working prototypes
- ✅ 50+ email signups
- ✅ Validated demand

### Phase 1: MVP
- ✅ Working end-to-end flow
- ✅ 5 templates
- ✅ Documentation complete
- ✅ Deployed to production

### Phase 2: Beta
- ✅ 50+ beta users
- ✅ 100+ projects created
- ✅ NPS > 30
- ✅ No critical bugs

### Phase 3: Launch
- ✅ 500+ users
- ✅ 50+ paying customers
- ✅ $2,000+ MRR
- ✅ Active community

### Phase 4: Platform
- ✅ Python support
- ✅ Cloud deployments
- ✅ Template marketplace
- ✅ 200+ paying customers

### Phase 5: Enterprise
- ✅ Self-hosted option
- ✅ SOC 2 certified
- ✅ 3+ enterprise deals
- ✅ $100K+ ARR

---

## Decision Points

### DP-1: After Phase 0 (June 10, 2026)
**Decision:** Proceed with MVP or pivot?  
**Criteria:**
- Email signups > 50
- Positive survey feedback (80%+)
- Technical feasibility validated
- Personal commitment confirmed

### DP-2: After Phase 1 (August 5, 2026)
**Decision:** Launch beta or continue building?  
**Criteria:**
- MVP feature complete
- No critical bugs
- Confident in code generation quality
- Ready for user feedback

### DP-3: After Phase 2 (September 2, 2026)
**Decision:** Public launch or iterate longer?  
**Criteria:**
- NPS > 30
- Beta users actively using
- Product-market fit signals
- Ready to scale

### DP-4: After Phase 3 (October 28, 2026)
**Decision:** Focus on growth or new features?  
**Criteria:**
- User growth trajectory
- Conversion rate > 8%
- MRR > $2,000
- Feature requests from paying customers

---

## Pivot Scenarios

### Scenario 1: Low User Interest
**If:** < 200 users after 3 months  
**Options:**
- Pivot to consulting (MCP server development services)
- Open-source entire project, build consulting practice
- Niche down (e.g., only for financial services)

### Scenario 2: Anthropic Builds Competing Tool
**If:** Anthropic releases official MCP designer  
**Options:**
- Differentiate with advanced features
- Focus on enterprise/self-hosted market
- Partner with Anthropic as implementation consultants
- Pivot to template marketplace only

### Scenario 3: Strong Demand for Specific Use Case
**If:** One vertical (e.g., database integrations) dominates usage  
**Options:**
- Specialize in that vertical
- Build vertical-specific features
- Marketing focused on that use case

---

## Communication & Reporting

### Weekly Updates (During Active Development)
- Progress on current sprint
- Blockers and decisions needed
- Metrics (signups, usage, revenue)
- Next week's priorities

### Monthly Reviews
- Phase progress vs plan
- Metrics dashboard
- Key learnings
- Adjust roadmap as needed

### Quarterly Planning
- Review OKRs
- Update 3-month roadmap
- Resource allocation
- Strategic decisions

---

## Related Documents

- **CLAUDE.md** - Project overview and architecture
- **SKILLS.md** - Required skills and learning resources
- **MEMORY.md** - Project decisions and rationale
- **PLAN_PHASE.md** - Current phase execution details (Sprint-level)

---

## Changelog

### 2026-05-13
- Initial project roadmap created
- Defined 5 phases (Learning to Enterprise)
- Established success metrics
- Documented decision points

---

**Last Updated:** May 13, 2026  
**Current Phase:** Phase 0 - Learning & Validation  
**Next Milestone:** Complete MCP protocol mastery (May 19, 2026)  
**Overall Status:** 🟢 On Track
