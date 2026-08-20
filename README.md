# FastAPI Test Automation

[![Test Backend](../../actions/workflows/test-backend.yml/badge.svg)](../../actions/workflows/test-backend.yml)
[![Playwright Tests](../../actions/workflows/playwright.yml/badge.svg)](../../actions/workflows/playwright.yml)

A full-stack test automation practice project based on **FastAPI, React and PostgreSQL**.

The project focuses on building and extending a complete software testing workflow, including:

- API automated testing with Pytest
- JWT authentication testing
- Boundary value and negative scenario testing
- Data-driven testing with parameterization
- Code coverage analysis
- Playwright end-to-end testing
- Docker-based test environment
- GitHub Actions continuous integration
- Coverage quality gate
- Cross-platform issue analysis and regression testing

> This repository is adapted from the open-source **Full Stack FastAPI Template**.  
> The main work in this repository focuses on test automation engineering, test case extension, E2E testing, CI integration and issue analysis rather than claiming the original business system as a from-scratch implementation.

---

## 1. Project Overview

The application is a full-stack management system with:

- FastAPI backend
- React + TypeScript frontend
- PostgreSQL database
- JWT-based authentication
- Items CRUD functionality
- User management
- Password recovery
- Docker Compose environment

Based on this system, a complete automated testing workflow was built and extended.

The overall testing architecture is:

```text
                    GitHub Push / Pull Request
                              │
                              ▼
                      GitHub Actions CI
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          Backend Test Pipeline      Playwright Pipeline
                 │                         │
                 ▼                         ▼
             PostgreSQL              Browser Automation
                 │                         │
                 ▼                         ▼
               Pytest                 React Frontend
                 │                         │
                 ▼                         ▼
            FastAPI APIs              FastAPI APIs
                 │                         │
                 ▼                         ▼
             Coverage                  PostgreSQL
                 │
                 ▼
       Coverage Quality Gate
             >= 90%
```

---

## 2. Technology Stack

### Application

- Python
- FastAPI
- SQLModel
- PostgreSQL
- React
- TypeScript
- Vite
- JWT

### Testing

- Pytest
- FastAPI TestClient
- Coverage.py
- Playwright
- Chromium
- Docker Compose

### CI

- GitHub Actions
- Automated regression testing
- Coverage quality gate
- Playwright HTML reports

---

## 3. API Automation Testing

Backend automated tests are implemented with **Pytest + FastAPI TestClient**.

The API test suite covers:

- User login
- JWT token generation
- JWT authentication
- Invalid credentials
- User management
- Items CRUD
- Permission validation
- Resource-not-found scenarios
- Invalid token scenarios
- Input validation
- Boundary value testing

Example test workflow:

```text
Prepare Test Data
        │
        ▼
Send HTTP Request
        │
        ▼
Receive Response
        │
        ▼
Validate Status Code
        │
        ▼
Validate Response Body
        │
        ▼
PASS / FAIL
```

---

## 4. Custom API Test Cases

Additional API automation cases were added in:

```text
backend/tests/api/routes/test_items_extended.py
```

These tests focus on scenarios beyond the basic CRUD happy path.

### Boundary value testing

The following scenarios are covered:

```text
Empty title
Title length > maximum
Description length > maximum
Maximum valid title length
```

Example:

```python
@pytest.mark.parametrize(
    "payload",
    [
        {"title": "", "description": "normal"},
        {"title": "a" * 256, "description": "normal"},
        {"title": "normal", "description": "a" * 256},
    ],
)
def test_create_item_invalid_boundary(
    client,
    superuser_token_headers,
    payload,
):
    response = client.post(
        "/api/v1/items/",
        headers=superuser_token_headers,
        json=payload,
    )

    assert response.status_code == 422
```

This test uses:

```text
pytest.mark.parametrize
```

to implement **data-driven testing**, allowing multiple input combinations to reuse the same test logic.

---

## 5. JWT Authentication Testing

Authentication-related cases cover both valid and invalid token scenarios.

Example invalid token scenario:

```python
def test_read_items_with_invalid_token(client):
    headers = {
        "Authorization": "Bearer invalid-token"
    }

    response = client.get(
        "/api/v1/items/",
        headers=headers,
    )

    assert response.status_code == 403
```

The test validates that protected resources cannot be accessed with an invalid JWT.

Authentication testing includes:

```text
Valid credentials
      ↓
Generate JWT
      ↓
Access protected API
      ↓
200 OK
```

and:

```text
Invalid JWT
      ↓
Access protected API
      ↓
403 Forbidden
```

---

## 6. Test Fixtures

Reusable test dependencies are managed with Pytest fixtures.

Examples include:

```text
client
db
superuser_token_headers
normal_user_token_headers
```

They provide reusable resources such as:

```text
FastAPI TestClient
Database Session
Authenticated User Headers
Superuser Authentication
```

This reduces duplicated setup logic across test cases.

---

## 7. Code Coverage

Backend code coverage is measured with **Coverage.py**.

Run locally:

```bash
cd backend

uv run coverage erase
uv run coverage run -m pytest
uv run coverage report -m
```

Generate HTML coverage report:

```bash
uv run coverage html
```

The generated report is located at:

```text
backend/htmlcov/index.html
```

Coverage reports help identify:

```text
Executed code
Missed code
Untested exception branches
Untested permission branches
```

This allows test cases to be added based on uncovered business logic instead of only increasing the number of test cases.

---

## 8. Coverage Quality Gate

The backend GitHub Actions pipeline contains a coverage quality gate:

```bash
coverage report --fail-under=90
```

The rule is:

```text
Coverage >= 90%
        │
        ▼
      PASS
```

```text
Coverage < 90%
        │
        ▼
     CI FAIL
```

This prevents code changes with insufficient test coverage from silently passing the CI pipeline.

---

## 9. Playwright E2E Testing

Frontend end-to-end tests are implemented with **Playwright**.

The Playwright suite covers scenarios including:

- Login page validation
- Valid login
- Invalid email
- Invalid password
- Logout
- Protected route access
- Item creation
- Item editing
- Item deletion
- Empty state validation

Playwright simulates actual browser behavior:

```text
Open Browser
      ↓
Open Web Page
      ↓
Locate Element
      ↓
Input Data
      ↓
Click Button
      ↓
Wait for Result
      ↓
Assert UI State
```

---

## 10. Custom End-to-End Business Flow

A custom E2E test was added in:

```text
frontend/tests/items_business_flow.spec.ts
```

It tests a complete business flow:

```text
Authenticated User
        ↓
Open Items Page
        ↓
Create Item
        ↓
Verify Item Appears
        ↓
Open Item Menu
        ↓
Delete Item
        ↓
Verify Item Disappears
```

Example:

```typescript
test("Create and delete item end-to-end", async ({ page }) => {
  const title = `E2E Item ${Date.now()}`
  const description = "Created by Playwright E2E test"

  await page.goto("/items")

  await page
    .getByRole("button", { name: "Add Item" })
    .click()

  await page
    .getByLabel("Title")
    .fill(title)

  await page
    .getByLabel("Description")
    .fill(description)

  await page
    .getByRole("button", { name: "Save" })
    .click()

  await expect(
    page.getByText("Item created successfully")
  ).toBeVisible()

  const itemRow = page
    .getByRole("row")
    .filter({ hasText: title })

  await expect(itemRow).toBeVisible()

  await itemRow
    .getByRole("button")
    .last()
    .click()

  await page
    .getByRole("menuitem", { name: "Delete Item" })
    .click()

  await page
    .getByRole("button", { name: "Delete" })
    .click()

  await expect(
    page.getByRole("row").filter({ hasText: title })
  ).not.toBeVisible()
})
```

A timestamp is used in the item title:

```typescript
Date.now()
```

to reduce conflicts between repeated E2E executions.

---

## 11. Playwright Locators

The test suite prioritizes semantic locators such as:

```typescript
page.getByRole()
page.getByLabel()
page.getByTestId()
```

instead of relying heavily on fragile XPath expressions.

For example:

```typescript
page.getByRole("button", {
  name: "Add Item",
})
```

This improves:

- Readability
- Maintainability
- UI test stability

---

## 12. Authentication State Reuse

Playwright authentication setup stores authenticated browser state in:

```text
playwright/.auth/user.json
```

The authentication process is executed before dependent Chromium tests.

This avoids performing repeated login operations in every E2E test.

Workflow:

```text
Login once
    ↓
Save browser authentication state
    ↓
Reuse authentication state
    ↓
Execute E2E test cases
```

---

## 13. CI Pipeline

GitHub Actions is used to automatically execute regression tests after code changes.

### Backend CI

The backend pipeline performs:

```text
Checkout Code
      ↓
Set Up Python
      ↓
Install uv
      ↓
Start PostgreSQL
      ↓
Database Migration
      ↓
Run Pytest
      ↓
Generate Coverage
      ↓
Upload Coverage Report
      ↓
Check 90% Coverage Gate
```

### Playwright CI

The Playwright pipeline performs:

```text
Checkout Code
      ↓
Install Bun
      ↓
Install Python / uv
      ↓
Install Dependencies
      ↓
Build Docker Environment
      ↓
Initialize Database
      ↓
Run Playwright E2E Tests
      ↓
Generate Test Reports
      ↓
Upload HTML Report
```

The CI pipelines run automatically after pushes to:

```text
main
```

and can also be triggered for pull requests.

---

## 14. Issue Found During Regression Testing

During full backend regression testing on Windows, two email-related test cases failed.

The error was:

```text
UnicodeDecodeError:
'gbk' codec can't decode byte ...
```

Affected scenarios included:

```text
Password recovery email
New user email
```

### Root Cause

Email HTML templates were loaded with:

```python
Path(...).read_text()
```

without explicitly specifying the encoding.

On Windows, Python attempted to use the system default encoding, resulting in a decoding error when reading UTF-8 HTML templates.

### Fix

The implementation was changed to:

```python
Path(...).read_text(encoding="utf-8")
```

### Verification

After the fix:

```text
Previously failed tests
        ↓
Targeted regression
        ↓
PASS
        ↓
Full regression suite
        ↓
PASS
```

This issue demonstrates a complete testing and debugging workflow:

```text
Run Regression Tests
        ↓
Find Failed Cases
        ↓
Analyze Stack Trace
        ↓
Locate Common Failure Point
        ↓
Identify Encoding Issue
        ↓
Fix Source Code
        ↓
Run Targeted Regression
        ↓
Run Full Regression
```

---

## 15. Local Environment

Recommended tools:

```text
Docker Desktop
Python / uv
Bun
Chromium
Git
```

---

## 16. Start Database Services

From the project root:

```bash
docker compose up -d db mailcatcher
```

Check container status:

```bash
docker compose ps
```

---

## 17. Start Backend

Open a terminal:

```bash
cd backend
```

Install dependencies:

```bash
uv sync
```

Initialize database:

```bash
uv run python app/backend_pre_start.py
uv run alembic upgrade head
uv run python app/initial_data.py
```

Start FastAPI:

```bash
uv run fastapi dev
```

Backend API:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

---

## 18. Start Frontend

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
bun install
```

Start Vite:

```bash
bun run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 19. Run Backend Tests

From:

```text
backend/
```

run:

```bash
uv run pytest -v
```

Run one test file:

```bash
uv run pytest tests/api/routes/test_items_extended.py -v
```

Run one test case:

```bash
uv run pytest tests/api/routes/test_login.py::test_get_access_token -v
```

---

## 20. Run Coverage

```bash
uv run coverage erase
uv run coverage run -m pytest
uv run coverage report -m
```

HTML report:

```bash
uv run coverage html
```

---

## 21. Run Playwright Tests

From:

```text
frontend/
```

install Chromium if needed:

```bash
bunx playwright install chromium
```

Run all tests:

```bash
bunx playwright test
```

Run login tests:

```bash
bunx playwright test tests/login.spec.ts --project=chromium
```

Run tests with visible browser:

```bash
bunx playwright test --project=chromium --headed
```

Run the custom business flow:

```bash
bunx playwright test tests/items_business_flow.spec.ts --project=chromium
```

Open Playwright report:

```bash
bunx playwright show-report
```

---

## 22. Project Structure

The main testing-related files are:

```text
fastapi-test-automation
│
├── backend
│   ├── app
│   │   ├── api
│   │   ├── core
│   │   └── utils.py
│   │
│   └── tests
│       ├── api
│       │   └── routes
│       │       ├── test_login.py
│       │       ├── test_users.py
│       │       ├── test_items.py
│       │       └── test_items_extended.py
│       │
│       ├── crud
│       └── conftest.py
│
├── frontend
│   ├── tests
│   │   ├── auth.setup.ts
│   │   ├── login.spec.ts
│   │   ├── items.spec.ts
│   │   └── items_business_flow.spec.ts
│   │
│   └── playwright.config.ts
│
├── .github
│   └── workflows
│       ├── test-backend.yml
│       ├── playwright.yml
│       └── test-docker-compose.yml
│
├── compose.yml
└── README.md
```

---

## 23. Testing Strategy

The project applies multiple test design techniques.

### Equivalence Partitioning

Examples:

```text
Valid credentials
Invalid credentials
```

### Boundary Value Analysis

Examples:

```text
title = ""
title length = maximum
title length > maximum
```

### Negative Testing

Examples:

```text
Incorrect password
Non-existent user
Invalid JWT
Missing resource
Unauthorized resource access
```

### Data-Driven Testing

Implemented using:

```python
@pytest.mark.parametrize
```

### End-to-End Testing

Implemented using Playwright to validate complete user business flows through the browser.

---

## 24. Engineering Highlights

The main test engineering work demonstrated in this repository includes:

- Built and extended REST API automation using Pytest
- Designed positive, negative and boundary test scenarios
- Applied Pytest parameterization for data-driven testing
- Tested JWT authentication and protected resources
- Used reusable fixtures to manage test dependencies
- Analyzed backend code coverage with Coverage.py
- Applied a 90% coverage quality gate in CI
- Built Playwright browser-based E2E tests
- Implemented a complete Item create-and-delete business flow
- Reused Playwright authentication state to reduce repeated login operations
- Integrated backend and E2E testing with GitHub Actions
- Used Docker Compose to provide reproducible database and test services
- Diagnosed a Windows GBK / UTF-8 compatibility issue through regression testing
- Performed targeted regression before full regression verification

---

## 25. What I Learned

This project was used to practice a complete test development workflow:

```text
Understand Business APIs
        ↓
Manual API Verification
        ↓
Design Test Cases
        ↓
Pytest API Automation
        ↓
Fixture Reuse
        ↓
Boundary / Negative Testing
        ↓
Coverage Analysis
        ↓
Playwright E2E
        ↓
CI Integration
        ↓
Regression Testing
        ↓
Failure Analysis
        ↓
Bug Fix Verification
```

Rather than only learning individual testing tools, the goal is to understand how automated testing fits into an actual software engineering workflow.

---

## 26. Project Origin

This repository is based on the open-source **Full Stack FastAPI Template**.

The original template provides the application foundation, including:

```text
FastAPI
React
PostgreSQL
Docker Compose
JWT Authentication
Basic Pytest Tests
Basic Playwright Tests
GitHub Actions
```

The purpose of this repository is to practice and demonstrate test development work on top of a realistic full-stack application.

The customized testing work includes:

```text
Extended API test scenarios
Boundary value testing
Invalid JWT testing
Pytest parameterization
Custom Playwright E2E business flow
Coverage verification
CI adaptation
Windows encoding bug analysis and fix
Regression testing
```

---

## 27. License

This project follows the license of the original Full Stack FastAPI Template.

See:

```text
LICENSE
```

for details.