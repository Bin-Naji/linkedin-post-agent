# 🤖 LinkedIn Post Agent

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.2+-emerald.svg)](https://github.com/langchain-ai/langgraph)
[![Groq](https://img.shields.io/badge/Groq-Fast%20Inference-orange.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![uv](https://img.shields.io/badge/uv-managed-purple.svg)](https://github.com/astral-sh/uv)

A human-in-the-loop AI workflow that generates, reviews, iteratively improves, and publishes LinkedIn posts using **LangGraph** and **Groq**.

The project demonstrates how to build a stateful AI workflow where an LLM generates draft content, a human reviews the result, and the workflow either approves the post or incorporates feedback for revision cycles.

---

## 🚀 Architecture & Workflow

The agent uses a LangGraph `StateGraph` with conditional routing to manage the conversation state and feedback loop:

```mermaid
graph TD
    START([START]) --> Generator[Generator Node<br/><i>LLM creates post</i>]
    Generator --> Review[Review Node<br/><i>Human inspects draft</i>]
    Review --> Router{Approve?}
    Router -- Yes --> Post[Post Node<br/><i>Publish final content</i>]
    Router -- No --> Feedback[Feedback Node<br/><i>Collect user feedback</i>]
    Feedback --> Generator
    Post --> END([END])
```

---

## ✨ Features

- **LLM Content Generation**: Fast LinkedIn post creation powered by Groq's high-speed inference.
- **Human-in-the-Loop (HITL)**: Direct human approval or revision request at the review node.
- **Iterative Feedback Loop**: Captures feedback and appends it to state history for intelligent LLM revisions.
- **State Management**: Built on `MessagesState` to preserve full context across revision iterations.
- **Conditional Routing**: Clean control flow separation using LangGraph routers and edges.
- **Secure Environment Config**: Strict `dotenv` management separating secrets from codebase.
- **Modern Package Tooling**: Fully managed with `uv` for fast, reproducible environment sync.

---

## 🛠️ Tech Stack

* **Language**: Python 3.11+
* **Orchestration**: [LangGraph](https://github.com/langchain-ai/langgraph)
* **LLM Integration**: `langchain-groq`, `langchain-core`
* **Inference Engine**: [Groq API](https://groq.com/) (`llama-3.1-8b-instant`)
* **Environment**: `python-dotenv`
* **Package Manager**: [uv](https://github.com/astral-sh/uv)

---

## 📁 Project Structure

```text
linkedin-post-agent/
├── src/
│   └── linkedin_post_agent/
│       ├── __init__.py      # Package initializer
│       ├── config.py        # Environment & configuration loader
│       ├── graph.py         # LangGraph workflow definition & compilation
│       ├── nodes.py         # Graph node implementations (generate, review, feedback, post)
│       ├── router.py        # Conditional routing logic for human approval
│       └── main.py          # CLI entry point
├── .env.example             # Template for required environment variables
├── .gitignore                # Git exclusion rules
├── pyproject.toml           # Hatch & uv project metadata
├── uv.lock                  # Lockfile for dependency reproducibility
├── README.md                # Project documentation
└── LICENSE                  # MIT License
```

---

## ⚙️ Quick Start

### 1. Prerequisites
Ensure you have **Python 3.11+** and **`uv`** installed.
```bash
# Install uv if not already present
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Installation
Clone the repository and enter the directory:
```bash
git clone https://github.com/Bin-Naji/linkedin-post-agent.git
cd linkedin-post-agent
```

Install dependencies using `uv`:
```bash
uv sync
```

### 3. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Add your **Groq API Key** in `.env`:
```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

> ⚠️ **Security Note:** Never commit `.env` to Git. It is automatically ignored by `.gitignore`.

---

## 💻 Usage

Run the agent via `uv`:
```bash
uv run python -m linkedin_post_agent.main
```

### Example Interaction

```text
============================================================
GENERATED LINKEDIN POST
============================================================

🚀 AI Agents are revolutionizing content creation!

Instead of replaces creators, autonomous agents act as 
collaborative drafting partners...

============================================================

Approve this post? (yes/no): no

What would you like me to improve?
> Make it shorter, add 3 relevant hashtags, and end with a question.

============================================================
GENERATED LINKEDIN POST
============================================================

🤖 AI Agents aren't replacing creators—they're supercharging them!

By handling initial drafts and revision cycles, human-in-the-loop 
workflows elevate content quality.

What's your take on AI-assisted writing? 

#AIAgents #LangGraph #ContentCreation

============================================================

Approve this post? (yes/no): yes

============================================================
FINAL LINKEDIN POST
============================================================
...
✅ Post published successfully!
```

---

## 🧠 Core Concepts & Patterns

### 1. State-Driven Iteration
The state is typed with `MessagesState`. Every node receives the full array of prior messages, allowing the model to see:
1. User's initial prompt
2. Previous LLM draft
3. User's feedback
4. Revised LLM response

### 2. Clean Node & Router Separation
Nodes are pure or side-effect functions handling isolated steps:
* `generate_post`: Invokes `ChatGroq` with `state["messages"]`.
* `review_post`: Displays draft to stdout.
* `review_router`: Evaluates interactive user input to return `"post"` or `"feedback"`.
* `get_feedback`: Captures revision instructions as a new `HumanMessage`.
* `publish_post`: Finalizes output.

---

## 🔮 Future Roadmap

- [ ] Add LangGraph persistence checkpointing (`MemorySaver` / SQLite).
- [ ] Implement a Streamlit or Next.js UI interface.
- [ ] Direct LinkedIn API posting integration.
- [ ] Multi-turn tone & length parameter controls.
- [ ] Automated post quality assessment node.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).