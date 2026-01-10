"""
Confirmation UI - Handles user confirmation for command execution
"""
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import config


class ConfirmationUI:
    def __init__(self):
        self.console = Console()
    
    def show_command_preview(self, command_info, risk_info):
        """
        Display command preview with risk assessment
        
        Args:
            command_info (dict): Command and explanation from LLM
            risk_info (dict): Risk analysis results
            
        Returns:
            bool: True if user confirms, False otherwise
        """
        risk_level = risk_info['risk_level']
        
        # Color based on risk
        color_map = {
            config.RISK_SAFE: 'green',
            config.RISK_CAUTION: 'yellow',
            config.RISK_CRITICAL: 'red'
        }
        color = color_map.get(risk_level, 'white')
        
        # Emoji based on risk
        emoji_map = {
            config.RISK_SAFE: '✅',
            config.RISK_CAUTION: '⚠️',
            config.RISK_CRITICAL: '🚨'
        }
        emoji = emoji_map.get(risk_level, '❓')
        
        # Build display text
        display_text = f"""[bold]{emoji} Risk Level: {risk_level}[/bold]

[bold cyan]Command:[/bold cyan]
[{color}]{command_info['command']}[/{color}]

[bold cyan]What it does:[/bold cyan]
{command_info['explanation']}

[bold cyan]Risk Assessment:[/bold cyan]
{risk_info['reason']}
"""
        
        # Add warnings if any
        if risk_info['warnings']:
            display_text += f"\n[bold red]⚠️  Warnings:[/bold red]\n"
            for warning in risk_info['warnings']:
                display_text += f"  • {warning}\n"
        
        # Show panel
        self.console.print(Panel(display_text, border_style=color, title="Command Preview"))
        
        # Get confirmation based on risk level
        if risk_level == config.RISK_CRITICAL:
            return self._get_critical_confirmation()
        elif risk_level == config.RISK_CAUTION:
            return self._get_caution_confirmation()
        else:  # SAFE
            if config.AUTO_EXECUTE_SAFE_COMMANDS:
                self.console.print("[green]✓ Executing safe command...[/green]")
                return True
            return self._get_safe_confirmation()
    
    def _get_safe_confirmation(self):
        """Quick confirmation for safe commands"""
        response = Prompt.ask(
            "\n[green]Execute this command?[/green]",
            choices=["y", "n", "yes", "no"],
            default="y"
        )
        return response.lower() in ["y", "yes"]
    
    def _get_caution_confirmation(self):
        """Standard confirmation for caution-level commands"""
        response = Prompt.ask(
            "\n[yellow]⚠️  This command will modify your system. Proceed?[/yellow]",
            choices=["y", "n", "yes", "no"],
            default="n"
        )
        return response.lower() in ["y", "yes"]
    
    def _get_critical_confirmation(self):
        """Strict confirmation for critical commands"""
        self.console.print("\n[bold red]🚨 CRITICAL OPERATION - This command could cause data loss or system damage![/bold red]")
        
        # First confirmation
        response1 = Prompt.ask(
            "[red]Are you absolutely sure you want to execute this?[/red]",
            choices=["yes", "no"],
            default="no"
        )
        
        if response1.lower() not in ["y", "yes"]:
            return False
        
        # Second confirmation
        response2 = Prompt.ask(
            "[red]Type 'y' or 'CONFIRM' to proceed[/red]"
        )
        
        return response2.lower() in ["y", "yes", "confirm"]
    
    def show_execution_result(self, success, output, error=None):
        """Display command execution results"""
        if success:
            self.console.print("\n[green]✓ Command executed successfully[/green]")
            if output:
                self.console.print("\n[bold]Output:[/bold]")
                self.console.print(output)
        else:
            self.console.print("\n[red]✗ Command failed[/red]")
            if error:
                self.console.print(f"[red]Error: {error}[/red]")
    
    def show_cancellation(self):
        """Show cancellation message"""
        self.console.print("\n[yellow]Command cancelled by user[/yellow]")