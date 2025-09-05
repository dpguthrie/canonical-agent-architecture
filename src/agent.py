import json
from dataclasses import dataclass
from typing import Any, Dict, List

import braintrust
import openai

from .tools import (
    Tool,
    ToolResult,
)


@dataclass
class AgentOptions:
    """Configuration options for the agent"""

    model: str = "gpt-4"
    max_iterations: int = 10
    system_prompt: str = ""
    temperature: float = 0.1


class AgentWhileLoop:
    """
    Implementation of the canonical agent architecture: a while loop with tools.
    This pattern provides a clean, debuggable foundation for building production-ready AI agents.
    """

    def __init__(self, tools: List[Tool], options: AgentOptions):
        self.tools = {tool.name: tool for tool in tools}
        self.options = options
        self.client = openai.OpenAI()

    async def run(self, query: str, hooks: Any) -> str:
        """
        Run the agent with the canonical while loop pattern:
        1. Send query to LLM
        2. If LLM wants to use tools, execute them
        3. Send tool results back to LLM
        4. Repeat until LLM responds without tool calls or max iterations reached
        """
        with braintrust.start_span(
            name="agent_run", type=braintrust.SpanTypeAttribute.TASK
        ) as root_span:
            root_span.log(input={"input": query})

            messages = []

            # Add system prompt if provided
            if self.options.system_prompt:
                messages.append(
                    {"role": "system", "content": self.options.system_prompt}
                )

            # Add initial user query
            messages.append({"role": "user", "content": query})

            iteration = 0
            done = False
            tools_used = []

            while not done and iteration < self.options.max_iterations:
                with braintrust.start_span(
                    type=braintrust.SpanTypeAttribute.TASK,
                    name=f"agent_iteration_{iteration}",
                    metadata={"iteration": iteration, "done": done},
                ) as iteration_span:
                    iteration_span.log(input={"messages": messages})

                    # Get LLM response
                    response = await self._get_llm_response(messages)
                    message = response.choices[0].message
                    messages.append(message)

                    iteration_span.log(output=message)

                    if message.tool_calls and len(message.tool_calls) > 0:
                        # Execute tools and add results to conversation
                        for tool_call in message.tool_calls:
                            tool_result = await self._execute_tool(tool_call)
                            tools_used.append(tool_call.function.name)
                            messages.append(
                                {
                                    "role": "tool",
                                    "tool_call_id": tool_call.id,
                                    "content": json.dumps(tool_result),
                                }
                            )

                    elif message.content:
                        # LLM is done, return final response
                        done = True
                        iteration_span.log(
                            metadata={"done": done},
                        )

                    iteration += 1

            last_message = messages[-1]
            if last_message.role == "assistant" and last_message.content:
                content = None

                if isinstance(last_message.content, str):
                    content = last_message.content
                else:
                    # Assuming content is a list of parts (dict-like), like [{"text": "..."}]
                    content = "".join(
                        part.get("text", "") if "text" in part else ""
                        for part in last_message.content
                    )

                hooks.metadata["tools_used"] = tools_used
                braintrust.current_span().log(
                    output=content,
                    metrics={
                        "total_iterations": iteration,
                    },
                )
                return content
            else:
                fallback_message = f"Agent reached maximum iterations ({self.options.max_iterations}) without completing the task."
                braintrust.current_span().log(
                    output=fallback_message,
                    metrics={
                        "total_iterations": iteration,
                        "max_iterations_reached": 1,
                    },
                )
                return fallback_message

    async def _get_llm_response(self, messages: List[Dict[str, Any]]):
        """Get response from LLM with function calling enabled"""
        functions = [tool.to_function_schema() for tool in self.tools.values()]

        with braintrust.start_span(
            type=braintrust.SpanTypeAttribute.LLM, name="llm_call"
        ) as span:
            response = self.client.chat.completions.create(
                model=self.options.model,
                messages=messages,  # type: ignore
                tools=[{"type": "function", "function": func} for func in functions],  # type: ignore
                temperature=self.options.temperature,
            )

            span.log(
                input={"messages": messages, "functions": functions},
                output={"response": response.model_dump()},
            )

            return response

    async def _execute_tool(self, tool_call) -> ToolResult:
        """Execute a tool call and return the result"""
        tool_name = tool_call.function.name

        if tool_name not in self.tools:
            return {
                "success": False,
                "message": f"Unknown tool: {tool_name}",
                "data": None,
            }

        with braintrust.start_span(
            type=braintrust.SpanTypeAttribute.TOOL,
            name=f"tool_execution_{tool_name}",
        ) as span:
            try:
                arguments = json.loads(tool_call.function.arguments)

                result = await self.tools[tool_name].execute(**arguments)

                span.log(
                    input=arguments,
                    output=result,
                )

                return result

            except Exception as e:
                span.log(error=str(e))
                error_result: ToolResult = {
                    "success": False,
                    "message": f"Error executing {tool_name}: {str(e)}",
                    "data": None,
                }
                return error_result
