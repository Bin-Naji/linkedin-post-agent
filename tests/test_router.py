"""Unit tests for router logic."""

from unittest.mock import patch
from langchain_core.messages import AIMessage
from linkedin_post_agent.router import review_router


def test_review_router_approve_yes():
    """Test that 'yes' routes to the 'post' node."""
    state = {"messages": [AIMessage(content="Draft post")]}
    with patch("builtins.input", return_value="yes"):
        result = review_router(state)
        assert result == "post"


def test_review_router_approve_y():
    """Test that 'y' routes to the 'post' node."""
    state = {"messages": [AIMessage(content="Draft post")]}
    with patch("builtins.input", return_value="y"):
        result = review_router(state)
        assert result == "post"


def test_review_router_reject_no():
    """Test that 'no' routes to the 'feedback' node."""
    state = {"messages": [AIMessage(content="Draft post")]}
    with patch("builtins.input", return_value="no"):
        result = review_router(state)
        assert result == "feedback"


def test_review_router_feedback_text():
    """Test that any other input routes to the 'feedback' node."""
    state = {"messages": [AIMessage(content="Draft post")]}
    with patch("builtins.input", return_value="n"):
        result = review_router(state)
        assert result == "feedback"
