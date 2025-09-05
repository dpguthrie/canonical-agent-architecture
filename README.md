# Agent Architecture

A canonical agent architecture implementation with tools, built for production-ready AI agents. This project demonstrates a clean, debuggable foundation using a while loop pattern with tool integration and comprehensive evaluation capabilities.

**Inspired by:** [The canonical agent architecture: A while loop with tools](https://www.braintrust.dev/blog/agent-while-loop) - Braintrust's blog post on building reliable agents with simple, composable patterns.

## Features

- **Canonical Agent Architecture**: Clean while loop implementation with tool calling
- **Customer Service Tools**: Pre-built tools for user management, notifications, and subscriptions
- **Comprehensive Evaluation**: Built-in evaluation framework with custom scorers
- **Braintrust Integration**: Advanced logging, tracing, and evaluation capabilities
- **Type-Safe**: Full type annotations and validation
- **Production Ready**: Error handling, logging, and monitoring

## Quick Start

### Prerequisites

- Python 3.12 or higher
- OpenAI API key
- Braintrust account

### Installation

#### Option 1: Using uv (Recommended)

**macOS/Linux:**
```bash
# Clone the repository
git clone https://github.com/dpguthrie/canonical-agent.git
cd canonical-agent

# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

**Windows (PowerShell):**
```powershell
# Clone the repository
git clone https://github.com/dpguthrie/canonical-agent.git
cd canonical-agent

# Install uv if you haven't already
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install dependencies
uv sync
```

#### Option 2: Using pip

**macOS/Linux:**
```bash
# Clone the repository
git clone https://github.com/dpguthrie/canonical-agent.git
cd canonical-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .
```

**Windows (Command Prompt):**
```cmd
# Clone the repository
git clone https://github.com/dpguthrie/canonical-agent.git
cd canonical-agent

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -e .
```

**Windows (PowerShell):**
```powershell
# Clone the repository
git clone https://github.com/dpguthrie/canonical-agent.git
cd canonical-agent

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -e .
```

### Environment Setup

1. **Create your environment file:**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   ```

2. **Edit the `.env` file with your API keys:**
   ```env
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Braintrust Configuration (optional, for evaluations)
   BRAINTRUST_API_KEY=your_braintrust_api_key_here
   BRAINTRUST_PROJECT_NAME=agent-arch-eval
   ```

### Running the Agent

#### Basic Usage

**Using uv:**
```bash
uv run src/main.py
```

**Using pip:**
```bash
python src/main.py
```

#### Running Evaluations

**Using uv:**
```bash
uv run --env-file .env src/evals/eval_agent.py
```

**Using pip:**
```bash
python src/evals/eval_agent.py
```

## Project Structure

```
agent-arch/
├── README.md                 # This file
├── pyproject.toml           # Project configuration and dependencies
├── uv.lock                  # Lock file for uv package manager
├── .env.example             # Template for environment variables
└── src/
    ├── __init__.py          # Package initialization
    ├── agent.py             # Core agent implementation (AgentWhileLoop)
    ├── datasets.py          # Evaluation datasets
    ├── main.py              # Example usage and entry point
    ├── prompt.py            # System prompts for the agent
    ├── push.py              # Utilities for pushing data to Braintrust
    ├── scorers.py           # Custom evaluation scorers
    ├── tools.py             # Tool implementations with Braintrust integration
    └── evals/
        ├── __init__.py      # Evaluation package initialization
        ├── base.py          # Base evaluation utilities
        └── eval_agent.py    # Main evaluation script
```

### Key Components

#### Core Agent (`src/agent.py`)
- **`AgentWhileLoop`**: The main agent class implementing the canonical while loop pattern
- **`AgentOptions`**: Configuration dataclass for agent behavior
- Integrates with OpenAI's function calling and Braintrust logging

#### Tools (`src/tools.py`)
- **`Tool`**: Abstract base class for all agent tools
- **Customer Service Tools**:
  - `SearchUsersTool`: Find users by various criteria
  - `GetUserDetailsTool`: Retrieve detailed user information
  - `NotifyCustomerTool`: Send notifications to customers
  - `UpdateSubscriptionTool`: Manage user subscriptions
- **Braintrust Integration**: Built-in registration and Pydantic model generation
- **Lambda-Compatible**: Self-contained definitions that work in AWS Lambda environments

#### Evaluation Framework (`src/evals/`)
- **`eval_agent.py`**: Main evaluation script using Braintrust
- **`base.py`**: Helper functions for running evaluations
- **Custom Scorers**: Content accuracy and tool usage evaluation

#### Datasets (`src/datasets.py`)
- Pre-defined evaluation scenarios covering:
  - Multi-step workflows
  - Single lookups
  - Subscription management
  - Customer notifications

## Usage Examples

### Basic Agent Interaction

```python
import asyncio
from src.agent import AgentWhileLoop, AgentOptions
from src.tools import get_tools
from src.prompt import SYSTEM_PROMPT

async def main():
    # Initialize tools
    tools = get_tools()
    
    # Configure agent
    options = AgentOptions(
        model="gpt-4",
        max_iterations=10,
        system_prompt=SYSTEM_PROMPT,
        temperature=0.1,
    )
    
    # Create and run agent
    agent = AgentWhileLoop(tools=tools, options=options)
    response = await agent.run("Check if john@example.com is an active subscriber")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

### Custom Tool Implementation

```python
from src.tools import Tool, ToolResult

class CustomTool(Tool):
    @property
    def name(self) -> str:
        return "custom_tool"
    
    @property
    def description(self) -> str:
        return "A custom tool for specific functionality"
    
    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "input": {"type": "string", "description": "Input parameter"}
            },
            "required": ["input"]
        }
    
    def execute(self, input: str) -> ToolResult:
        # Your custom logic here
        return {
            "success": True,
            "message": f"Processed: {input}",
            "data": {"result": input.upper()}
        }
```

## Development

### Running Tests

```bash
# Using uv
uv run pytest

# Using pip
python -m pytest
```

### Code Formatting

```bash
# Using uv
uv run ruff format
uv run ruff check

# Using pip
python -m ruff format
python -m ruff check
```

### Development Dependencies

Install development dependencies for testing and linting:

```bash
# Using uv
uv sync --dev

# Using pip
pip install -e ".[dev]"
```

## Evaluation and Monitoring

The project includes a comprehensive evaluation framework using Braintrust:

1. **Custom Scorers**: Evaluate content accuracy and tool usage
2. **Automated Testing**: Run evaluations on predefined datasets
3. **Performance Tracking**: Monitor agent performance over time
4. **Detailed Logging**: Full conversation and tool execution logs

### Running Evaluations

Evaluations test the agent against various customer service scenarios:

```bash
# Make sure your .env file is configured
uv run --env-file .env src/evals/eval_agent.py
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `BRAINTRUST_API_KEY`: Your Braintrust API key (optional, for evaluations)
- `BRAINTRUST_PROJECT_NAME`: Project name for Braintrust logging (optional)

### Agent Configuration

Customize agent behavior through `AgentOptions`:

```python
options = AgentOptions(
    model="gpt-4o",           # OpenAI model to use
    max_iterations=10,        # Maximum tool calling iterations
    system_prompt=SYSTEM_PROMPT,  # System instructions
    temperature=0.1,          # Response randomness (0.0-1.0)
)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite and linting
6. Submit a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For questions and support:
- Open an issue on GitHub
- Check the documentation in the code
- Review the evaluation examples for usage patterns

## Architecture Notes

This implementation follows the "canonical agent architecture" pattern as described in [Braintrust's blog post](https://www.braintrust.dev/blog/agent-while-loop), which provides:

- **Simplicity**: Easy to understand and debug
- **Flexibility**: Easy to add new tools and capabilities
- **Observability**: Full logging and tracing of agent behavior
- **Reliability**: Proper error handling and iteration limits
- **Testability**: Comprehensive evaluation framework

The while loop pattern ensures predictable behavior while allowing for complex multi-step reasoning and tool usage. As the blog post notes, this pattern wins for the same reason as UNIX pipes and React components: it's simple, composable, and flexible enough to handle complexity without becoming complex itself.
