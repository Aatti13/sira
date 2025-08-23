from abc import ABC, abstractmethod
from typing import Any, Dict


from .Base_Agent import BaseAgent
from ..models.data_models import ResearchSession, ScopeBrief


class InterviewerAgent(BaseAgent):
  def __init__(self, config: Dict[str, Any]):
    super().__init__("interviewer", config)
    # Add LLM service
  
  @abstractmethod
  def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
    scope = input_data.get("scope", "general")
    return {
      "agent": self.name,
      "refined_scope": f"Refined: {scope}",
      "questions": ["What’s your research goal?", "Any constraints?"]
    }