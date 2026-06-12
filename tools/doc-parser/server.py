import sys
from typing import Any
import PyPDF2
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("doc-parser")

@mcp.tool()
def extract_text(file_path: str) -> str:
    """Extracts raw text from a PDF document.
    
    Args:
        file_path: The absolute path to the PDF file or text file.
        
    Returns:
        The extracted text content from the document.
    """
    try:
        if file_path.lower().endswith('.pdf'):
            text = []
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
            return "\n".join(text)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

if __name__ == "__main__":
    mcp.run()
