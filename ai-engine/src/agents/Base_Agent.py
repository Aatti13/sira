from abc import ABC, abstractmethod
from typing import Any, Dict
import logging
from ..models.data_models import ResearchSession

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
  def __init__(self, agent_type: int, config: Dict[str, Any], description: str):
    self.agent_type = agent_type
    self.config = config
    self.description = description
    self.logger = logger.getChild(agent_type)
  
  @abstractmethod
  def execute(self, session: ResearchSession, **kwargs) -> Dict[str, Any]:
    pass

  def validate_input(self, session: ResearchSession) -> bool:
    pass

  async def log_progress(self, session_id: str, message: str):
    self.logger.info(f"Session {session_id}: {message}")
    # Try adding WebSocket logging here if needed