"""
Push tools to Braintrust using simple Pydantic model creation.

This script automatically converts our local Tool classes to Braintrust tools
using Pydantic's create_model to dynamically create models from our existing schemas.

Usage:
    uv run --env-file .env src/braintrust_sync/push_tools.py

    OR

    braintrust push src/braintrust_sync/push_tools.py
"""

import os

import braintrust
from dotenv import load_dotenv
from pydantic import create_model

from src.tools import get_tools

load_dotenv()


def schema_to_pydantic(schema_dict, model_name):
    """Convert JSON schema dict directly to Pydantic model using create_model."""
    if schema_dict.get("type") != "object":
        return schema_dict

    properties = schema_dict.get("properties", {})
    required = schema_dict.get("required", [])

    # Build field definitions for create_model
    fields = {}
    for name, prop in properties.items():
        # Simple type mapping
        python_type = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": bool,
        }.get(prop.get("type"), str)

        # Required fields use ... as default, optional use None
        default = ... if name in required else None
        fields[name] = (python_type, default)

    return create_model(model_name, **fields)


# Create project and tools
project_name = os.environ.get("BRAINTRUST_PROJECT_NAME", "agent-arch")
project = braintrust.projects.create(name=project_name)

for tool_instance in get_tools():
    slug = tool_instance.name.replace("_", "-").lower()

    # Convert schema to Pydantic model
    param_model = schema_to_pydantic(tool_instance.parameters, f"{slug.title()}Params")

    # Simple handler
    async def handler(**kwargs):
        result = await tool_instance.execute(**kwargs)
        return dict(result)

    # Create tool
    project.tools.create(
        handler=handler,
        name=tool_instance.name.replace("_", " ").title(),
        slug=slug,
        description=tool_instance.description,
        parameters=param_model,
        if_exists="replace",
    )
