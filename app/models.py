from pydantic import BaseModel
from typing import Optional

class PromptRequest(BaseModel):
    prompt: str
    character_name: Optional[str] = None
    setting: Optional[str] = None
    tone: Optional[str] = None
    art_style: Optional[str] = None