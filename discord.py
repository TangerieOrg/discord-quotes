import json
from typing import List, TypedDict
from tqdm import tqdm

class Author(TypedDict):
    name : str
    id : str

class Message(TypedDict):
    author : Author
    id : str 
    content : str
    timestamp: str

def load_messages(path : str) -> List[Message]:
    with open(path, "r") as fp:
        data = json.load(fp)
        
    return data["messages"]

class GroupedAuthor(TypedDict):
    id : str
    name : str

class GroupedMessage(TypedDict):
    author: GroupedAuthor
    content : str 
    startId : str 
    endId : str
    timestamp: str

def get_messages_grouped(msgs : List[Message]) -> List[GroupedMessage]:
    cur_author : str = None 
    cur_message_parts : List[Message] = []
    cur_timestamp : str = None
    grouped : List[GroupedMessage] = []
    
    for msg in msgs:
        timestamp = ":".join(msg["timestamp"].split(".")[0].split(":")[:-1])
        if msg["author"]["id"] != cur_author or timestamp != cur_timestamp:
            if len(cur_message_parts) > 0:
                grouped.append({
                    "author": {
                        "id": msg["author"]["id"],
                        "name": msg["author"]["name"],
                    },
                    "startId": cur_message_parts[0]["id"],
                    "endId": cur_message_parts[-1]["id"],
                    "timestamp": msg["timestamp"],
                    "content": "\n".join(x["content"] for x in cur_message_parts)
                })
            cur_message_parts = []
            cur_author = msg["author"]["id"]
            cur_timestamp = timestamp
        cur_message_parts.append(msg)
    
    grouped.append({
        "author": msg["author"],
        "startId": cur_message_parts[0]["id"],
        "endId": cur_message_parts[-1]["id"],
        "timestamp": cur_message_parts[-1]["timestamp"],
        "content": "\n".join(x["content"] for x in cur_message_parts)
    })
    
    return grouped