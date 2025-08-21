from abc import ABC, abstractmethod
from typing import Any, Dict
from .Base_Agent import BaseAgent

class ReaderAgent(BaseAgent): 
  def __init__(self):
    super().__init__(name="Reader Agent", description="An agent that reads and processes input data to extract relevant information.")
  
  def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
    text = input_data.get("text", "")
    if not text:
      return {"agent": self.name, "error": "No text provided"}
    
    # Simulate reading and processing the text
    processed_text = text.lower()  # Example processing step
    return {
      "agent": self.name,
      "processed_text": processed_text,
      "summary": f"Processed {len(text)} characters"
    }
