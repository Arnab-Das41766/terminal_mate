# TerminalMate 🤖

**TerminalMate** is your AI-powered terminal assistant, designed to translate natural language into safe, executable terminal commands. Powered by **Qwen 2.5 Coder**, it helps you manage files, run scripts, and automate workflows with ease.

## ✨ Features

- **Natural Language Commands**: Just say what you want to do (e.g., "create a project folder", "find large files").
- **Safety First**:
  - ✅ **SAFE**: Read-only commands run automatically.
  - ⚠️ **CAUTION**: File modifications require confirmation.
  - 🚨 **CRITICAL**: Dangerous operations need explicit approval.
- **Workflow Automation**: dedicated workflows for common tasks like project setup.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

## 📂 Project Structure

```
terminalmate/
├── core/           # Core logic (LLM engine, executor, workflow)
├── safety/         # Risk analysis and confirmation UI
├── ui/             # User interface components
├── utils/          # Utility functions
├── config.py       # Configuration settings
├── main.py         # Main entry point
├── setup.py        # Automated setup script
└── requirements.txt # Project dependencies
```

## 🚀 Installation

### 1. Prerequisites
TerminalMate uses **Ollama** to run the local LLM.
- **Install Ollama**: Download from [ollama.ai](https://ollama.ai)
- **Pull the Model**:
  ```bash
  ollama pull qwen2.5-coder:7b
  ```

### 2. Clone the Repository
```bash
git clone https://github.com/Arnab-Das41766/terminal_mate.git
cd terminalmate
```

### 3. Run Setup Script
The setup script will create necessary directories and install Python dependencies.
```bash
python setup.py
```
*Note: This script will verify your Ollama installation, create the project structure if needed, and run `pip install -r requirements.txt`.*

## 🎮 Usage

Start the assistant by running:

```bash
python main.py
```

### How to Use
1.  **Type your request**: Just type what you want to do in plain English.
2.  **Review the plan**: TerminalMate will show you the command it intends to run and its risk level.
3.  **Confirm**: Type `y` or `yes` to execute.

### Examples

- **File Management**:
  > "List all Python files in the current folder"
  > "Create a new directory called 'data' and move all csv files there"

- **System Info**:
  > "Show my current disk usage"
  > "What is my IP address?"

- **Workflows**:
  > "Create a standard project setup"
  *(This runs a predefined workflow to scaffold a new project)*

## 🛠️ Workflows

You can also run built-in workflows directly from the CLI without starting the interactive session:

```bash
python core/workflow.py "Standard Project Setup"
```

## 🤝 Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.
