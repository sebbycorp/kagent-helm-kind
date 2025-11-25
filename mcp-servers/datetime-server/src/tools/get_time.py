"""Get current time tool for datetime-server MCP server.

This tool returns the current time in various formats.
"""

from datetime import datetime
from core.server import mcp


@mcp.tool()
def get_time(format: str = "24h", include_seconds: bool = True) -> str:
    """Get the current time.
    
    Args:
        format: The time format to return. Options:
            - "24h": 24-hour format [default]
            - "12h": 12-hour format with AM/PM
        include_seconds: Whether to include seconds in the output [default: True]
    
    Returns:
        The current time in the specified format
    """
    now = datetime.now()
    
    if format == "24h":
        if include_seconds:
            return now.strftime("%H:%M:%S")
        else:
            return now.strftime("%H:%M")
    elif format == "12h":
        if include_seconds:
            return now.strftime("%I:%M:%S %p")
        else:
            return now.strftime("%I:%M %p")
    else:
        return f"Unknown format: {format}. Using 24h format: {now.strftime('%H:%M:%S')}"
