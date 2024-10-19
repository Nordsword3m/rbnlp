from fastapi import FastAPI
from spacy import load
from urllib.parse import unquote
from pydantic import BaseModel
class Item(BaseModel):
    s: str

app = FastAPI()
nlp = load("de_core_news_sm", disable=["parser", "morphologizer", "lemmatizer", "attribute_ruler", "ner"])

@app.get("/")
def read_root(s: str = None):
  if s is not None:
    return nlp(unquote(s)).to_json()

@app.post("/")
def read_root_post(item: Item = None):
  if item is not None and item.s is not None:
    return nlp(item.s).to_json()
  
  return "use s key to analyze a text"
