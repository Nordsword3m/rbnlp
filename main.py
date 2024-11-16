from typing import List
from fastapi import FastAPI
from spacy import load
from urllib.parse import unquote
from pydantic import BaseModel
from json import dumps
from re import sub
class Item(BaseModel):
  s: List[str]

app = FastAPI()
nlp = load("de_core_news_sm", disable=["parser", "lemmatizer", "attribute_ruler", "ner"])

def firstElem(arr):
  if len(arr) == 0:
    return ""
  return arr[0]

def token2obj(tok):
  return {
    "text": sub(r"[.,/#!?$%^&*;:{}=\-_`~()]", '', tok.text).strip(),
    "tag": tok.tag_,
    "case": firstElem(tok.morph.get("Case")),
  }

def get_tokens(doc):
  return [token2obj(tok) for tok in doc]

@app.get("/")
def read_root(s: str = None):
  if s is not None:
    return get_tokens(nlp(unquote(s)))

@app.post("/")
def read_root_post(item: Item = None):
  if item is not None and item.s is not None:
    return [get_tokens(d) for d in nlp.pipe([unquote(x) for x in item.s])]
  
  return "use s key to analyze a text"
