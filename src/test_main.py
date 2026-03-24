import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root_no_text():
  response = client.get("/")
  assert response.status_code == 400
  assert response.json() == {"detail": "use s param to analyze a text"}

def test_read_root():
  response = client.get("/?s=Das%20ist%20ein%20Test%2Cder%20funktioniert.")
  assert response.status_code == 200
  assert response.json() == [
    {"text": "Das", "tag": "PDS", "case": "Nom"},
    {"text": "ist", "tag": "VAFIN", "case": ""},
    {"text": "ein", "tag": "ART", "case": "Nom"},
    {"text": "Test", "tag": "NN", "case": "Nom"},
    {"text": ",", "tag": "$,", "case": ""},
    {"text": "der", "tag": "PRELS", "case": "Nom"},
    {"text": "funktioniert", "tag": "VVFIN", "case": ""},
    {"text": ".", "tag": "$.", "case": ""}
  ]

def test_read_root_post_no_item():
  response = client.post("/")
  assert response.status_code == 400
  assert response.json() == {"detail": "use s body data key to analyze a list of texts"}

def test_read_root_post_no_s():
  response = client.post("/", json={"d": ["Das ist ein Test,der funktioniert."]})
  assert response.status_code == 422
  assert response.json() == {
    "detail":[
      {
        "input": {
          "d": ["Das ist ein Test,der funktioniert."]
        },
        "loc": ["body", "s"],
        "msg": "Field required",
        "type": "missing",
      }
    ]
  }

def test_read_root_post():
  response = client.post("/", json={"s": ["Das ist ein Test,der funktioniert.", "Das ist ein weiterer Test."]})
  assert response.status_code == 200
  assert response.json() == [
    [
      {"text": "Das", "tag": "PDS", "case": "Nom"},
      {"text": "ist", "tag": "VAFIN", "case": ""},
      {"text": "ein", "tag": "ART", "case": "Nom"},
      {"text": "Test", "tag": "NN", "case": "Nom"},
      {"text": ",", "tag": "$,", "case": ""},
      {"text": "der", "tag": "PRELS", "case": "Nom"},
      {"text": "funktioniert", "tag": "VVFIN", "case": ""},
      {"text": ".", "tag": "$.", "case": ""}
    ],
    [
      {"text": "Das", "tag": "PDS", "case": "Nom"},
      {"text": "ist", "tag": "VAFIN", "case": ""},
      {"text": "ein", "tag": "ART", "case": "Nom"},
      {"text": "weiterer", "tag": "ADJA", "case": "Nom"},
      {"text": "Test", "tag": "NN", "case": "Nom"},
      {"text": ".", "tag": "$.", "case": ""}
    ]
  ]

@pytest.mark.parametrize("version,expected_count", [
  ("v1.2.0", 70926),
  ("v1.2.1", 70862),
])
def test_get_data_all(version, expected_count):
  response = client.get(f"/data/{version}/all.json")
  assert response.status_code == 200
  assert len(response.json()) == expected_count

@pytest.mark.parametrize("version,filename", [
  ("v1.2.0", "1000.json"),
  ("v1.2.1", "72.json"),
])
def test_get_data_sect_not_found(version, filename):
  response = client.get(f"/data/{version}/{filename}")
  assert response.status_code == 404
  assert response.json() == {"detail": "Not Found"}

@pytest.mark.parametrize("version,filename,expected_count", [
  ("v1.2.0", "0.json", 1000),
  ("v1.2.0", "10.json", 1000),
  ("v1.2.0", "70.json", 926),
  ("v1.2.1", "0.json", 1000),
  ("v1.2.1", "10.json", 1000),
  ("v1.2.1", "70.json", 862),
  ("v1.2.1", "71.json", 33),
])
def test_get_data_sect(version, filename, expected_count):
  response = client.get(f"/data/{version}/{filename}")
  assert response.status_code == 200
  assert len(response.json()) == expected_count

def test_health():
  response = client.get("/health")
  assert response.status_code == 200
  assert response.json() == {"status": "ok"}
