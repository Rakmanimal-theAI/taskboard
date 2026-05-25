# TaskBoard — Full-Stack Kanban App with LLM-Powered Project Intelligence

![Dashboard Screenshot](screenshots/dashboard.png)

---

## Executive Summary

Modern teams waste hours in status meetings because project state lives in people's heads, not systems. TaskBoard is a production-ready project management platform that gives teams a real-time Kanban view of their work, with an AI layer that generates instant plain-English project summaries from live task data. Built with a full-stack TypeScript and Python architecture, containerised with Docker, and integrated with a local LLM, the app reduces manual reporting overhead and keeps teams focused on shipping.

---

## Business Problem

Small and medium teams struggle with two problems: visibility and communication. Without a centralised task tracking system, work gets lost, priorities blur, and managers spend time chasing status updates instead of unblocking their team. Existing tools like Jira are powerful but heavyweight and expensive. TaskBoard solves this with a lightweight, self-hostable alternative that any team can spin up with a single command, and that uses AI to surface project health without any manual effort.

---

## Methodology

The application follows a REST API architecture with JWT-based authentication, separating concerns cleanly across three layers: a React frontend for user interaction, a FastAPI backend for business logic, and a PostgreSQL database for persistence. The AI summariser uses prompt engineering to format live task data into a structured context window, then queries a local Llama 3.2 model via Ollama to generate a concise status summary, keeping all data on-premise with no external API dependency.

---

## Technical Skills

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript, Tailwind CSS, React Query, Zustand, dnd-kit |
| Backend | Python, FastAPI, SQLAlchemy, Alembic, JWT authentication |
| Database | PostgreSQL, relational schema design, migration management |
| AI | Ollama, Llama 3.2, prompt engineering, local LLM inference |
| DevOps | Docker, Docker Compose, nginx reverse proxy, GitHub Actions |
| Testing | pytest, integration testing, test fixtures, TestClient |

Notable implementation details: dependency injection for database sessions, Pydantic v2 schema validation, Alembic migration versioning, axios interceptors for automatic token refresh, and drag-and-drop state reconciliation with optimistic backend updates.

---

## Results and Recommendations

![Kanban Board Screenshot](screenshots/kanban.png)

The platform delivers three core capabilities that directly reduce operational overhead:

One-command deployment via Docker Compose eliminates environment setup friction, making it viable for any team regardless of technical background. The Kanban board with drag-and-drop status updates gives teams a real-time view of work in progress, replacing ad-hoc communication. The LLM summariser generates a project health report in under 10 seconds from live data, replacing manual status updates entirely.

For teams adopting this tool, the recommended next step is integrating it with existing communication tools like Slack to push automated daily summaries, closing the loop between task state and team awareness.

---

## Next Steps and Limitations

**Next steps:**
- GitHub Actions CI/CD pipeline for automated testing and deployment to AWS
- Deploy to AWS EC2 with RDS for a fully cloud-hosted production environment
- Slack or email integration for automated daily project summaries
- Role-based access control so multiple team members can collaborate on the same project
- Mobile-responsive design improvements for on-the-go task management

**Limitations:**
- The LLM summariser currently runs locally via Ollama, meaning it requires the host machine to have sufficient RAM to run Llama 3.2. A cloud-hosted model endpoint would remove this constraint in production
- Authentication is single-user per project, collaborative multi-user workflows are not yet supported
- There is no activity log or audit trail, which limits accountability in team environments

---

## Local Setup

```bash
git clone https://github.com/Rakmanimal-theAI/taskboard
cd taskboard
docker-compose up --build
```

App runs at `http://localhost`. Backend API docs at `http://localhost:8000/docs`.

**Demo credentials:**
Email: demo@taskboard.com
Password: demo1234

---

## Live Demo

[Live URL] | [GitHub Repository](https://github.com/Rakmanimal-theAI/taskboard) | [Demo Video](#)
