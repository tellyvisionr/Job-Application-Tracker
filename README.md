# Job Application Tracker

A full-stack web application for tracking job applications through every stage of the hiring process. Built with a FastAPI REST API, TypeScript frontend, and containerized with Docker for consistent local development and cloud deployment.

---

## Features

- Create, view, update, and delete job applications
- Track pipeline stage per application — Applied, Phone Screen, Interview, Offer, Rejected
- Store compensation range, application date, and free-form notes
- RESTful API with automatic documentation via Swagger UI

## Tech Stack

| Layer | Technology |
|---|---|
| API | Python, FastAPI, SQLAlchemy |
| Database | PostgreSQL |
| Frontend | TypeScript, Vite |
| Containerization | Docker |
| Cloud Hosting | AWS (planned) |

## Project Structure

```
Job-Application-Tracker/
├── docker-compose.yml
├── api/                  # FastAPI backend
│   ├── Dockerfile
│   ├── main.py           # App entry point & route definitions
│   ├── models.py         # SQLAlchemy ORM model
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── database.py       # Database connection & session management
│   └── requirements.txt
└── client/               # TypeScript frontend
    ├── Dockerfile
    ├── src/
    │   └── main.ts       # API calls & UI logic
    ├── index.html
    └── package.json
```

## Getting Started

### Prerequisites

- Docker

### Run

```bash
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend | `http://localhost:5173` |
| API | `http://localhost:8000` |
| API Docs | `http://localhost:8000/docs` |

To stop all services:

```bash
docker compose down
```

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/applications/` | Create a new application |
| `GET` | `/applications/` | List all applications |
| `GET` | `/applications/{id}` | Get a single application |
| `PUT` | `/applications/{id}` | Update an application |
| `DELETE` | `/applications/{id}` | Delete an application |

## Deployment

This project is planned for deployment on **AWS** using the following services:

| Service | Purpose |
|---|---|
| ECS (Fargate) | Run containerized API |
| RDS (PostgreSQL) | Managed database |
| S3 + CloudFront | Host and serve the frontend |
| ECR | Store Docker images |
