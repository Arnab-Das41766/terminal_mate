"""
Command Executor - Safely executes terminal commands
"""
import subprocess
import os
import config


class CommandExecutor:
    def __init__(self):
        self.current_dir = os.getcwd()
        
    def execute(self, command):
        """
        Execute a command and return results
        
        Args:
            command (str): Command to execute
            
        Returns:
            dict: {
                'success': bool,
                'output': str,
                'error': str,
                'return_code': int
            }
        """
        try:
            # Determine shell based on OS
            if config.IS_WINDOWS:
                shell = True
                executable = None
            else:
                shell = True
                executable = '/bin/bash'
            
            # Execute command
            process = subprocess.Popen(
                command,
                shell=shell,
                executable=executable,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.current_dir
            )
            
            # Get output
            stdout, stderr = process.communicate(timeout=config.COMMAND_TIMEOUT)
            
            # Check if command changed directory
            if command.strip().startswith('cd '):
                self._handle_cd_command(command)
            
            # Special handling for explorer command which determines success differently
            # Explorer often returns 1 but works fine if no stderr
            success = process.returncode == 0
            if not success and command.strip().lower().startswith('explorer ') and not stderr.strip():
                success = True
            
            return {
                'success': success,
                'output': stdout.strip(),
                'error': stderr.strip() if stderr else None,
                'return_code': process.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'output': '',
                'error': f'Command timed out after {config.COMMAND_TIMEOUT} seconds',
                'return_code': -1
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'return_code': -1
            }
    
    def _handle_cd_command(self, command):
        """Handle directory change commands"""
        try:
            # Extract path from cd command
            parts = command.strip().split(maxsplit=1)
            if len(parts) > 1:
                new_dir = parts[1].strip().strip('"').strip("'")
                
                # Expand ~ to home directory
                if new_dir.startswith('~'):
                    new_dir = os.path.expanduser(new_dir)
                
                # Handle relative paths
                if not os.path.isabs(new_dir):
                    new_dir = os.path.join(self.current_dir, new_dir)
                
                # Change directory if it exists
                if os.path.isdir(new_dir):
                    self.current_dir = os.path.abspath(new_dir)
                    os.chdir(self.current_dir)
        except Exception:
            pass  # If cd fails, keep current directory
    
    def get_current_directory(self):
        """Get current working directory"""
        return self.current_dir
    
    def validate_command(self, command):
        """
        Basic validation of command syntax
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not command or not command.strip():
            return False, "Empty command"
        
        # Check for command injection attempts
        dangerous_chars = [';', '&&', '||', '|', '`', '$()']
        if any(char in command for char in dangerous_chars):
            # Allow these in certain contexts but warn
            return True, "Warning: Command contains chaining operators"
        
        return True, None