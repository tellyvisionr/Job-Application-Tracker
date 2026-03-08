# API Test Suite

Tests cover all five CRUD endpoints using an in-memory SQLite database. No running services are required.

## Running the Tests

```bash
cd api
pytest tests/ -v
```

---

## Test Cases

### POST /applications/ — Create

| Test | Description | Expected |
|---|---|---|
| `test_create_application` | Submit a fully populated application | `201` with all fields returned including auto-generated `id` |
| `test_create_application_defaults` | Submit only required fields | `201` with `status` defaulting to `"Applied"`, optional fields `null` |
| `test_create_application_missing_required_fields` | Omit `role` and `date_applied` | `422 Unprocessable Entity` |

---

### GET /applications/ — List All

| Test | Description | Expected |
|---|---|---|
| `test_get_all_applications_empty` | Request before any data exists | `200` with empty array |
| `test_get_all_applications` | Request after creating two applications | `200` with array of two records |

---

### GET /applications/{id} — Get One

| Test | Description | Expected |
|---|---|---|
| `test_get_application_by_id` | Request a valid application by ID | `200` with correct record |
| `test_get_application_not_found` | Request a non-existent ID (999) | `404` with `"Application not found"` |

---

### PUT /applications/{id} — Update

| Test | Description | Expected |
|---|---|---|
| `test_update_application_status` | Update `status` field only | `200` with updated status; all other fields unchanged |
| `test_update_application_notes` | Update `notes` field only | `200` with updated notes |
| `test_update_application_not_found` | Update a non-existent ID (999) | `404` with `"Application not found"` |

---

### DELETE /applications/{id} — Delete

| Test | Description | Expected |
|---|---|---|
| `test_delete_application` | Delete an existing application | `204`; subsequent GET returns `404` |
| `test_delete_application_not_found` | Delete a non-existent ID (999) | `404` with `"Application not found"` |

---

## Setup

Each test runs against a fresh database. The `reset_db` fixture creates all tables before each test and drops them after, ensuring full isolation between test cases.

The `get_db` FastAPI dependency is overridden to use SQLite instead of PostgreSQL, so tests run without any external services.
