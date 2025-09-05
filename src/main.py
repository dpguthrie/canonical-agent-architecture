import asyncio

from dotenv import load_dotenv

from src.agent import AgentOptions, AgentWhileLoop
from src.prompt import SYSTEM_PROMPT
from src.tools import (
    GetUserDetailsTool,
    NotifyCustomerTool,
    SearchUsersTool,
    UpdateSubscriptionTool,
)

load_dotenv()


# Example usage
async def main():
    """Example of how to use the AgentWhileLoop"""

    # Initialize tools
    tools = [
        NotifyCustomerTool(),
        SearchUsersTool(),
        GetUserDetailsTool(),
        UpdateSubscriptionTool(),
    ]

    # Configure agent
    options = AgentOptions(
        model="gpt-4",
        max_iterations=10,
        system_prompt=SYSTEM_PROMPT,
        temperature=0.1,
    )

    # Create agent
    agent = AgentWhileLoop(tools=tools, options=options)

    # Example customer service query
    query = """A customer with email john@example.com is complaining that they can't access pro features even though they're paying for a pro subscription. Please investigate and help resolve this issue."""

    # Run the agent
    response = await agent.run(query)
    print(f"Agent response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
