# command to run: uv run --env-file .env src/evals/eval_agent.py

from typing import Any

from src.agent import AgentOptions, AgentWhileLoop
from src.prompt import SYSTEM_PROMPT
from src.tools import get_tools


def create_customer_service_agent() -> AgentWhileLoop:
    """Create a customer service agent for evaluation"""
    tools = get_tools()

    options = AgentOptions(
        model="gpt-4o",
        max_iterations=10,
        system_prompt=SYSTEM_PROMPT,
        temperature=0.1,
    )

    return AgentWhileLoop(tools=tools, options=options)


async def run_agent_task(input_data: str, hooks: Any) -> str:
    """Run a single agent task"""
    agent = create_customer_service_agent()
    return await agent.run(input_data, hooks)
