from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .Base_Agent import BaseAgent

class CriticAgent(BaseAgent):
  def __init__(self):
    super().__init__(name="Critic Agent", description="An agent that evaluates and critiques the output of other agents.")

  @abstractmethod
  def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
    summaries = input_data.get("summaries", [])
    evaluation = "High quality" if summaries else "Insufficient evidence"
    critiques = []
    return {
        "agent": self.name,
        "evaluation": evaluation,
        "critiques": critiques
    }