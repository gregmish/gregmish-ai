"""
Laptop Control Tools for AI Agent
Provides the agent with capabilities to interact with the system
"""

import os
import subprocess
import psutil
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class FileOperationInput(BaseModel):
    """Input for file operations"""
    operation: str = Field(description="Operation: 'read', 'write', 'create', 'delete', 'list'")
    path: str = Field(description="File or directory path")
    content: Optional[str] = Field(default=None, description="Content for write operations")


class FileOperationTool(BaseTool):
    """Tool for file system operations"""
    name = "file_operation"
    description = """
    Perform file system operations. Operations: 
    - 'read': Read file content
    - 'write': Write/update file content
    - 'create': Create new file or directory
    - 'delete': Delete file or directory
    - 'list': List directory contents
    Use this when you need to work with files or folders.
    """
    args_schema = FileOperationInput
    
    def _run(self, operation: str, path: str, content: Optional[str] = None) -> str:
        try:
            path_obj = Path(path).expanduser().resolve()
            
            if operation == "read":
                if not path_obj.exists():
                    return f"Error: File not found: {path}"
                with open(path_obj, 'r', encoding='utf-8') as f:
                    return f.read()
            
            elif operation == "write":
                if content is None:
                    return "Error: Content required for write operation"
                path_obj.parent.mkdir(parents=True, exist_ok=True)
                with open(path_obj, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"Successfully wrote to {path}"
            
            elif operation == "create":
                if path.endswith('/') or path.endswith('\\'):
                    path_obj.mkdir(parents=True, exist_ok=True)
                    return f"Created directory: {path}"
                else:
                    path_obj.parent.mkdir(parents=True, exist_ok=True)
                    path_obj.touch()
                    return f"Created file: {path}"
            
            elif operation == "delete":
                if path_obj.is_file():
                    path_obj.unlink()
                    return f"Deleted file: {path}"
                elif path_obj.is_dir():
                    import shutil
                    shutil.rmtree(path_obj)
                    return f"Deleted directory: {path}"
                else:
                    return f"Error: Path not found: {path}"
            
            elif operation == "list":
                if not path_obj.is_dir():
                    return f"Error: Not a directory: {path}"
                items = []
                for item in path_obj.iterdir():
                    items.append(f"{'[DIR]' if item.is_dir() else '[FILE]'} {item.name}")
                return "\n".join(items) if items else "Empty directory"
            
            else:
                return f"Error: Unknown operation '{operation}'"
                
        except Exception as e:
            return f"Error: {str(e)}"


class TerminalCommandInput(BaseModel):
    """Input for terminal commands"""
    command: str = Field(description="Shell command to execute")
    timeout: int = Field(default=30, description="Timeout in seconds")


class TerminalCommandTool(BaseTool):
    """Tool for executing terminal commands"""
    name = "terminal_command"
    description = """
    Execute shell commands in PowerShell. Use this to run programs, 
    install software, manage processes, or perform any terminal operation.
    Be careful with destructive commands.
    """
    args_schema = TerminalCommandInput
    
    def _run(self, command: str, timeout: int = 30) -> str:
        try:
            result = subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8',
                errors='replace'
            )
            
            output = []
            if result.stdout:
                output.append("STDOUT:\n" + result.stdout)
            if result.stderr:
                output.append("STDERR:\n" + result.stderr)
            if result.returncode != 0:
                output.append(f"EXIT CODE: {result.returncode}")
            
            return "\n".join(output) if output else "Command completed successfully (no output)"
            
        except subprocess.TimeoutExpired:
            return f"Error: Command timed out after {timeout} seconds"
        except Exception as e:
            return f"Error: {str(e)}"


class SystemInfoInput(BaseModel):
    """Input for system information"""
    info_type: str = Field(description="Type: 'cpu', 'memory', 'disk', 'processes', 'network', 'all'")


class SystemInfoTool(BaseTool):
    """Tool for getting system information"""
    name = "system_info"
    description = """
    Get system information. Types:
    - 'cpu': CPU usage and info
    - 'memory': RAM usage
    - 'disk': Disk usage
    - 'processes': Running processes
    - 'network': Network connections
    - 'all': All information
    Use this to monitor system status.
    """
    args_schema = SystemInfoInput
    
    def _run(self, info_type: str) -> str:
        try:
            info = []
            
            if info_type in ["cpu", "all"]:
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_count = psutil.cpu_count()
                info.append(f"CPU: {cpu_percent}% ({cpu_count} cores)")
            
            if info_type in ["memory", "all"]:
                mem = psutil.virtual_memory()
                info.append(f"Memory: {mem.percent}% used ({mem.used / (1024**3):.1f}GB / {mem.total / (1024**3):.1f}GB)")
            
            if info_type in ["disk", "all"]:
                disk = psutil.disk_usage('/')
                info.append(f"Disk: {disk.percent}% used ({disk.used / (1024**3):.1f}GB / {disk.total / (1024**3):.1f}GB)")
            
            if info_type in ["processes", "all"]:
                procs = []
                for proc in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), 
                                 key=lambda p: p.info['cpu_percent'] or 0, reverse=True)[:10]:
                    try:
                        procs.append(f"{proc.info['name']} (PID: {proc.info['pid']}) - CPU: {proc.info['cpu_percent']}%")
                    except:
                        pass
                info.append("Top Processes:\n" + "\n".join(procs))
            
            if info_type in ["network", "all"]:
                net = psutil.net_io_counters()
                info.append(f"Network: Sent {net.bytes_sent / (1024**2):.1f}MB, Recv {net.bytes_recv / (1024**2):.1f}MB")
            
            return "\n\n".join(info) if info else "Invalid info type"
            
        except Exception as e:
            return f"Error: {str(e)}"


class WebSearchInput(BaseModel):
    """Input for web search/scraping"""
    url: str = Field(description="URL to fetch")


class WebSearchTool(BaseTool):
    """Tool for fetching web content"""
    name = "web_search"
    description = """
    Fetch content from a URL. Use this to browse the web, 
    download files, or get information from websites.
    """
    args_schema = WebSearchInput
    
    def _run(self, url: str) -> str:
        try:
            import requests
            from bs4 import BeautifulSoup
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Try to parse as HTML
            if 'text/html' in response.headers.get('Content-Type', ''):
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)
                
                # Truncate if too long
                if len(text) > 3000:
                    text = text[:3000] + "\n... (truncated)"
                
                return text
            else:
                return f"Content-Type: {response.headers.get('Content-Type')}\n{response.text[:1000]}"
            
        except Exception as e:
            return f"Error: {str(e)}"


class PythonCodeInput(BaseModel):
    """Input for Python code execution"""
    code: str = Field(description="Python code to execute")


class PythonCodeTool(BaseTool):
    """Tool for executing Python code"""
    name = "python_code"
    description = """
    Execute Python code and return the result. Use this for calculations,
    data processing, or any task requiring Python. Print statements will be captured.
    """
    args_schema = PythonCodeInput
    
    def _run(self, code: str) -> str:
        try:
            import io
            import sys
            from contextlib import redirect_stdout, redirect_stderr
            
            # Capture output
            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()
            
            local_vars = {}
            
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                exec(code, {"__builtins__": __builtins__}, local_vars)
            
            stdout_val = stdout_buffer.getvalue()
            stderr_val = stderr_buffer.getvalue()
            
            result = []
            if stdout_val:
                result.append("Output:\n" + stdout_val)
            if stderr_val:
                result.append("Errors:\n" + stderr_val)
            if not stdout_val and not stderr_val:
                result.append("Code executed successfully (no output)")
            
            return "\n".join(result)
            
        except Exception as e:
            return f"Error: {type(e).__name__}: {str(e)}"


def get_all_tools() -> List[BaseTool]:
    """Get all available tools for the agent"""
    return [
        FileOperationTool(),
        TerminalCommandTool(),
        SystemInfoTool(),
        WebSearchTool(),
        PythonCodeTool(),
    ]
