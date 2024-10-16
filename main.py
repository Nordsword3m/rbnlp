from typing import Union
from fastapi import FastAPI
from spacy import load
from urllib.parse import unquote

app = FastAPI()
nlp = load("de_core_news_sm", disable=["parser", "attribute_ruler", "lemmatizer", "ner"])

@app.get("/")
def read_root(s: Union[str, None] = None):
  if s is not None:
    return nlp(unquote(s)).to_json()
  else:
    return None
