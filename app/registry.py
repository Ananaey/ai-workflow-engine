from typing import Dict, Any, List

# Simple dictionary to hold tools
tool_registry: Dict[str, callable] = {}


def tool(name: str):
    """Decorator to register a tool by name."""
    def wrapper(fn):
        tool_registry[name] = fn
        return fn
    return wrapper


@tool("split_text")
def split_text_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Input in state: { "text": "long text...", "chunk_size": 200 }
    Output adds:   { "chunks": [ ... ] }
    """
    text = state.get("text", "")
    chunk_size = state.get("chunk_size", 200)

    chunks: List[str] = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    state["chunks"] = chunks
    return state


@tool("summarize_chunks")
def summarize_chunks_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Very dumb 'summary': take first sentence of each chunk.
    """
    chunks: List[str] = state.get("chunks", [])
    summaries: List[str] = []

    for c in chunks:
        if "." in c:
            summaries.append(c.split(".")[0] + ".")
        else:
            summaries.append(c)

    state["summaries"] = summaries
    return state


@tool("merge_summaries")
def merge_summaries_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    summaries: List[str] = state.get("summaries", [])
    merged = " ".join(summaries)
    state["merged_summary"] = merged
    return state


@tool("refine_summary")
def refine_summary_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Very simple refinement: truncate to max_length chars.
    Input: state["max_length"]
    """
    merged = state.get("merged_summary", "")
    max_length = state.get("max_length", 300)

    refined = merged[:max_length].strip()
    state["final_summary"] = refined
    return state
