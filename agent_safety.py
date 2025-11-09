"""
Safety and Permissions System
Protects against dangerous operations and requires user approval
"""

import json
from pathlib import Path
from typing import Optional, Tuple
from colorama import Fore, Style, init

init(autoreset=True)


class SafetySystem:
    """Safety system for controlling dangerous operations"""
    
    # Dangerous patterns that require approval
    DANGEROUS_PATTERNS = [
        # File operations
        r'rm\s+-rf',
        r'rmdir\s+/s',
        r'del\s+/f',
        r'format\s+',
        # System operations
        r'shutdown',
        r'restart',
        r'reboot',
        r'registry',
        # Network operations
        r'curl.*\|\s*bash',
        r'wget.*\|\s*sh',
        # Installation
        r'npm\s+install\s+-g',
        r'pip\s+install.*--force',
    ]
    
    # Critical directories that are protected
    PROTECTED_DIRS = [
        'C:\\Windows',
        'C:\\Program Files',
        'C:\\Program Files (x86)',
        '/System',
        '/Windows',
        '/usr',
        '/bin',
        '/sbin',
    ]
    
    def __init__(self, config_file: str = "./agent_config.json"):
        """Initialize safety system"""
        self.config_file = Path(config_file)
        self.auto_approve = False
        self.approval_history = []
        self._load_config()
    
    def _load_config(self):
        """Load safety configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.auto_approve = config.get('auto_approve', False)
            except:
                pass
    
    def _save_config(self):
        """Save safety configuration"""
        config = {
            'auto_approve': self.auto_approve,
            'version': '1.0'
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def check_operation(self, operation: str, details: str) -> Tuple[bool, Optional[str]]:
        """
        Check if an operation is safe
        Returns: (is_approved, reason)
        """
        # Check for dangerous patterns
        import re
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, details, re.IGNORECASE):
                return self._request_approval(
                    operation,
                    details,
                    f"Contains dangerous pattern: {pattern}"
                )
        
        # Check for protected directories
        for protected_dir in self.PROTECTED_DIRS:
            if protected_dir.lower() in details.lower():
                return self._request_approval(
                    operation,
                    details,
                    f"Affects protected directory: {protected_dir}"
                )
        
        # Check operation type
        if operation in ['delete', 'terminal_command']:
            return self._request_approval(
                operation,
                details,
                f"Potentially destructive operation: {operation}"
            )
        
        # Safe by default
        return True, None
    
    def _request_approval(self, operation: str, details: str, reason: str) -> Tuple[bool, Optional[str]]:
        """Request user approval for potentially dangerous operation"""
        if self.auto_approve:
            print(f"{Fore.YELLOW}[AUTO-APPROVED] {operation}: {details}{Style.RESET_ALL}")
            return True, None
        
        print(f"\n{Fore.RED}⚠️  APPROVAL REQUIRED ⚠️{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Operation:{Style.RESET_ALL} {operation}")
        print(f"{Fore.YELLOW}Details:{Style.RESET_ALL} {details}")
        print(f"{Fore.YELLOW}Reason:{Style.RESET_ALL} {reason}")
        print(f"\n{Fore.CYAN}Options:{Style.RESET_ALL}")
        print("  [y] Approve this operation")
        print("  [n] Deny this operation")
        print("  [a] Approve all (disable safety for this session)")
        print("  [q] Quit agent")
        
        while True:
            choice = input(f"\n{Fore.GREEN}Your choice: {Style.RESET_ALL}").strip().lower()
            
            if choice == 'y':
                self.approval_history.append({
                    'operation': operation,
                    'details': details,
                    'approved': True
                })
                return True, None
            
            elif choice == 'n':
                self.approval_history.append({
                    'operation': operation,
                    'details': details,
                    'approved': False
                })
                return False, "User denied the operation"
            
            elif choice == 'a':
                self.auto_approve = True
                self._save_config()
                print(f"{Fore.YELLOW}Auto-approve enabled for this session{Style.RESET_ALL}")
                return True, None
            
            elif choice == 'q':
                return False, "User quit the agent"
            
            else:
                print(f"{Fore.RED}Invalid choice. Please enter y, n, a, or q{Style.RESET_ALL}")
    
    def enable_auto_approve(self):
        """Enable auto-approval"""
        self.auto_approve = True
        self._save_config()
    
    def disable_auto_approve(self):
        """Disable auto-approval"""
        self.auto_approve = False
        self._save_config()
    
    def get_approval_stats(self):
        """Get approval statistics"""
        if not self.approval_history:
            return "No operations have required approval yet"
        
        approved = sum(1 for h in self.approval_history if h['approved'])
        denied = len(self.approval_history) - approved
        
        return {
            'total_requests': len(self.approval_history),
            'approved': approved,
            'denied': denied,
            'auto_approve_enabled': self.auto_approve
        }
