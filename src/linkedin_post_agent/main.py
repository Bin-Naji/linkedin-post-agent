"""Application entry point for running the LinkedIn Post Agent."""

from langchain_core.messages import HumanMessage
from .graph import build_graph


def main() -> None:
    """Run the LinkedIn post generation workflow CLI."""
    app = build_graph()

    initial_message = HumanMessage(
        content=(
            "Write an engaging LinkedIn post about AI Agents "
            "taking over content creation and supercharging human workflows."
        )
    )

    app.invoke({"messages": [initial_message]})


if __name__ == "__main__":
    main()