from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from spacy import load
from urllib.parse import unquote
from pydantic import BaseModel
class Item(BaseModel):
  s: List[str]

app = FastAPI()
nlp = load("de_core_news_md", disable=["parser", "lemmatizer", "attribute_ruler", "ner"])

def firstElem(arr):
  if len(arr) == 0:
    return ""
  return arr[0]

def token2obj(tok):
  return {
    "text": tok.text.strip(),
    "tag": tok.tag_,
    "case": firstElem(tok.morph.get("Case")),
  }

def get_tokens(doc):
  return [token2obj(tok) for tok in doc]

@app.get("/")
def read_root(s: str = None):
  if s is not None:
    return get_tokens(nlp(unquote(s)))
  
  raise HTTPException(status_code=400, detail="use s param to analyze a text")  

@app.post("/")
def read_root_post(item: Item = None):
  if item is not None and item.s is not None:
    return [get_tokens(d) for d in nlp.pipe([unquote(x) for x in item.s])]
  
  raise HTTPException(status_code=400, detail="use s body data key to analyze a list of texts")  

app.mount("/data", StaticFiles(directory="./German-Words/data"), name="data")

@app.get("/health")
def health():
  return {"status": "ok"}