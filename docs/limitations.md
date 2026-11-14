# Platform Limitations & Architectural Boundaries

## 1. Application-Level Boundaries
- **OrangeHRM Open Source Edition vs Enterprise**:
  - The Open Source Starter edition hosted at `opensource-demo.orangehrmlive.com` is a subset of OrangeHRM's commercial enterprise platform.
  - Multi-tier hierarchical approval chains, matrix organization charts, and SAML/SSO integrations are enterprise-only features and are excluded from this open-source test suite.
- **REST API Direct Endpoints**:
  - The hosted demo has closed API documentation and restricts direct token-based API invocations. The framework interacts via W3C WebDriver directly through the browser.

## 2. Environment Constraints
- **Public Hosted Demo Volatility**:
  - Periodic database refreshes occur without warning.
  - Network latency varies based on global shared load.
  - Rate limiting applies to concurrent brute-force logins.
- **Destructive Test Policy**:
  - Deleting existing baseline demo records (e.g. standard admin, pre-seeded departments, default employees) is strictly prohibited to maintain environment health for other users.
  - High-concurrency write tests (more than 2 concurrent workers) should be directed to self-hosted instances.

## 3. Automation Framework Scope
- **Primary Technology**: Python 3.12, Selenium WebDriver 4, and pytest.
- **Playwright / TypeScript Evaluation**: Playwright was evaluated during architectural spikes. Because Selenium 4 with Selenium Manager fulfills 100% of browser automation requirements with zero external driver overhead, introducing a secondary TypeScript codebase would introduce needless tech-stack duplication without demonstrable value (ADR-001).
