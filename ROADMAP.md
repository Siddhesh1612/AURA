# 🗺️ AURA Development Roadmap

> **AURA (AI-Powered Unified Risk & Attack Analysis)** is being developed in iterative phases, with each phase building upon a stable architectural foundation.

---

# Current Status

| Phase | Status |
|--------|--------|
| Phase 1 – Backend Foundation | ✅ Completed |
| Phase 2 – Intelligence Layer | 🚧 Planned |
| Phase 3 – Graph Intelligence | 📋 Planned |
| Phase 4 – Windows Agent | 📋 Planned |
| Phase 5 – Frontend Dashboard | 📋 Planned |
| Phase 6 – Security & Authentication | 📋 Planned |
| Phase 7 – Deployment & Production | 📋 Planned |

---

# ✅ Phase 1 — Backend Foundation (Completed)

The objective of this phase was to establish a clean, scalable, and maintainable backend architecture.

### Configuration
- [x] Centralized application settings
- [x] Environment-based configuration
- [x] Configuration caching

### Logging
- [x] Centralized logging module
- [x] Rotating log files
- [x] Configurable log levels

### Database
- [x] PostgreSQL connection
- [x] SQLAlchemy 2.x integration
- [x] Declarative Base
- [x] Session management

### Domain
- [x] Event enums
- [x] Event ORM model
- [x] Event validation schemas

### Persistence
- [x] Repository Layer
- [x] Service Layer
- [x] Event Receiver API

### Architecture Hardening
- [x] Transaction ownership in Service Layer
- [x] Race-safe duplicate handling
- [x] Centralized API router

---

# 🚧 Phase 2 — Intelligence Layer

The Intelligence Layer transforms raw telemetry into actionable security intelligence.

## Event Correlation Engine

- [ ] Correlation pipeline
- [ ] Correlation rules
- [ ] Correlation identifiers
- [ ] Timeline construction

## Detection Rule Engine

- [ ] Rule evaluation
- [ ] Rule prioritization
- [ ] Custom detection rules
- [ ] Severity mapping

## Risk Assessment Engine

- [ ] Dynamic risk scoring
- [ ] Context-aware risk calculation
- [ ] Asset-aware scoring
- [ ] Identity-aware scoring

## AI Inference Pipeline

- [ ] Feature extraction
- [ ] ML model execution
- [ ] Prediction pipeline
- [ ] Confidence calculation

## Explainable AI

- [ ] SHAP integration
- [ ] Feature importance
- [ ] Analyst explanations
- [ ] Decision transparency

---

# 📋 Phase 3 — Graph Intelligence

## Neo4j Integration

- [ ] Graph database
- [ ] Node projection
- [ ] Relationship projection
- [ ] Graph synchronization

## Attack Graph

- [ ] Attack chains
- [ ] Lateral movement
- [ ] Identity relationships
- [ ] Asset relationships

## Investigation

- [ ] Interactive graph
- [ ] Entity exploration
- [ ] Graph queries
- [ ] Timeline integration

---

# 📋 Phase 4 — Windows Endpoint Agent

## Endpoint Collection

- [ ] Windows Event Logs
- [ ] Sysmon
- [ ] Process monitoring
- [ ] File monitoring
- [ ] Registry monitoring
- [ ] Network monitoring

## Communication

- [ ] Secure enrollment
- [ ] Authentication
- [ ] Compression
- [ ] Encryption
- [ ] Retry logic
- [ ] Offline buffering

---

# 📋 Phase 5 — Frontend Dashboard

## Dashboard

- [ ] Overview
- [ ] Risk dashboard
- [ ] Threat dashboard
- [ ] Event explorer

## Investigation

- [ ] Timeline
- [ ] Search
- [ ] Filtering
- [ ] Graph visualization

## Administration

- [ ] Agents
- [ ] Rules
- [ ] Users
- [ ] Settings

---

# 📋 Phase 6 — Security

## Authentication

- [ ] JWT
- [ ] Refresh Tokens
- [ ] API Keys

## Authorization

- [ ] RBAC
- [ ] Permission system

## Platform Security

- [ ] Rate limiting
- [ ] Request validation
- [ ] Audit logs
- [ ] Security headers

---

# 📋 Phase 7 — Deployment

## Database

- [ ] Alembic migrations
- [ ] Backup strategy
- [ ] Restore strategy

## DevOps

- [ ] Docker
- [ ] Docker Compose
- [ ] GitHub Actions
- [ ] CI/CD

## Monitoring

- [ ] Metrics
- [ ] Health checks
- [ ] Alerting
- [ ] Performance monitoring

## Testing

- [ ] Unit tests
- [ ] Integration tests
- [ ] API tests
- [ ] End-to-end tests

---

# Long-Term Vision

AURA aims to become a comprehensive cybersecurity platform capable of:

- Endpoint Detection & Response (EDR)
- Security Information & Event Management (SIEM)
- AI-assisted Threat Detection
- Graph-based Attack Analysis
- Explainable Machine Learning
- Automated Incident Investigation
- Unified Security Operations

---

# Milestones

| Version | Milestone |
|----------|-----------|
| v0.1.0 | Backend Foundation |
| v0.2.0 | Intelligence Layer |
| v0.3.0 | Graph Intelligence |
| v0.4.0 | Windows Agent |
| v0.5.0 | Frontend Dashboard |
| v0.6.0 | Security & Authentication |
| v1.0.0 | First Stable Release |

---

# Guiding Principles

Throughout development, AURA follows:

- Clean Architecture
- SOLID Principles
- Domain-Driven Design (DDD)
- Security by Design
- Scalability First
- Maintainability
- Explainable AI
- Production Readiness