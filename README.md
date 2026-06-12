# Practice - Reqres API With Pytest

Practice project for API testing with Pytest and Requests using Reqres.

Reqres currently requires an `x-api-key` header in requests. For that reason, live tests are automatically skipped when the `REQRES_API_KEY` environment variable is not configured.

Official documentation: https://reqres.in/docs

## Goal

Practice automated testing against a REST API:

- status code validation;
- JSON payload validation;
- header validation;
- positive and negative test cases;
- fixtures for HTTP client and configuration;
- markers to filter test suites;
- separation between client, schemas, and tests.

## Structure

```text
clients/
  reqres_client.py
schemas/
  product_schema.py
tests/
  conftest.py
  test_products.py
  test_reqres_config.py
pyproject.toml
requirements.txt
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure API Key

PowerShell:

```powershell
$env:REQRES_API_KEY="your_api_key"
```

You can also configure the Reqres environment:

```powershell
$env:REQRES_ENV="prod"
```

## Run Tests

Run everything:

```bash
pytest
```

Run only smoke tests:

```bash
pytest -m smoke
```

Run only live tests against Reqres:

```bash
pytest -m live
```

Run API regression:

```bash
pytest -m "api and regression"
```

## QA Criteria

Live tests depend on network access, credentials, and external availability. In a professional environment, these tests should be separated from unit tests or local contract tests to avoid false negatives.
