# Copilot Instructions for rbnlp

## Repository Overview

**rbnlp** is a German Natural Language Processing (NLP) API service built with FastAPI and spaCy. It provides tokenization and part-of-speech tagging for German text using the `de_core_news_md` spaCy model. The service is containerized with Docker and deployed to AWS ECS.

**Repository Size**: ~67MB (includes 60MB+ of static JSON data files)
**Primary Language**: Python 3.12
**Framework**: FastAPI 0.115.2
**NLP Library**: spaCy 3.8.2 with de_core_news_md model

## Project Structure

```
/home/runner/work/rbnlp/rbnlp/
├── .github/
│   └── workflows/
│       ├── test-and-deploy.yml    # Main CI/CD pipeline (runs on main branch)
│       └── test-api.yml           # Test workflow (runs on all branches)
├── src/
│   ├── main.py                    # FastAPI application (46 lines)
│   ├── test_main.py               # Pytest test suite (93 lines, 10 tests)
│   └── data/
│       └── v1.0.0/                # Static JSON data files (24,119 German word entries)
│           ├── all.json           # Full dataset (24,119 entries, ~1.54M lines, 32MB)
│           ├── 0.json through 24.json  # Paginated data (1000 entries each, except 24.json has 119 entries)
│           └── version.json       # Version metadata
├── German-Words/                  # Git submodule (currently empty in working directory)
├── Dockerfile                     # Container definition
├── requirements.txt               # Python dependencies (75 packages)
├── testContainer.js               # Node.js integration tests for deployed container
└── .gitignore                     # Excludes env/, __pycache__/

```

## Build and Test Instructions

### Prerequisites

- **Python**: 3.12 (verified with 3.12.3)
- **Node.js**: v20+ (for integration tests, verified with v20.19.6)
- **Docker**: Latest version (verified with 28.0.4)

### Installation (Required First Step)

**ALWAYS run this before any other command:**

```bash
pip install -r requirements.txt
```

**Installation time**: ~2 minutes (downloads ~420MB including PyTorch 2.5.1, spaCy models, and CUDA libraries)
**Critical dependencies**: spaCy, FastAPI, PyTorch, de_core_news_md (German language model)

**Note**: requirements.txt is UTF-16 encoded, but pip handles this correctly. If you encounter encoding issues, convert to UTF-8: `iconv -f UTF-16 -t UTF-8 requirements.txt > requirements_utf8.txt`

### Running Tests

**Command**: 
```bash
cd src && python -m pytest -vv
```

**Test execution time**: ~5 seconds
**Expected result**: 10 tests pass
**Test coverage**:
- GET endpoint with/without query parameter
- POST endpoint with/without body data
- Static file serving for data endpoints
- Health check endpoint
- Error handling (400, 404, 422 status codes)

**Note**: Tests must be run from the `src/` directory as they use relative imports and file paths.

### Running the Development Server

**Command**:
```bash
cd src && fastapi dev main.py --port 8000
```

**Access**: http://127.0.0.1:8000
**API docs**: http://127.0.0.1:8000/docs (automatic OpenAPI documentation)

### Running the Production Server

**Command**:
```bash
cd src && fastapi run main.py --port 8080
```

**Note**: Port 80 requires root privileges. Use port 8080 for local testing.

### Building the Docker Container

**Command**:
```bash
docker build -t rbnlp .
```

**Build context**: Uses Python 3.12 base image, installs AWS CLI and all dependencies
**Working directory**: Container sets `/app` as workdir and copies `src/` contents there

### Testing the Docker Container

**⚠️ CRITICAL PORT MISMATCH ISSUE**: The Dockerfile configures the app to run on port 80, but the GitHub workflow `test-and-deploy.yml` expects port 5000. This causes the health check to fail.

**Current workflow command (FAILS)**:
```bash
docker run -d -p 5000:5000 rbnlp
node testContainer.js http://localhost:5000
```

**Workaround - Use port 80**:
```bash
docker run -d -p 5000:80 rbnlp
node testContainer.js http://localhost:5000
```

**Alternative - Rebuild with correct port**:
Modify Dockerfile line 8 to: `CMD ["fastapi", "run", "main.py", "--port", "5000"]`

## API Endpoints

1. **GET /?s={text}** - Tokenize and tag a single German sentence
2. **POST /** with `{"s": ["text1", "text2", ...]}` - Batch process multiple sentences
3. **GET /health** - Health check endpoint (returns `{"status": "ok"}`)
4. **GET /data/v1.0.0/{file}.json** - Serve static German word data files
   - `all.json`: Complete dataset (24,119 word entries)
   - `0.json` through `23.json`: 1000 word entries each
   - `24.json`: 119 word entries (remaining from 24,000 / 1000 pagination)
   - `version.json`: Version metadata

**Note**: JSON files are formatted with pretty-printing, so line counts are much higher than entry counts (e.g., 24.json has 119 entries but ~8,700 lines).

## GitHub Workflows

### test-api.yml (Runs on All Branches)

**Trigger**: Push to any branch, manual workflow dispatch
**Steps**:
1. Checkout with submodules (`submodules: recursive`)
2. Set up Python 3.12
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests: `cd src && python -m pytest -vv`

**Expected duration**: ~3 minutes

### test-and-deploy.yml (Runs on Main Branch Only)

**Trigger**: Push to main branch, manual workflow dispatch
**Steps**:

**Job 1: test-container**
1. Checkout with submodules
2. Set up Docker buildx
3. Build Docker image
4. Run container on port 5000:5000 ⚠️ (PORT MISMATCH - see above)
5. Run Node.js integration tests

**Job 2: build-and-deploy** (requires test-container success)
1. Checkout with submodules
2. Configure AWS credentials (requires secrets)
3. Login to Amazon ECR
4. Build and push Docker image to ECR
5. Deploy to ECS cluster (forces new deployment)

**Environment variables**:
- `ECR_IMAGE`: rbnlp
- `ECS_CLUSTER`: rbnlp-cluster
- `ECS_SERVICE`: rbnlp-service
- `AWS_REGION`: eu-west-2

**Required secrets**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_ACCOUNT_ID`

## Code Architecture

### main.py Structure

**Key components**:
- `nlp`: spaCy German model loaded with disabled components (parser, lemmatizer, attribute_ruler, ner) for faster processing
- `token2obj(tok)`: Converts spaCy token to JSON object with text, POS tag, and grammatical case
- `get_tokens(doc)`: Maps document tokens to JSON array
- FastAPI routes for GET/POST analysis and static file serving

**Pydantic model**:
```python
class Item(BaseModel):
    s: List[str]
```

### test_main.py Structure

Uses FastAPI TestClient for endpoint testing. All tests verify exact JSON response structure and status codes.

## Key Dependencies

From requirements.txt (75 packages total):
- **fastapi** (0.115.2): Web framework
- **spacy** (3.8.2): NLP library
- **de_core_news_md**: German language model (installed from GitHub release)
- **torch** (2.5.1): PyTorch for spaCy transformers (~190MB)
- **pytest** (8.3.3): Testing framework
- **uvicorn** (0.32.0): ASGI server
- **pydantic** (2.9.2): Data validation

## Common Issues and Workarounds

### 1. Port Mismatch in Docker Testing
**Issue**: Dockerfile uses port 80, workflow expects port 5000
**Workaround**: Map host port 5000 to container port 80: `docker run -d -p 5000:80 rbnlp`

### 2. Git Submodule Not Initialized
**Issue**: German-Words submodule directory is empty
**Workaround**: Workflows use `actions/checkout@v4` with `submodules: recursive`
**Manual fix**: `git submodule update --init --recursive`

### 3. Permission Denied on Port 80
**Issue**: FastAPI cannot bind to port 80 without root
**Workaround**: Use port 8080 or higher for local testing

### 4. Tests Must Run from src/ Directory
**Issue**: Relative imports and file paths in test_main.py assume working directory is src/
**Solution**: Always `cd src` before running pytest

## Making Code Changes

### Testing Your Changes

1. **ALWAYS install dependencies first**: `pip install -r requirements.txt`
2. **Run tests from src/ directory**: `cd src && python -m pytest -vv`
3. **Test locally with dev server**: `cd src && fastapi dev main.py --port 8000`
4. **Verify API responses**: Check http://127.0.0.1:8000/docs for interactive testing

### Validating Changes Before PR

1. Run the test suite: `cd src && python -m pytest -vv` (must pass all 10 tests)
2. Build Docker image: `docker build -t rbnlp .`
3. Test containerized app: `docker run -d -p 5000:80 rbnlp && node testContainer.js http://localhost:5000`

### When to Update Tests

Update `src/test_main.py` if you:
- Modify API response structure
- Add/remove endpoints
- Change error handling behavior
- Modify data validation rules

## Important Notes

- **No linting configured**: Repository has no pylint, flake8, black, or other linting tools
- **No type checking**: No mypy or similar type checkers configured
- **Data files are committed**: The src/data/ directory contains 60MB+ of static JSON (version-controlled)
- **Submodule dependency**: German-Words submodule must be initialized for production deployment
- **Python version locked**: Dockerfile and workflow explicitly use Python 3.12

## Trust These Instructions

This documentation is based on verified exploration and testing of the repository. Only perform additional searches if:
- The instructions are incomplete for your specific task
- You discover the instructions are outdated or incorrect
- You are working on a completely new feature not covered here

For standard tasks (bug fixes, endpoint modifications, test updates), follow these instructions directly without additional exploration.
