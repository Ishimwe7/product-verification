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

# Product Verification Service

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker)](https://www.docker.com/)

A robust product management service implementing **Clean Architecture** and **Domain-Driven Design (DDD)**. This service manages product lifecycles using a hybrid database strategy to balance structured data and flexible audit trails.

---
```text
## Project Structure

├── src/
│   ├── api/             # FastAPI Routers & Schemas
│   ├── domain/          # Entities & Business Logic
│   ├── use_cases/       # Application Logic (Interactors)
│   ├── infrastructure/  # Database Repositories & Clients
│   └── main.py          # App Entry Point
├── tests/               # Unit & Integration Tests
├── docker-compose.yml   # Infrastructure Orchestration
├── run.sh               # Startup Automation
└── test.sh              # Test Automation
---
```
## Getting Started

### 1. Prerequisites
* Docker and Docker Compose
* Python 3.13+ (for running tests outside of Docker)

### 2. Quick Start (Docker)
The easiest way to run the entire stack (App + MySQL + MongoDB) is using the provided automation script:

# Setup environment, start databases, and run the server
bash run.sh

### 3. Environment Configuration

*Copy the template to create your environment file:*  
cp .env.example .env

### 4. Database Seeding
To populate the database with initial test data (categories, sample products, etc.), run the seeding script:

**python seed.py**

### Testing & Quality Assurance
*I utilized pytest for both unit and integration testing. To ensure the src directory is correctly mapped and the Python path is set, use the provided test script:*

# Run Unit and Integration tests
bash test.sh


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


---

## Business Rules (Requirement #4)

The system automatically transitions product states based on the following criteria:

* **Pass:** Status becomes `active` if all fields are valid.
* **Fail:** Status becomes `rejected` if:
    * Price is $\le 0$ or Stock is $< 0$.
    * Required fields (`Name`, `Category`, `Currency`) are empty or null.
    * Asset list is empty (Total assets $< 1$).
* **Audit Trail:** Detailed failure reasons are stored in **MongoDB** to allow for schema-less, extensible audit logs without affecting core MySQL performance.