import json
from typing import List, Tuple, TypedDict
from openai import OpenAI
import dotenv
dotenv.load_dotenv()
import os

class ExtractedQuote(TypedDict):
    quote : str
    by : str

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_KEY"]
)

CHAT_MODEL="mistralai/mistral-small-24b-instruct-2501"

SYSTEM_PROMPT = """## Task
Extract quotes and authors from the user's message if any are present.
## Rules
- Do not change the quotes in any way
- If there are multiple quotes, extract them separately
- If there are no quotes, do not extract anything
- Response must be in JSON in the below format
##  Output JSON Format
[{"quote": "quote content A", "by": "By A"}, {"quote": "quote content B", "by": "By B"}]
"""

EXAMPLE_RESULTS : List[Tuple[str, List[ExtractedQuote]]] = [
    ("lele\n- me", [{ "quote": "lele", "by": "me" }]),
    ("“Why can’t you be more positive?” - Harrison", [{ "quote": "Why can’t you be more positive?", "by": "Harrison" }]),
    ("GOTEEMMMMM\nglad im still up ther", []),
    ("“It’s like prostitution but free”- Jake 2021\n“I learnt how to grow weed and not get caught thanks to her.” - Cameron Walker 2021", [
        { "quote": "It’s like prostitution but free", "by": "Jake 2021" },
        { "quote": "I learnt how to grow weed and not get caught thanks to her.", "by": "Cameron Walker 2021" },
    ]),
]

__example_results_messages = []
for msg, result in EXAMPLE_RESULTS:
    __example_results_messages.append({
        "role": "user",
        "content": msg
    })
    __example_results_messages.append({
        "role": "assistant",
        "content": json.dumps(result)
    })

def extract_quotes(content : str) -> List[ExtractedQuote]:
    completion = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            *__example_results_messages,
            {
                "role": "user",
                "content": content   
            }
        ]
    )
    try:
        result = json.loads(completion.choices[0].message.content)
    except:
        result = []
    if isinstance(result, list):
        return result
    else:
        return []