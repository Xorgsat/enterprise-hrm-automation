# ADR-001: Primary Automation Stack Selection

## Status
Accepted

## Context
The Enterprise Human Resource Management (HRM) Quality Engineering Platform requires a scalable, maintainable, and observable end-to-end automation foundation. The target application is OrangeHRM Open Source (hosted demo and self-hosted environments). 

We need to choose between:
1. Python 3.12 + Selenium WebDriver 4 + pytest
2. TypeScript + Playwright
3. Hybrid multi-language repository

## Decision
We select **Python 3.12 + Selenium WebDriver 4 (with Selenium Manager) + pytest** as the primary automation stack.

### Key Justifications
1. **Industry Standard Enterprise Reliability**: Selenium 4 with W3C WebDriver specification provides native browser control without needing separate external driver binaries thanks to built-in Selenium Manager.
2. **pytest Ecosystem**: pytest provides unmatched test lifecycle fixtures, dependency injection, parameterized execution, granular marker-based test selection (`smoke`, `regression`, `negative`), and seamless parallel execution via `pytest-xdist`.
3. **Data Engineering Integration**: Python's data manipulation and synthetic data generation libraries (such as `Faker` and `Pydantic`) enable sophisticated factory patterns with worker-isolated namespaces.
4. **Unified Diagnostic & Reporting Pipeline**: Python's native `logging` module combined with `allure-pytest` and JUnit XML reporting produces structured, actionable failure diagnostics.
5. **No Architectural Splitting**: TypeScript + Playwright is kept as an optional future complementary inspection tool rather than creating split-stack duplication. The Python framework is completely self-contained.

## Consequences
- **Positive**: Single runtime, reproducible environment via `pyproject.toml` / `requirements.txt`, clean CI pipeline in GitHub Actions, zero dependency on Node.js runtime for the primary test suite.
- **Negative / Trade-offs**: Selenium requires disciplined explicit synchronization for dynamic single-page application (SPA) states compared to Playwright's auto-waiting. This is solved architecturally via a centralized `WaitManager` and custom expected conditions.
