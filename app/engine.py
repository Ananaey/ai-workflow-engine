from typing import Dict, Any, Optional, List, Callable


class WorkflowEngine:
    def __init__(self, tool_registry: Dict[str, Callable]):
        self.tool_registry = tool_registry

    def run(
        self,
        graph: Dict[str, Any],
        initial_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        graph structure (example):
        {
            "nodes": {
                "split": {"tool": "split_text"},
                "summarize": {"tool": "summarize_chunks"},
                "merge": {"tool": "merge_summaries"},
                "refine": {"tool": "refine_summary"},
            },
            "edges": {
                "split": "summarize",
                "summarize": "merge",
                "merge": "refine",
                "refine": None
            },
            "start_node": "split",
            "loop": {
                "node": "refine",
                "condition": {"key": "final_summary", "max_length": 300},
            }
        }
        """
        state = dict(initial_state)
        log: List[Dict[str, Any]] = []

        current = graph.get("start_node")
        nodes = graph.get("nodes", {})
        edges = graph.get("edges", {})

        loop_config = graph.get("loop")

        visited_count = 0
        max_steps = 100  # safety

        while current is not None and visited_count < max_steps:
            node_cfg = nodes.get(current)
            if not node_cfg:
                raise ValueError(f"Node '{current}' not defined in graph")

            tool_name = node_cfg.get("tool")
            tool_fn = self.tool_registry.get(tool_name)
            if not tool_fn:
                raise ValueError(f"Tool '{tool_name}' not found in registry")

            before_state = dict(state)
            state = tool_fn(state)
            after_state = dict(state)

            log.append({
                "node": current,
                "tool": tool_name,
                "before": before_state,
                "after": after_state,
            })

            # Handle simple loop condition for summarization workflow:
            # stop when len(final_summary) <= max_length
            if loop_config and current == loop_config.get("node"):
                key = loop_config["condition"]["key"]
                max_len = loop_config["condition"]["max_length"]
                value = state.get(key, "")

                if isinstance(value, str) and len(value) <= max_len:
                    # Stop looping: end the graph
                    break

            # Move to next node
            nxt = edges.get(current)
            current = nxt
            visited_count += 1

        return {"final_state": state, "log": log}
