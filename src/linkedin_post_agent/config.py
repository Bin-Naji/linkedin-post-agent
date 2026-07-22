"""Configuration loader for environment variables and model settings."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_required_env(name: str) -> str:
    """Return a required environment variable or raise an error.

    Args:
        name: Name of the environment variable.

    Returns:
        str: Value of the environment variable.

    Raises:
        ValueError: If the environment variable is missing or empty.
    """
    value = os.getenv(name)

    if not value:
        raise ValueError(
            f"Missing required environment variable: {name}. "
            "Please ensure it is set in your .env file."
        )

    return value


def get_model_name() -> str:
    """Return the configured Groq model name, defaulting to llama-3.1-8b-instant.

    Returns:
        str: Model identifier string.
    """
    return os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")