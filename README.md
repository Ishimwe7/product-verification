# Product Verification Service

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker)](https://www.docker.com/)

A robust product management service implementing **Clean Architecture** and **Domain-Driven Design (DDD)**. This service manages product lifecycles using a hybrid database strategy to balance structured data and flexible audit trails.

---

## Architecture Overview

This project strictly adheres to layered architecture principles to ensure business logic remains independent of external tools:

* **API Layer:** FastAPI routers handling request validation and response formatting.
* **Use Case Layer:** Orchestrates workflows (Create, Verify, Get) and acts as the Application Service layer.
* **Domain Layer:** Contains the `Product` entity, state transition guards, and pure verification logic.
* **Infrastructure Layer:** Implementation details for **MySQL** (Core Data), **MongoDB** (Verification Audit), and a Console Event Dispatcher.

## Project Structure
```text
├── src/
│   ├── api/                # FastAPI Routers & Pydantic Schemas
│   ├── domain/             # Core Entities & Business Logic (Requirement #4)
│   ├── application/        # Application Layer
│   │   └── use_cases/      # Application-specific Business Logic (Interactors)
│   ├── infrastructure/     # Repositories (MySQL/MongoDB) & DB Clients
│   └── main.py             # FastAPI Entry Point & Dependency Injection
├── tests/                  # Unit & Integration Tests (Requirement #10)
├── docker-compose.yml      # Infrastructure Orchestration
├── seed.py                 # Initial Data Population Script
├── run.sh                  # Startup Automation Script
└── test.sh                 # Test Execution Script
```

## Getting Started

### 1. Prerequisites
* Docker and Docker Compose
* Python 3.13+ (for running tests outside of Docker)

### 2. Quick Start (Docker)
The easiest way to run the entire stack (App + MySQL + MongoDB) is using the provided automation script:

```bash
bash run.sh
```

### 3. Environment Configuration

*Copy the template to create your environment file:* 
```bash 
cp .env.example .env
```

### 4. Database Seeding
To populate the database with initial test data (categories, sample products, etc.), run the seeding script:

**python seed.py**

### Testing & Quality Assurance
*I utilized pytest for both unit and integration testing. To ensure the src directory is correctly mapped and the Python path is set, use the provided test script:*

# Run Unit and Integration tests
```bash
bash test.sh
```

### Test Coverage Includes:

* **Domain Logic:** Validation of price, stock, and asset requirements (including negative testing).
* **Integration:** Full lifecycle from product creation to hybrid database persistence and retrieval.
* **Edge Cases:** Handling of non-existent products and invalid state transitions. 

### 🔌 API Endpoints

| Method | Endpoint | Description | Status |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/v1/products` | Create a new product (initial state: `pending`) | 201 |
| **POST** | `/api/v1/products/{id}/verify` | Trigger domain verification and transition state | 200 |
| **GET** | `/api/v1/products/{id}` | Retrieve specific product details and status | 200 |
| **GET** | `/api/v1/products` | List all products in the catalog | 200 |
| **GET** | `/api/v1/products/{id}/logs` | Retrieve specific verification failure reasons from **MongoDB** | 200 |
| **GET** | `/api/v1/admin/logs` | **Admin Only:** Fetch all historical verification attempts (Paginated) | 200 |

---

### Admin & Observability

To maintain system integrity and auditability, the logging infrastructure follows these standards:

* **Restricted Access**: The `/api/v1/admin/logs` endpoint is designated for administrative use. In production, this is protected via **Role-Based Access Control (RBAC)** to prevent unauthorized access to the full audit trail.
* **Pagination**: To ensure high performance and low latency, the global logs endpoint is **paginated**. It supports `limit` and `offset` parameters (defaulting to the latest 50 entries) to prevent memory overhead when handling large datasets.
* **Data Persistence**: Verification logs are stored in **MongoDB** as immutable documents. This ensures a permanent audit history that persists even if the primary product record is modified or archived in the MySQL database.

## Business Rules (Requirement #4)

The system automatically transitions product states based on the following criteria:

* **Pass:** Status becomes `active` if all fields are valid.
* **Fail:** Status becomes `rejected` if:
    * Price is $\le 0$ or Stock is $< 0$.
    * Required fields (`Name`, `Category`, `Currency`) are empty or null.
    * Asset list is empty (Total assets $< 1$).
* **Audit Trail:** Detailed failure reasons are stored in **MongoDB** to allow for schema-less, extensible audit logs without affecting core MySQL performance.