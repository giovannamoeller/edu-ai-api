from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CompetencyDetails(BaseModel):
    score: int
    justification: str

class CompetencyFeedback(BaseModel):
    competency1: CompetencyDetails
    competency2: CompetencyDetails
    competency3: CompetencyDetails
    competency4: CompetencyDetails
    competency5: CompetencyDetails

class EssayScores(BaseModel):
    competency1: int
    competency2: int
    competency3: int
    competency4: int
    competency5: int

class EssayRequest(BaseModel):
    text: str
    subject: str

class EssayResponse(BaseModel):
    scores: EssayScores
    feedback: CompetencyFeedback
    created_at: datetime