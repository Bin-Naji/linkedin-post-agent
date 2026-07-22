"""LangGraph nodes for the LinkedIn post agent workflow."""

from typing import Any, Dict

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import MessagesState

from .config import get_model_name, get_required_env


def get_llm() -> ChatGroq:
    """Create and return a configured Groq chat model instance.

    Returns:
        ChatGroq: An instance of ChatGroq configured with environment variables.
    """
    api_key = get_required_env("GROQ_API_KEY")

    return ChatGroq(
        model=get_model_name(),
        api_key=api_key,
        temperature=0.7,
    )


def generate_post(state: MessagesState) -> Dict[str, Any]:
    """Generate or regenerate a LinkedIn post using LLM.

    Passes the complete message history to the model so it can build upon
    the initial request and incorporate any feedback provided in previous turns.

    Args:
        state: Current graph state containing conversation messages.

    Returns:
        Dict[str, Any]: State update containing the generated LLM message.
    """
    llm = get_llm()
    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }


def review_post(state: MessagesState) -> MessagesState:
    """Display the generated LinkedIn post for human review.

    Args:
        state: Current graph state containing conversation messages.

    Returns:
        MessagesState: Unmodified state passed downstream to the router.
    """
    post = state["messages"][-1].content

    print("\n" + "=" * 60)
    print("GENERATED LINKEDIN POST")
    print("=" * 60)
    print(post)
    print("=" * 60)

    return state


def get_feedback(state: MessagesState) -> Dict[str, Any]:
    """Collect improvement feedback interactively from the user.

    Args:
        state: Current graph state containing conversation messages.

    Returns:
        Dict[str, Any]: State update containing the user's feedback as a HumanMessage.
    """
    feedback = input(
        "\nWhat would you like me to improve?\n> "
    ).strip()

    if not feedback:
        feedback = (
            "Improve the post while keeping the original topic. "
            "Make it clearer, more engaging, and professional."
        )

    return {
        "messages": [
            HumanMessage(
                content=(
                    "Please revise the LinkedIn post using "
                    f"this feedback:\n{feedback}"
                )
            )
        ]
    }


def publish_post(state: MessagesState) -> MessagesState:
    """Simulate publishing the approved LinkedIn post.

    Args:
        state: Current graph state containing conversation messages.

    Returns:
        MessagesState: Unmodified state upon workflow completion.
    """
    post = state["messages"][-1].content

    print("\n" + "=" * 60)
    print("FINAL LINKEDIN POST")
    print("=" * 60)
    print(post)
    print("=" * 60)
    print("✅ Post published successfully!")

    return state