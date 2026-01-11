"""
LLM Engine for interacting with Ollama models
"""
import ollama
import os
import config


class LLMEngine:
    def __init__(self, model_name=None):
        self.model_name = model_name or config.LLM_MODEL
        self.conversation_history = []
        
    def generate_command(self, user_input, context=None):
        """
        Generate a terminal command from natural language input
        
        Args:
            user_input (str): Natural language request
            context (dict): Optional context (current directory, previous commands, etc.)
            
        Returns:
            dict: {
                'command': str,
                'explanation': str,
                'confidence': float
            }
        """
        # Build the prompt
        prompt = self._build_prompt(user_input, context)
        
        try:
            # Call Ollama
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': self._get_system_prompt()
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': config.LLM_TEMPERATURE,
                }
            )
            
            # Parse response
            result = self._parse_response(response['message']['content'])
            return result
            
        except Exception as e:
            return {
                'command': None,
                'explanation': f"Error generating command: {str(e)}",
                'confidence': 0.0,
                'error': True
            }
    
    def _get_system_prompt(self):
        """Get the system prompt based on current OS and shell"""
        os_info = f"OS: {config.CURRENT_OS}, Shell: {config.SHELL_TYPE}"
        
        return rf"""You are a terminal command generator assistant. Your job is to convert natural language requests into proper terminal commands.

{os_info}

CRITICAL RULES:
1. Output ONLY the command, nothing else
2. Generate commands appropriate for the current OS and shell
3. Be precise and safe - avoid destructive commands unless explicitly requested
4. If the request is ambiguous, generate the most likely safe interpretation
5. Use standard command syntax and flags
7. ** INTELLIGENT SEARCHING **: If the user asks to "find", "search", or "list" files, assume they might need a recursive search (e.g., `dir /s` or `find . -name`) if specific paths aren't given.
8. ** PATH RESOLUTION **: ALWAYS use the absolute paths provided in the "SYSTEM PATHS" section (e.g., for Desktop, Downloads) instead of trying to guess relative paths like `..\Desktop`.
9. ** VALID SYNTAX ONLY **: Do NOT use English conjunctions like "OR" or "AND" in commands. Use proper shell syntax for multiple arguments (e.g., `dir *.jpg *.png`, NOT `dir *.jpg OR *.png`).

9. ** WINDOWS SEARCH **: On Windows, use PowerShell for multiple file patterns. Example: `powershell -c "Get-ChildItem -Path '..' -Recurse -Include '*.jpg','*.png' | Select-Object -ExpandProperty FullName"` instead of `dir`.
10. ** SPECIFICITY **: If the user asks for a specific type (e.g. "images"), do NOT use generic wildcards like `*arnab*`. You MUST search for extensions: `*arnab*.jpg`, `*arnab*.png`.
11. ** FUZZY MATCHING **: When searching for a specific filename (e.g., "instruction"), ALWAYS add a wildcard suffix `*` to catch plurals or partial matches (e.g., use `instruction*.*` instead of `instruction.*`).
12. ** DIRECTORY SEARCH **: If the user specifically asks to find a "folder" or "directory", YOU MUST use `dir /ad` (Attribute Directory) to filter results. Example: `dir /ad /s /b "...\*foldername*"`
13. ** QUOTE PATHS **: You MUST enclose ALL file paths and directory names in double quotes to handle spaces correctly. Example: `cd "C:\Users\Arnab Das\Desktop"` instead of `cd C:\Users\Arnab Das\Desktop`.

FORMAT YOUR RESPONSE EXACTLY AS:
COMMAND: <the actual command here>
EXPLANATION: <brief explanation of what it does>

Example 1 (Recursive Search):
User: find all pdfs
COMMAND: dir /s /b *.pdf
EXPLANATION: Recursively lists all .pdf files in the current folder and subfolders.

Example 2 (Desktop Access):
User: list files on desktop
COMMAND: dir "..\*"
EXPLANATION: Lists files in the parent directory (Desktop).

Example 3 (Find in Desktop):
User: find CV in desktop
COMMAND: dir /s /b "..\*CV*"
EXPLANATION: Recursively searches for "CV" starting from the Desktop (parent folder).

Example 4 (Wi-Fi Password):
User: get wifi password for MyNetwork
COMMAND: netsh wlan show profile name="MyNetwork" key=clear
EXPLANATION: Retrieves the saved Wi-Fi profile and shows the password (key content).

Example 5 (Kill Process):
User: kill chrome
COMMAND: powershell -c "Stop-Process -Name *chrome* -Force"
EXPLANATION: Forcefully terminates any process containing "chrome" in its name.

Example 6 (System Info):
User: what is my ip
COMMAND: ipconfig
Example 7 (Open VS Code):
User: open vs code in this directory
COMMAND: code .
EXPLANATION: Opens the current directory in Visual Studio Code (requires 'code' in PATH).

Example 8 (Standard Project Setup):
User: create a new standard project named "MyNewApp"
COMMAND: mkdir MyNewApp && cd MyNewApp && python -m core.workflow "Standard Project Setup"
EXPLANATION: Creates the folder, enters it, and runs the standard project setup workflow."""
    
    def _build_prompt(self, user_input, context):
        """Build the prompt with context"""
        prompt = f"User request: {user_input}\n"
        
        # Add standard paths info
        user_home = os.path.expanduser("~")
        prompt += f"\nSYSTEM PATHS:\n"
        prompt += f"Home: {user_home}\n"
        prompt += f"Downloads: {os.path.join(user_home, 'Downloads')}\n"
        prompt += f"Desktop: {os.path.join(user_home, 'Desktop')}\n"
        
        if context:
            if 'current_dir' in context:
                prompt += f"Current directory: {context['current_dir']}\n"
                    
            if 'previous_command' in context:
                prompt += f"Previous command: {context['previous_command']}\n"
            
            # Add recent history for conversational context
            if 'recent_history' in context and context['recent_history']:
                prompt += "\nRECENT CONVERSATION HISTORY:\n"
                for item in context['recent_history'][-3:]:  # Last 3 items
                    prompt += f"User: {item['input']}\n"
                    prompt += f"Command Executed: {item['command']}\n"
                    if item.get('output'):
                        # Truncate output if too long
                        output_snippet = item['output'][:200] + "..." if len(item['output']) > 200 else item['output']
                        prompt += f"Command Output: {output_snippet}\n"
                    prompt += "---\n"
        
        if "standard project" in user_input.lower():
            if context and 'app_root' in context:
                workflow_script = os.path.join(context['app_root'], 'core', 'workflow.py')
                # Escape backslashes for string usage if needed, or just rely on python string handling
                prompt += f'\nIMPORTANT: You MUST append `&& python "{workflow_script}" "Standard Project Setup"` after creating and entering the directory. Do NOT just create the folder.'
            else:
                prompt += '\nIMPORTANT: You MUST append `&& python -m core.workflow "Standard Project Setup"` after creating and entering the directory.'
        
        return prompt
    
    def _parse_response(self, response_text):
        """Parse the LLM response to extract command and explanation"""
        lines = response_text.strip().split('\n')
        command = None
        explanation = ""
        
        for line in lines:
            if line.startswith("COMMAND:"):
                command = line.replace("COMMAND:", "").strip()
            elif line.startswith("EXPLANATION:"):
                explanation = line.replace("EXPLANATION:", "").strip()
        
        # Fallback: if format not followed, treat entire response as command
        if not command:
            command = response_text.strip()
            explanation = "Command generated from natural language"
        
        return {
            'command': command,
            'explanation': explanation,
            'confidence': 0.9,  # Qwen is quite reliable
            'error': False
        }
    
    def chat(self, user_message):
        """Have a conversation with the AI (for clarifications)"""
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {'role': 'system', 'content': 'You are a helpful terminal assistant. Answer questions about commands clearly and concisely.'},
                    {'role': 'user', 'content': user_message}
                ]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"