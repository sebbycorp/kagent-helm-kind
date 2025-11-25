"""Get current datetime tool for datetime-server MCP server.

This tool returns the current date and time together.
"""

from datetime import datetime
from core.server import mcp


@mcp.tool()
def get_datetime(format: str = "iso", timezone: str = "local") -> str:
    """Get the current date and time.
    
    Args:
        format: The datetime format to return. Options:
            - "iso": ISO 8601 format (YYYY-MM-DD HH:MM:SS) [default]
            - "timestamp": Unix timestamp (seconds since epoch)
            - "human": Human-readable format (e.g., "January 24, 2025 at 3:04 PM")
        timezone: Timezone information [currently only "local" is supported]
    
    Returns:
        The current date and time in the specified format
    """
    now = datetime.now()
    
    if format == "iso":
        return now.strftime("%Y-%m-%d %H:%M:%S")
    elif format == "timestamp":
        return str(int(now.timestamp()))
    elif format == "human":
        return now.strftime("%B %d, %Y at %I:%M %p")
    else:
        return f"Unknown format: {format}. Using ISO format: {now.strftime('%Y-%m-%d %H:%M:%S')}"
