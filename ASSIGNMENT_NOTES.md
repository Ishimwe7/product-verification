# Assignment Notes - Product Verification Service

## Architecture Choices
- **Clean Architecture:** Organized into API, Use Case, Domain, and Infrastructure layers to ensure the business logic is independent of the database and framework.
- **Dependency Injection:** Used FastAPI's `Depends` to inject repositories and event dispatchers, making the system highly testable.
- **Domain-Driven Design (DDD):** The `Product` entity contains the logic for its own state transitions (`pending` -> `active`/`rejected`).

## MySQL vs MongoDB: Intentional Use
- **MySQL (Core Data):** Used for the `products` table. MySQL provides ACID compliance, which is essential for managing product catalogs and financial data (price/stock).
- **MongoDB (Audit/Checklist):** Used to store verification results. Since verification checks might change (e.g., adding new rules), MongoDB's schema-less nature allows us to store varying checklist results and failure reasons without migrating the main database.

## Assumptions & Tradeoffs
- **Dummy Dispatcher:** Implemented a console-logger for events as per requirements. In production, this would be replaced with a RabbitMQ or Amazon SNS implementation.
- **UnitOfWork:** For this task, the Use Case orchestrates the saving to both databases. In a larger system, a formal Unit of Work pattern would be used to ensure atomicity across MySQL and MongoDB.