"""
Risk Analyzer - Classifies commands as SAFE, CAUTION, or CRITICAL
"""
import config


class RiskAnalyzer:
    def __init__(self):
        self.critical_keywords = config.CRITICAL_KEYWORDS
        self.caution_keywords = config.CAUTION_KEYWORDS
        
    def analyze_command(self, command):
        """
        Analyze a command and return its risk level
        
        Args:
            command (str): The command to analyze
            
        Returns:
            dict: {
                'risk_level': str (SAFE/CAUTION/CRITICAL),
                'reason': str,
                'warnings': list
            }
        """
        command_lower = command.lower()
        warnings = []
        
        # Check for critical operations
        for keyword in self.critical_keywords:
            if keyword in command_lower:
                warnings.append(f"Contains dangerous operation: '{keyword}'")
                return {
                    'risk_level': config.RISK_CRITICAL,
                    'reason': f"Command contains critical operation: {keyword}",
                    'warnings': warnings
                }
        
        # Check for caution-level operations
        for keyword in self.caution_keywords:
            if keyword in command_lower:
                warnings.append(f"Modifies system state: '{keyword}'")
                return {
                    'risk_level': config.RISK_CAUTION,
                    'reason': f"Command will modify files or system: {keyword}",
                    'warnings': warnings
                }
        
        # Safe operations (read-only)
        safe_commands = ['ls', 'dir', 'cat', 'type', 'echo', 'pwd', 'cd', 
                        'whoami', 'date', 'time', 'help', 'man', 'find', 'grep']
        
        first_word = command_lower.split()[0] if command_lower.split() else ""
        if any(first_word == safe_cmd for safe_cmd in safe_commands):
            return {
                'risk_level': config.RISK_SAFE,
                'reason': "Read-only operation",
                'warnings': []
            }
        
        # Default to CAUTION for unknown commands
        return {
            'risk_level': config.RISK_CAUTION,
            'reason': "Unknown command - proceed with caution",
            'warnings': ['Command not recognized as safe']
        }
    
    def get_risk_color(self, risk_level):
        """Get color code for risk level"""
        colors = {
            config.RISK_SAFE: 'green',
            config.RISK_CAUTION: 'yellow',
            config.RISK_CRITICAL: 'red'
        }
        return colors.get(risk_level, 'white')
    
    def get_risk_emoji(self, risk_level):
        """Get emoji for risk level"""
        emojis = {
            config.RISK_SAFE: '✅',
            config.RISK_CAUTION: '⚠️',
            config.RISK_CRITICAL: '🚨'
        }
        return emojis.get(risk_level, '❓')