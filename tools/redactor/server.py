import sys
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("redactor")

@mcp.tool()
def apply_redaction(original_text: str, entities_to_redact: list[str]) -> str:
    """Redacts specified entities from the original text by replacing them with [REDACTED].
    
    Args:
        original_text: The source text.
        entities_to_redact: A list of string entities that have been verified as PII.
        
    Returns:
        The redacted text.
    """
    redacted_text = original_text
    
    # Sort by length descending to avoid partial matches
    sorted_entities = sorted(entities_to_redact, key=len, reverse=True)
    
    for entity in sorted_entities:
        if entity:
            redacted_text = redacted_text.replace(entity, "[REDACTED]")
            
    return redacted_text

if __name__ == "__main__":
    mcp.run()
