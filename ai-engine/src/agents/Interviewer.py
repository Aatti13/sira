from abc import ABC, abstractmethod
from typing import Any, Dict
from .Base_Agent import BaseAgent

class InterviewerAgent(BaseAgent):
  def __init__(self):
    super().__init__(name="Interviewer Agent", description="An agent that conducts interviews and gathers information from other agents.")
  
  @abstractmethod
  def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
    scope = input_data.get("scope", "general")
    return {
      "agent": self.name,
      "refined_scope": f"Refined: {scope}",
      "questions": ["What’s your research goal?", "Any constraints?"]
    }