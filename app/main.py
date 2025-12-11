from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uuid

from .engine import WorkflowEngine
from .registry import tool_registry
from .models import GraphDefinition, RunRequest

app = FastAPI(title="Minimal Workflow Engine")

# In-memory stores
GRAPHS: Dict[str, Dict[str, Any]] = {}
RUNS: Dict[str, Dict[str, Any]] = {}

engine = WorkflowEngine(tool_registry=tool_registry)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/graph/create")
def create_graph(graph_def: GraphDefinition):
    graph_id = str(uuid.uuid4())
    GRAPHS[graph_id] = graph_def.dict()
    return {"graph_id": graph_id}


@app.post("/graph/run")
def run_graph(req: RunRequest):
    graph = GRAPHS.get(req.graph_id)
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")

    result = engine.run(graph=graph, initial_state=req.initial_state)

    run_id = str(uuid.uuid4())
    RUNS[run_id] = result["final_state"]

    return {
        "run_id": run_id,
        "final_state": result["final_state"],
        "log": result["log"],
    }


@app.get("/graph/state/{run_id}")
def get_state(run_id: str):
    state = RUNS.get(run_id)
    if not state:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"run_id": run_id, "state": state}
