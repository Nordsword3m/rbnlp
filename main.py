import os
from typing import List
from fastapi import FastAPI, HTTPException
from spacy import load
from urllib.parse import unquote
from pydantic import BaseModel
from re import sub
import json
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

with open("German-Words/parsedWords.json", encoding="utf8") as f:
  data = json.load(f)

# Load sections from each file in German-Words/parsedSections into array
sections = []
for root, dirs, files in os.walk("German-Words/parsedSections"):
  for file in files:
    with open(os.path.join(root, file), encoding="utf8") as f:
      sections.append(json.load(f))

@app.get("/data")
def get_data(sect: int = None):
  if sect is not None:
    if sect < len(sections):
      return sections[sect]
    else:
      raise HTTPException(status_code=404, detail="Section not found")  
    
  return data
