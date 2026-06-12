import sys
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ner-detector")

@mcp.tool()
def detect_entities(text: str) -> str:
    """Detects sensitive entities (PII) such as Names, Organizations, and Locations in the text.
    
    Args:
        text: The raw text to analyze.
        
    Returns:
        A JSON string containing a list of detected candidate entities.
    """
    # MOCK implementation
    entities = []
    words = text.split()
    for i, word in enumerate(words):
        clean_word = word.strip(".,;:!?()[]{}'\"")
        if clean_word and clean_word[0].isupper() and len(clean_word) > 1:
            if i > 0 and words[i-1].endswith('.'):
                continue
            entities.append({
                "entity": clean_word,
                "type": "MOCK_PII_CANDIDATE"
            })
            
    # Deduplicate
    unique_entities = list({e['entity']: e for e in entities}.values())
    return json.dumps(unique_entities)

if __name__ == "__main__":
    mcp.run()
