import json
import os
from typing import List, TypedDict
from discord import GroupedAuthor, get_messages_grouped, load_messages
from pprint import pprint
from tqdm import tqdm
from extract import ExtractedQuote, extract_quotes

msgs = load_messages("data/quotes.json")

grouped = get_messages_grouped(msgs)

class OutputRow(TypedDict):
    startId : str 
    endId : str
    author : GroupedAuthor
    quotes : List[ExtractedQuote]

output : List[OutputRow] = []

if os.path.exists("data/output.json"):
    with open("data/output.json", "r") as fp:
        output = json.load(fp)
        
seenStartIds = set(x["startId"] for x in output)

def save_output():
    global output 
    with open("data/output.json", "w") as fp:
        json.dump(output, fp)

i = -1
for msg in tqdm(grouped):
    i += 1
    if msg["startId"] in seenStartIds: continue
    extracted = extract_quotes(msg["content"])
    if len(extracted) == 0: continue
    output.append({
        "startId": msg["startId"],
        "endId": msg["endId"],
        "author": msg["author"],
        "quotes": extracted
    })
    if i % 10 == 0:
        save_output()
        
save_output()