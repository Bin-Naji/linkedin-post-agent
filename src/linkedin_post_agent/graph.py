"""LangGraph workflow definition and compilation with checkpointer persistence support."""

from typing import Any, Optional
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import (
    END,
    START,
    MessagesState,
    StateGraph,
)
from langgraph.graph.state import CompiledStateGraph

from .nodes import (
    generate_post,
    get_feedback,
    publish_post,
    review_post,
)
from .router import review_router


def build_graph(checkpointer: Optional[Any] = None) -> CompiledStateGraph:
    """Build and compile the human-in-the-loop LinkedIn post workflow.

    Args:
        checkpointer: Optional LangGraph checkpointer for state persistence.
                     If None, defaults to an in-memory MemorySaver checkpointer.

    Returns:
        CompiledStateGraph: The executable compiled LangGraph application.
    """
    if checkpointer is None:
        checkpointer = MemorySaver()

    builder = StateGraph(MessagesState)

    # Register nodes
    builder.add_node("generator", generate_post)
    builder.add_node("review", review_post)
    builder.add_node("feedback", get_feedback)
    builder.add_node("post", publish_post)

    # Define edges
    builder.add_edge(START, "generator")
    builder.add_edge("generator", "review")

    # Conditional routing: Review -> Post (Publish) OR Feedback (Revise)
    builder.add_conditional_edges(
        "review",
        review_router,
        {
            "post": "post",
            "feedback": "feedback",
        },
    )

    # Feedback loop -> Generator
    builder.add_edge("feedback", "generator")
    builder.add_edge("post", END)

    return builder.compile(checkpointer=checkpointer)