# ADR-002: Test Data Management, Namespacing, and Environment Strategy

## Status
Accepted

## Context
Automating against a shared environment (such as the OrangeHRM Open Source Demo) presents serious test reliability and data isolation challenges:
1. Other users and automated runs access the same instance concurrently.
2. Hardcoded test data (e.g., creating an employee named "John Doe" or username "johndoe") causes duplicate record collisions.
3. Deleting pre-existing shared records damages demo integrity for other users and violates the OrangeHRM usage policy.
4. Parallel execution (`pytest-xdist`) running against the same database causes race conditions if worker data overlaps.

## Decision
1. **Dynamic Synthetic Data Factories**: Use `Faker` combined with unique test run identifiers and execution worker IDs (`pytest-xdist` worker ID + UUID + timestamp) to guarantee zero collisions.
   - Example employee format: First name `Aut_W1_7b4c`, Last name `Doe_8932`.
2. **Dual-Environment Strategy**:
   - **Public Demo Target**: Restricted to non-destructive workflows (smoke tests, creation of strictly namespaced records, verification of read flows, self-contained record progression). Destructive actions on existing shared records and high-concurrency stress tests are strictly prohibited.
   - **Self-Hosted / Local Target**: Full unconstrained regression, role-based authorization testing, destructive cleanup, and higher worker concurrency (`-n 4`).
3. **Strict Data Ownership**: Automated tests track every entity created during their execution scope and only clean up entities specifically registered to that test session.

## Consequences
- **Positive**: Complete test independence, deterministic parallel runs, no accidental overwriting of shared records, compliance with ethical testing guidelines.
- **Trade-offs**: Test assertions cannot rely on pre-existing database records; tests must create their own prerequisites or perform dynamic search queries.
