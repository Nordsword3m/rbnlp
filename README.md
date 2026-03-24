# rbnlp

A German NLP API built with FastAPI and spaCy, providing tokenisation and part-of-speech tagging for German text.

## Prerequisites

- Python 3.12
- Node.js v20+ *(only needed for Docker integration tests)*
- Docker *(only needed for container build/test)*

## Installation

Install all Python dependencies (required before any other step):

```bash
pip install -r requirements.txt
```

> This downloads ~420 MB including PyTorch, spaCy, and the German language model. Expect ~2 minutes on first run.

## Running Tests

```
cd src
python -m pytest -vv
```

All 17 tests should pass in ~5 seconds.

## Running the Development Server

```
cd src
python -m fastapi dev main.py --port 8000
```

The API will be available at <http://127.0.0.1:8000>.  
Interactive API docs (Swagger UI) are at <http://127.0.0.1:8000/docs>.

## Running the Production Server

```
cd src
python -m fastapi run main.py --port 8080
```

## Docker

### Build the image

```bash
docker build -t rbnlp .
```

### Run the container

```bash
docker run -d -p 5000:5000 rbnlp
```

### Run integration tests against the container

```bash
node testContainer.js http://localhost:5000
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/?s={text}` | Tokenise and tag a single German sentence |
| `POST` | `/` | Batch process multiple sentences — body: `{"s": ["text1", "text2"]}` |
| `GET` | `/health` | Health check — returns `{"status": "ok"}` |
| `GET` | `/data/v1.2.0/{file}.json` | Serve static German word data (v1.2.0) |
| `GET` | `/data/v1.2.1/{file}.json` | Serve static German word data (v1.2.1) |

### Example request

```bash
curl "http://localhost:8000/?s=Das%20ist%20ein%20Test."
```

```json
[
  {"text": "Das", "tag": "PDS", "case": "Nom"},
  {"text": "ist", "tag": "VAFIN", "case": ""},
  {"text": "ein", "tag": "ART", "case": "Nom"},
  {"text": "Test", "tag": "NN", "case": "Nom"},
  {"text": ".", "tag": "$.", "case": ""}
]
```

### Data files

Each dataset version provides:

- `all.json` — full word list
- `0.json` … `N.json` — paginated sections of 1,000 entries each (last file contains the remainder)

| Version | Total entries | Last section file |
|---------|--------------|-------------------|
| v1.2.0  | 70,926       | `70.json` (926 entries) |
| v1.2.1  | 70,862       | `71.json` (33 entries) |
