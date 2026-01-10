# TerminalMate 🤖

**TerminalMate** is your intelligent, AI-powered terminal assistant. It bridges the gap between natural language and complex shell commands, allowing you to control your system using plain English. Powered by the **Qwen 2.5 Coder** model (via Ollama), it ensures accuracy while prioritizing safety with built-in risk analysis.

## ✨ Features

- **🗣️ Natural Language Control**: Type what you want to do (e.g., "Find all large video files"), and TerminalMate generates the correct command.
- **🛡️ Safety First**:
    - **Risk Analysis**: automatically classifies commands as `SAFE`, `CAUTION`, or `CRITICAL`.
    - **Confirmation UI**: Dangerous commands require explicit user approval.
- **💻 Cross-Platform**: Works seamlessly on **Windows**, **Linux**, and **macOS**.
- **🧠 Context Aware**: Understands your current directory and previous interactions.
- **🎨 Beautiful UI**: Rich, color-coded interface for a premium user experience.

---

## 🚀 Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
2.  **Ollama**: [Download Ollama](https://ollama.ai/download)
3.  **Qwen 2.5 Coder Model**:
    ```bash
    ollama pull qwen2.5-coder:7b
    ```

---

## 📦 Installation

1.  **Clone or Download** the project to your local machine.
2.  **Navigate** to the project directory:
    ```bash
    cd terminalmate
    ```
3.  **Run the Setup Script**:
    This script will check your environment, install dependencies, and verify everything is ready.
    ```bash
    python setup.py
    ```

    *Alternatively, you can install dependencies manually:*
    ```bash
    pip install -r requirements.txt
    ```

---

## 🎮 Usage

Start the assistant by running:

```bash
python main.py
```

### Examples

Once inside TerminalMate, you can try commands like:

-   **File Management**:
    > "Create a new folder called 'ProjectDocs' and move all PDF files into it."
-   **System Info**:
    > "Show me the top 5 processes using the most memory."
-   **Searching**:
    > "Find all files named 'config' modified in the last 24 hours."
-   **Navigation**:
    > "Go to the parent directory."

### Special Commands
-   `help` / `?`: Show the help menu.
-   `clear`: Clear the screen.
-   `pwd`: Show current working directory.
-   `exit` / `quit`: Close TerminalMate.

---

## 📂 Project Structure

Here is an overview of the file structure to help you understand how TerminalMate is organized:

```text
terminalmate/
├── core/
│   ├── llm_engine.py       # Handles communication with Ollama (Qwen model)
│   ├── executor.py         # Validates and executes system commands
│   └── __init__.py
├── safety/
│   ├── risk_analyzer.py    # Analyzes commands for potential security risks
│   ├── confirmation.py     # UI for confirming dangerous actions
│   └── __init__.py
├── ui/
│   └── __init__.py         # UI styling and display components
├── utils/
│   └── __init__.py         # Helper utilities
├── config.py               # Configuration settings (Model, Risk Levels, etc.)
├── main.py                 # Application entry point
├── setup.py                # Automated setup script
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## ⚙️ Configuration

You can customize TerminalMate by editing `config.py`:

-   **`LLM_MODEL`**: Change the Ollama model used (default: `qwen2.5-coder:7b`).
-   **`ENABLE_SAFETY_CHECKS`**: Toggle safety analysis (Recommended: `True`).
-   **`REQUIRE_CONFIRMATION_FOR_CRITICAL`**: Enforce checks for dangerous commands.
-   **`RISK_CRITICAL` / `RISK_CAUTION`**: Customize which keywords trigger alerts.

---

## 🤝 Contributing

Feel free to fork this project and submit pull requests! Suggestions and improvements are always welcome.
