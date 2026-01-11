"""
Configuration settings for TerminalMate
"""
import os
import platform

# LLM Settings
LLM_MODEL = "qwen2.5-coder:7b"  # Using your existing Qwen model
LLM_TEMPERATURE = 0.1  # Low temperature for consistent command generation
LLM_TIMEOUT = 10  # Seconds to wait for LLM response
COMMAND_TIMEOUT = 60  # Seconds to wait for command execution (1 minute)

# Platform Detection
CURRENT_OS = platform.system().lower()  # 'windows', 'linux', 'darwin' (macOS)
IS_WINDOWS = CURRENT_OS == "windows"
IS_UNIX = CURRENT_OS in ["linux", "darwin"]

# Shell Detection
if IS_WINDOWS:
    SHELL_TYPE = "cmd"
else:
    SHELL_TYPE = os.environ.get("SHELL", "/bin/bash").split("/")[-1]

# Safety Settings
ENABLE_SAFETY_CHECKS = True
REQUIRE_CONFIRMATION_FOR_CRITICAL = True
AUTO_EXECUTE_SAFE_COMMANDS = False  # Set to True to skip confirmation for safe commands

# Risk Levels
RISK_SAFE = "SAFE"
RISK_CAUTION = "CAUTION"
RISK_CRITICAL = "CRITICAL"

# Critical Command Keywords
CRITICAL_KEYWORDS = [
    # Deletion
    "rm -rf", "rm -r", "del /f", "del /s", "rmdir /s", "shred",
    # System modifications
    "chmod 777", "chown", "chmod -R", "format", "mkfs",
    # Network
    "iptables", "ufw delete", "firewall",
    # Process termination
    "kill -9", "killall", "taskkill /f", "pkill",
    # Registry (Windows)
    "reg delete", "reg add",
    # Disk operations
    "dd if=", "fdisk", "parted",
    # Package management (can break system)
    "apt-get remove", "yum remove", "brew uninstall --force",
    # Sudo operations
    "sudo rm", "sudo chmod", "sudo chown"
]

CAUTION_KEYWORDS = [
    "mv", "move", "cp -r", "xcopy", "mkdir", "touch",
    "echo >", "cat >", "chmod", "chown", "kill", "taskkill"
]

# Logging
ENABLE_LOGGING = True
LOG_FILE = "terminalmate.log"
LOG_COMMANDS = True  # Log all executed commands

# UI Settings
USE_COLOR = True
SHOW_COMMAND_EXPLANATION = True
PROMPT_SYMBOL = "🤖 TerminalMate>"