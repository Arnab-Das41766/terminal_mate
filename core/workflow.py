"""
Workflow Engine for multi-step tasks
"""
import os
from dataclasses import dataclass
from typing import List, Callable, Optional


import sys
import os

# Add project root to path so we can import 'core' packages
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from rich.console import Console
from core.executor import CommandExecutor

@dataclass
class WorkflowStep:
    name: str
    command: str
    description: str = ""


@dataclass
class Workflow:
    name: str
    triggers: List[str]
    steps: List[WorkflowStep]
    description: str = ""


class WorkflowEngine:
    def __init__(self):
        self.workflows = self._load_workflows()
    
    def _load_workflows(self) -> List[Workflow]:
        """Load built-in workflows"""
        return [
            Workflow(
                name="Standard Project Setup",
                triggers=[
                    "create my standard project setup",
                    "setup standard project",
                    "init standard project"
                ],
                description="Creates a standard project structure with src, tests, docs, and git init",
                steps=[
                    WorkflowStep(
                        name="Create Directories",
                        command="mkdir src tests docs",
                        description="Creating folders: src, tests, docs"
                    ),
                    WorkflowStep(
                        name="Create README",
                        command="echo # Project > README.md",
                        description="Creating README.md"
                    ),
                    WorkflowStep(
                        name="Create Gitignore",
                        command="echo __pycache__/ > .gitignore",
                        description="Creating .gitignore"
                    ),
                    WorkflowStep(
                        name="Initialize Git",
                        command="git init",
                        description="Initializing git"
                    )
                ]
            )
        ]
    
    def find_workflow(self, user_input: str) -> Optional[Workflow]:
        """Find a workflow matching the user input"""
        normalized_input = user_input.lower().strip()
        for workflow in self.workflows:
            for trigger in workflow.triggers:
                if trigger in normalized_input:
                    return workflow
        return None
    
    def execute_workflow(self, workflow: Workflow, executor, console):
        """Execute a workflow"""
        console.print(f"[bold cyan]Running workflow: {workflow.name}[/bold cyan]")
        
        success = True
        for step in workflow.steps:
            console.print(f"  • {step.description}...", end=" ")
            
            # Execute command
            result = executor.execute(step.command)
            
            if result['success']:
                console.print("[green]DONE[/green]")
            else:
                console.print("[red]FAILED[/red]")
                console.print(f"    [red]Error: {result['error']}[/red]")
                success = False
                break
        
        if success:
            console.print(f"\n[bold green]Workflow '{workflow.name}' completed successfully![/bold green]\n")
        else:
            console.print(f"\n[bold red]Workflow '{workflow.name}' failed.[/bold red]\n")
        
        return success

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="TerminalMate Workflow Runner")
    parser.add_argument("name", help="Name of the workflow to run")
    args = parser.parse_args()
    
    # Initialize components
    console = Console()
    executor = CommandExecutor()
    engine = WorkflowEngine()
    
    # Find and execute workflow
    workflow = None
    for w in engine.workflows:
        if w.name.lower() == args.name.lower():
            workflow = w
            break
            
    if not workflow:
        # Fallback: try finding by trigger/loose match
        workflow = engine.find_workflow(args.name)
        
    if workflow:
        engine.execute_workflow(workflow, executor, console)
    else:
        console.print(f"[red]Error: Workflow '{args.name}' not found.[/red]")
        sys.exit(1)
