"""
TerminalMate - AI-Powered Terminal Assistant
Main application entry point
"""
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.llm_engine import LLMEngine
from core.executor import CommandExecutor
from core.workflow import WorkflowEngine
from safety.risk_analyzer import RiskAnalyzer
from safety.confirmation import ConfirmationUI
import config


class TerminalMate:
    def __init__(self):
        self.console = Console()
        self.llm = LLMEngine()
        self.executor = CommandExecutor()
        self.workflow_engine = WorkflowEngine()
        self.risk_analyzer = RiskAnalyzer()
        self.confirmation_ui = ConfirmationUI()
        self.history = []  # Store recent conversation history
        self.running = True
        
    def start(self):
        """Start the TerminalMate interactive session"""
        self.show_welcome()
        
        while self.running:
            try:
                # Get user input
                user_input = self.get_user_input()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if self.handle_special_commands(user_input):
                    continue
                
                # Generate command from natural language
                self.process_request(user_input)
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Goodbye! 👋[/yellow]")
                self.running = False
            except Exception as e:
                self.console.print(f"\n[red]Error: {str(e)}[/red]")
    
    def show_welcome(self):
        """Display welcome message"""
        welcome_text = """[bold cyan]Welcome to TerminalMate! 🤖[/bold cyan]

Your AI-powered terminal assistant using [bold]Qwen 2.5 Coder[/bold]

[bold]How to use:[/bold]
• Type commands in natural language (e.g., "list all text files")
• I'll convert them to terminal commands and ask for confirmation
• Type [yellow]'help'[/yellow] for more info or [yellow]'exit'[/yellow] to quit

[bold green]Current System:[/bold green]
• OS: {os}
• Shell: {shell}
• Directory: {dir}
""".format(
            os=config.CURRENT_OS.title(),
            shell=config.SHELL_TYPE,
            dir=self.executor.get_current_directory()
        )
        
        self.console.print(Panel(welcome_text, border_style="cyan"))
    
    def get_user_input(self):
        """Get input from user"""
        current_dir = os.path.basename(self.executor.get_current_directory())
        prompt_text = f"\n[bold cyan]{current_dir}>[/bold cyan] "
        
        try:
            user_input = Prompt.ask(prompt_text)
            return user_input.strip()
        except EOFError:
            self.running = False
            return None
    
    def handle_special_commands(self, user_input):
        """Handle special built-in commands"""
        lower_input = user_input.lower()
        
        if lower_input in ['exit', 'quit', 'q']:
            self.console.print("[cyan]Goodbye! 👋[/cyan]")
            self.running = False
            return True
        
        elif lower_input in ['help', '?']:
            self.show_help()
            return True
        
        elif lower_input == 'clear':
            os.system('cls' if config.IS_WINDOWS else 'clear')
            return True
        
        elif lower_input == 'pwd':
            self.console.print(f"[cyan]{self.executor.get_current_directory()}[/cyan]")
            return True
        
        return False
    
    def show_help(self):
        """Show help information"""
        help_text = """[bold]TerminalMate Commands:[/bold]

[bold cyan]Natural Language Examples:[/bold cyan]
• "list all files in this directory"
• "find Python files modified today"
• "show disk usage"
• "create a folder called projects"
• "delete all .tmp files" (⚠️ will ask for confirmation)

[bold cyan]Special Commands:[/bold cyan]
• [yellow]help[/yellow] - Show this help message
• [yellow]clear[/yellow] - Clear the screen
• [yellow]pwd[/yellow] - Show current directory
• [yellow]exit/quit[/yellow] - Exit TerminalMate

[bold cyan]Safety Features:[/bold cyan]
• ✅ [green]SAFE[/green] - Read-only commands (auto-executed)
• ⚠️  [yellow]CAUTION[/yellow] - File modifications (requires confirmation)
• 🚨 [red]CRITICAL[/red] - Dangerous operations (strict confirmation)
"""
        self.console.print(Panel(help_text, border_style="cyan", title="Help"))
    
    def process_request(self, user_input):
        """Process a natural language request"""
        # Show processing message
        with self.console.status("[cyan]🤔 Thinking...[/cyan]"):
            # Get context
            context = {
                'current_dir': self.executor.get_current_directory(),
                'os': config.CURRENT_OS,
                'shell': config.SHELL_TYPE,
                'app_root': os.path.dirname(os.path.abspath(__file__)),
                'recent_history': self.history
            }
            
            # Generate command using LLM
            command_info = self.llm.generate_command(user_input, context)
        
        # Check for errors
        if command_info.get('error'):
            self.console.print(f"[red]Error: {command_info['explanation']}[/red]")
            return
        
        # Validate command
        is_valid, validation_msg = self.executor.validate_command(command_info['command'])
        if not is_valid:
            self.console.print(f"[red]Invalid command: {validation_msg}[/red]")
            return
        
        # Analyze risk
        risk_info = self.risk_analyzer.analyze_command(command_info['command'])
        
        # Show preview and get confirmation
        if self.confirmation_ui.show_command_preview(command_info, risk_info):
            # Execute command
            self.execute_command(command_info['command'], user_input)
        else:
            self.confirmation_ui.show_cancellation()
    
    def execute_command(self, command, user_input=""):
        """Execute a confirmed command"""
        with self.console.status("[cyan]⚙️  Executing...[/cyan]"):
            result = self.executor.execute(command)
        
        # Update history
        self.history.append({
            'input': user_input,
            'command': command,
            'output': result['output'] or result['error'] or "No output"
        })
        
        # Keep history size manageable
        if len(self.history) > 5:
            self.history.pop(0)
            
        # Show results
        self.confirmation_ui.show_execution_result(
            result['success'],
            result['output'],
            result['error']
        )


def main():
    """Main entry point"""
    try:
        app = TerminalMate()
        app.start()
    except Exception as e:
        console = Console()
        console.print(f"[red]Fatal error: {str(e)}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()