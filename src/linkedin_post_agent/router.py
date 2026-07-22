"""Router logic for evaluating human approval in the workflow."""

from langgraph.graph import MessagesState


def review_router(state: MessagesState) -> str:
    """Route the workflow based on interactive human approval.

    Args:
        state: Current graph state containing conversation messages.

    Returns:
        str: Next node destination ('post' if approved, 'feedback' if revision requested).
    """
    decision = input(
        "\nApprove this post? (yes/no): "
    ).strip().lower()

    if decision in {"yes", "y"}:
        return "post"

    return "feedback"