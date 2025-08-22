from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class AgentType(str, Enum):
  INTERVIEWER = "interviewer"
  PLANNER = "planner"
  SEARCHER = "searcher"
  READER = "reader"
  CRITIC = "critic"

class ResearchStatus(str, Enum):
  PENDING = "pending"
  INTERVIEWING = "interviewing"
  PLANNING = "planning"
  SEARCHING = "searching"
  READING = "reading"
  SYNTHESIZING = "synthesizing"
  COMPLETED = "completed"
  FAILED = "failed"

class ScopeBrief(str, Enum):
  session_id: str
  research_question: str
  background_context: str
  search_scope: Dict[str, Any]
  inclusion_criteria: List[str]
  exclusion_criteria: List[str]
  target_paper_count: int = Field(default=50, ge=10, le=200)
  created_at: datetime = Field(default_factory=datetime.now(datetime.timezone.utc))

class ResearchStrategy(BaseModel):
  session_id: str
  search_queries: List[str]
  databases_to_search: List[str]
  search_parameters: Dict[str, Any]
  quality_thresholds: Dict[str, float]
  expected_timeline: int  # minutes
  created_at: datetime = Field(default_factory=datetime.now(datetime.timezone.utc))

class Paper(BaseModel):
  paper_id: str
  title: str
  authors: List[str]
  abstract: str
  publication_date: Optional[datetime]
  journal: Optional[str]
  doi: Optional[str]
  url: Optional[str]
  pdf_url: Optional[str]
  citation_count: Optional[int]
  relevance_score: float = Field(ge=0.0, le=1.0)

class EvidenceEntry(BaseModel):
  paper_id: str
  text_snippet: str
  page_number: Optional[int]
  confidence_score: float = Field(ge=0.0, le=1.0)
  evidence_type: str
  extracted_at: datetime = Field(default_factory=datetime.now(datetime.timezone.utc))

class ResearchSession(BaseModel):
  session_id: str
  user_id: str
  status: ResearchStatus
  scope_brief: Optional[ScopeBrief] = None
  research_strategy: Optional[ResearchStrategy] = None
  papers_found: List[Paper] = Field(default_factory=list)
  evidence_table: List[EvidenceEntry] = Field(default_factory=list)
  progress_messages: List[str] = Field(default_factory=list)
  created_at: datetime = Field(default_factory=datetime.now())
  updated_at: datetime = Field(default_factory=datetime.now())
