"""Unit and integration tests for graph compilation and persistence."""

from langgraph.checkpoint.memory import MemorySaver
from linkedin_post_agent.graph import build_graph


def test_graph_compilation():
    """Test that the state graph compiles without errors."""
    app = build_graph()
    assert app is not None


def test_graph_checkpointer_integration():
    """Test graph compilation with a MemorySaver checkpointer."""
    checkpointer = MemorySaver()
    app = build_graph(checkpointer=checkpointer)
    assert app.checkpointer == checkpointer
