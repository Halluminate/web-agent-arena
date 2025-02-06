import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

from .tasks import Task


class TaskType(Enum):
    WIKIPEDIA = "wikipedia"
    SEARCH = "search"
    QA = "qa"


@dataclass
class Task:
    """Represents a task for an agent to perform."""

    type: TaskType
    input: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


@dataclass
class AgentResponse:
    """Represents an agent's response to a task."""

    result: str
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class WebAgent(ABC):
    """Abstract base class for web-using agents."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def run_task(self, task: Task) -> AgentResponse:
        """Run a task and return the agent's response.

        Args:
            task: The task to perform

        Returns:
            AgentResponse containing the result and any metadata
        """
        pass


class MockWebAgent(WebAgent):
    """A mock implementation of a web agent for testing."""

    def __init__(self, name: str):
        super().__init__(name)
        # Simple list of mock responses for testing
        self._responses = [
            "https://en.wikipedia.org/wiki/Battle_of_Waterloo",
            "https://en.wikipedia.org/wiki/Ancient_Egyptian_architecture",
            "https://en.wikipedia.org/wiki/Theory_of_relativity",
            "The capital of France is Paris.",
            "The speed of light is approximately 299,792 kilometers per second.",
            "I found the information about renewable energy trends in Europe.",
            "According to recent studies, electric vehicle adoption is increasing worldwide.",
        ]

    async def run_task(self, task: Task) -> AgentResponse:
        """Return a random pre-defined response regardless of the task."""
        try:
            result = random.choice(self._responses)
            return AgentResponse(
                result=result,
                metadata={
                    "agent_name": self.name,
                    "task_id": task.id,
                },
            )
        except Exception as e:
            return AgentResponse(
                result="",
                error=str(e),
                metadata={
                    "agent_name": self.name,
                    "task_id": task.id if task else "unknown",
                },
            )
