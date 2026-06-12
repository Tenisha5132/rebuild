# Smart PII Redaction Agent

A smart, privacy-first document redaction tool built with the **Mozilla.ai Stack**.

This hackathon project demonstrates how to build an offline, intelligent PII redaction pipeline using local models and the Model Context Protocol (MCP). Sensitive documents never leave your machine!

## Architecture

This project leverages the following Mozilla.ai technologies:
- **`any-agent` (TinyAgent)**: Orchestrates the redaction pipeline, routing prompts and executing tools.
- **`mcpd`**: Serves and manages three custom tool servers:
  - `doc-parser`: Extracts text from documents (PDF, txt).
  - `ner-detector`: Interfaces with a BERT-based Named Entity Recognition model to identify candidate PII.
  - `redactor`: Applies redactions to the verified text.
- **`llamafile`**: A lightweight LLM (e.g. Gemma or Phi-3) that acts as the "Reasoning Engine". It verifies whether NER candidates are actually sensitive in the context of the sentence before redacting them.
- **`encoderfile`**: A robust, fast local embeddings & NER engine (used by `ner-detector`).

## Quickstart

### Prerequisites
1. Install Python 3.11+, `uv` (for python environments), and `mcpd` (via brew).
2. Download your `llamafile` and `encoderfile` binaries.

### Running the Stack

**1. Start the LLM Server (Terminal 1)**
```bash
./gemma4.llamafile --port 8086
```

**2. Start the MCP Server Daemon (Terminal 2)**
```bash
cd mozilla-redactor
uv tool install --editable . --force
mcpd daemon --dev --log-level=DEBUG --log-path ./mcpd.log --runtime-file .mcpd.toml
```

**3. Run the Redaction Agent (Terminal 3)**
```bash
cd mozilla-redactor
uv run python agent/main.py sample_doc.txt
```

## License
This project is licensed under the Mozilla Public License 2.0 (MPL-2.0). See the [LICENSE](LICENSE) file for details.
