"""
Smart PII Redaction Agent

This agent uses tinyagent and the mcpd Python SDK to
orchestrate the redaction pipeline:
1. Extract text using `doc-parser`
2. Detect PII using `ner-detector`
3. Verify and apply redaction using `redactor`
"""

import argparse
from mcpd import McpdClient
from tinyagent import AgentConfig, TinyAgent

# =============================================================================
# CONFIGURATION
# =============================================================================

MCPD_URL = "http://localhost:8090"
MODEL_ID = "openai/local"
MODEL_API_BASE = "http://localhost:8086/v1"
MODEL_API_KEY = "local"

AGENT_INSTRUCTIONS = """\
You are a highly secure Smart PII Redaction Agent. Your sole responsibility is to redact sensitive personally identifiable information (PII) from documents.
You have access to the following tools:
1. `extract_text(file_path)`: Extracts raw text from a document (e.g., PDF, TXT).
2. `detect_entities(text)`: Analyzes text to find candidate PII entities like Names, Organizations, and Locations.
3. `apply_redaction(original_text, entities_to_redact)`: Replaces verified entities in the text with [REDACTED].

Your workflow for any document:
1. Extract the text using `extract_text`.
2. Find candidate entities using `detect_entities`.
3. Carefully reason about the returned candidates. Ask yourself if they are truly sensitive PII in the context of the text.
4. Call `apply_redaction` with only the VERIFIED sensitive entities.
5. Provide a summary of the entities you redacted and the final redacted text.
"""

# =============================================================================
# AGENT SETUP
# =============================================================================

def run_agent(file_path: str, model_id: str) -> None:
    print(f"Connecting to mcpd at {MCPD_URL}...")
    try:
        client = McpdClient(api_endpoint=MCPD_URL)
        tools = client.agent_tools()
        print(f"Loaded {len(tools)} tools from mcpd")
    except Exception as e:
        print(f"Failed to connect to mcpd: {e}")
        print("Please ensure mcpd is running.")
        return

    print(f"Creating tinyagent with model {model_id}...")
    agent = TinyAgent.create(
        AgentConfig(
            model_id=model_id,
            api_base=MODEL_API_BASE,
            api_key=MODEL_API_KEY,
            instructions=AGENT_INSTRUCTIONS,
            tools=tools,
        ),
    )

    query = f"Please process and redact PII from this file: {file_path}"
    print(f"\nQuery: {query}")
    print("=" * 60)
    agent_trace = agent.run(query)

    print("\nFinal Result:")
    print("=" * 60)
    print(getattr(agent_trace, "final_output", agent_trace))


def main():
    parser = argparse.ArgumentParser(description="Smart PII Redaction Agent")
    parser.add_argument(
        "file_path",
        help="Path to the document to redact",
    )
    parser.add_argument(
        "--model",
        default=MODEL_ID,
        help="Model ID for generation",
    )
    args = parser.parse_args()

    run_agent(args.file_path, args.model)


if __name__ == "__main__":
    main()
