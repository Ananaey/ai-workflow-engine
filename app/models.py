from pydantic import BaseModel
from typing import Dict, Any, Optional


class GraphDefinition(BaseModel):
    nodes: Dict[str, Dict[str, Any]]
    edges: Dict[str, Optional[str]]
    start_node: str
    loop: Optional[Dict[str, Any]] = None


class RunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]
