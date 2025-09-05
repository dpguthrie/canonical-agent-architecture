"""Agent architecture package with canonical while loop implementation."""

import os

from braintrust import init_logger
from dotenv import load_dotenv

from src.main import AgentOptions, AgentWhileLoop
from src.tools import (
    GetUserDetailsTool,
    NotifyCustomerTool,
    SearchUsersTool,
    Tool,
    ToolResult,
    UpdateSubscriptionTool,
)

load_dotenv()

init_logger(project=os.getenv("BRAINTRUST_PROJECT_NAME"))

__all__ = [
    "AgentWhileLoop",
    "AgentOptions",
    "Tool",
    "ToolResult",
    "NotifyCustomerTool",
    "SearchUsersTool",
    "GetUserDetailsTool",
    "UpdateSubscriptionTool",
]

__version__ = "0.1.0"
