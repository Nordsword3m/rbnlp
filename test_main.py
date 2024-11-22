from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root_no_text():
  response = client.get("/")
  assert response.status_code == 400
  assert response.json() == {"detail": "use s key to analyze a text"}

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
  assert response.json() == {"detail": "use s key to analyze a list of texts"}

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

def test_get_data_all():
  response = client.get("/data/all.json")
  assert response.status_code == 200
  assert len(response.json()) == 24119

def test_get_data_sect_not_found():
  response = client.get("/data/1000.json")
  assert response.status_code == 404
  assert response.json() == {"detail": "Not Found"}

def test_get_data_sect():
  response = client.get("/data/10.json")
  assert response.status_code == 200
  assert len(response.json()) == 1000