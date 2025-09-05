import os

from braintrust import Eval
from dotenv import load_dotenv

from src.datasets import EVALUATION_DATASET
from src.evals.base import run_agent_task
from src.scorers import content_accuracy_scorer, tool_usage_scorer

load_dotenv()

Eval(
    name=os.environ["BRAINTRUST_PROJECT_NAME"],
    data=EVALUATION_DATASET,
    task=run_agent_task,
    scores=[
        content_accuracy_scorer,
        tool_usage_scorer,
    ],  # type: ignore
)
