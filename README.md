# AI Workflow Engine (Assignment)

This is a minimal workflow / graph engine built with **FastAPI** for the AI Engineering assignment.

It supports:
- Defining nodes (Python functions) as tools
- Maintaining a shared state (Python dict) flowing through nodes
- Sequential edges between nodes
- A simple loop configuration to repeat a node until a condition is satisfied
- FastAPI APIs to create graphs, run them, and inspect run state

The example workflow implemented is **Option B: Summarization + Refinement**:
1. Split text into chunks
2. Generate summaries for each chunk
3. Merge summaries
4. Refine final summary
5. Stop when summary length is under a configurable limit


## Project Structure

```text
ai-workflow-engine/
├─ app/
│  ├─ __init__.py
│  ├─ main.py        # FastAPI app + endpoints
│  ├─ engine.py      # Core workflow engine
│  ├─ registry.py    # Tool registry and tools for the sample workflow
│  └─ models.py      # Pydantic models for requests
├─ requirements.txt
└─ README.md
