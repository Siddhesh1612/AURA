# 🛡️ AURA
### AI-Powered Unified Risk & Attack Analysis Platform

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791?logo=postgresql)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Under%20Development-orange)

</p>

---

# Overview

AURA (AI-Powered Unified Risk & Attack Analysis) is an enterprise cybersecurity platform designed to collect, normalize, correlate, analyze, and visualize security telemetry from endpoints and external security sources.

Unlike traditional monitoring tools that only display events, AURA focuses on understanding relationships between events, identifying attack chains, calculating contextual risk, and assisting analysts with AI-driven explanations.

The long-term vision is to provide a unified security analysis platform capable of handling endpoint telemetry, SIEM integrations, graph analytics, machine learning inference, and intelligent incident investigation from a single interface.

---

# Vision

Modern security teams receive thousands of alerts every day.

Most are isolated events with little context.

AURA aims to transform raw telemetry into actionable intelligence by combining:

- Event Correlation
- Rule-Based Detection
- AI Risk Assessment
- Explainable Machine Learning
- Graph-Based Attack Visualization
- Unified Security Dashboard

---

# Current Phase

## ✅ Phase 1 — Backend Foundation (Completed)

The backend architecture has been completed with enterprise software engineering practices.

Implemented:

- Configuration Management
- Centralized Logging
- PostgreSQL Integration
- SQLAlchemy ORM
- Database Session Management
- Event Domain Model
- Event Validation Schemas
- Repository Layer
- Service Layer
- Event Receiver API
- Transaction Management
- Race-Safe Duplicate Detection
- Dependency Injection
- Clean Architecture

---

# Planned Features

## Intelligence Layer

- Event Correlation Engine
- Rule Engine
- Risk Assessment Engine
- Explainable AI
- SHAP Integration
- Attack Chain Detection

---

## Graph Intelligence

- Neo4j Integration
- Graph Projection
- Entity Relationships
- Interactive Investigation Graphs

---

## Windows Agent

- Endpoint Telemetry Collection
- Secure Device Enrollment
- Process Monitoring
- Network Activity Monitoring
- File Activity Monitoring
- Scheduled Reporting

---

## Dashboard

- Real-Time Events
- Risk Dashboard
- Timeline View
- Threat Analytics
- Search & Filtering
- Incident Management

---

# Architecture

```
                    Windows Agent
                          │
                          ▼
                 Event Receiver API
                          │
                          ▼
                   Event Service
                          │
                          ▼
                 Event Repository
                          │
                          ▼
                    PostgreSQL
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
  Correlation Engine               Rule Engine
          │                               │
          └───────────────┬───────────────┘
                          ▼
                Risk Assessment Engine
                          │
                          ▼
                 AI Inference Pipeline
                          │
                          ▼
                  Neo4j Graph Engine
                          │
                          ▼
                  React Dashboard
```

---

# Technology Stack

## Backend

- Python
- FastAPI
- SQLAlchemy 2.x
- Pydantic v2
- PostgreSQL

## Frontend

- React
- Vite
- TypeScript
- Tailwind CSS

## AI & Machine Learning

- Scikit-learn
- SHAP
- XGBoost
- LightGBM
- PyTorch (Planned)

## Graph Intelligence

- Neo4j

## DevOps

- Docker
- GitHub Actions
- Alembic (Planned)

---

# Project Structure

```
AURA/

backend/
frontend/
agent/
datasets/
docs/
scripts/
shared/
tests/

README.md
ROADMAP.md
SECURITY.md
LICENSE
docker-compose.yml
```

---

# Backend Architecture

The backend follows a layered architecture.

```
API
        │
        ▼
Service
        │
        ▼
Repository
        │
        ▼
Database
```

Responsibilities are clearly separated:

- API → HTTP only
- Service → Business Logic
- Repository → Database Persistence
- Models → Domain
- Schemas → Validation

---

# Design Principles

- Clean Architecture
- SOLID Principles
- Dependency Injection
- Repository Pattern
- Domain-Driven Design (DDD)
- Separation of Concerns

---

# Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/AURA.git
```

Move into the project

```bash
cd AURA
```

Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
uvicorn app.main:app --reload
```

Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# API

Current endpoints

```
POST /api/v1/events
```

Future endpoints

```
GET /events
GET /alerts
GET /incidents
GET /analytics
POST /agents
```

---

# Development Status

| Module | Status |
|---------|--------|
| Backend Foundation | ✅ Complete |
| Intelligence Layer | 🚧 Planned |
| Windows Agent | 🚧 Planned |
| Neo4j | 🚧 Planned |
| Dashboard | 🚧 Planned |
| Authentication | 🚧 Planned |
| Deployment | 🚧 Planned |

---

# Documentation

Additional documentation is available inside the `docs/` directory.

Future documents include:

- Architecture
- API Reference
- Database Design
- Development Guide
- Deployment Guide

---

# Contributing

Contributions, suggestions, and discussions are welcome.

Please open an issue before submitting major changes.

---

# License

This project is licensed under the MIT License.

See the LICENSE file for details.

---

# Author

**Siddhesh Ratnaparkhi**

Diploma in Artificial Intelligence & Machine Learning

Government Polytechnic, Nagpur

---

# Project Status

🚧 Active Development

Phase 1 has been completed successfully.

The project is now preparing for Phase 2 — Intelligence Layer.