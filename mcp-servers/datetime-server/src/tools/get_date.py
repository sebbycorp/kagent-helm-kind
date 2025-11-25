"""Get current date tool for datetime-server MCP server.

This tool returns the current date in various formats.
"""

from datetime import datetime
from core.server import mcp


@mcp.tool()
def get_date(format: str = "iso") -> str:
    """Get the current date.
    
    Args:
        format: The date format to return. Options:
            - "iso": ISO 8601 format (YYYY-MM-DD) [default]
            - "us": US format (MM/DD/YYYY)
            - "eu": European format (DD/MM/YYYY)
            - "long": Long format (e.g., "January 24, 2025")
            - "short": Short format (e.g., "Jan 24, 2025")
    
    Returns:
        The current date in the specified format
    """
    now = datetime.now()
    
    if format == "iso":
        return now.strftime("%Y-%m-%d")
    elif format == "us":
        return now.strftime("%m/%d/%Y")
    elif format == "eu":
        return now.strftime("%d/%m/%Y")
    elif format == "long":
        return now.strftime("%B %d, %Y")
    elif format == "short":
        return now.strftime("%b %d, %Y")
    else:
        return f"Unknown format: {format}. Using ISO format: {now.strftime('%Y-%m-%d')}"
