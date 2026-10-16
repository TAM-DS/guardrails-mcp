from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class Claim(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(max_length=1000)
    source_id: str = Field(max_length=80)

class Draft(BaseModel):
    model_config = ConfigDict(extra="forbid")
    decision: Literal["draft", "hold", "blocked"]
    subject: str = Field(max_length=300)
    body: str = Field(max_length=5000)
    claims: list[Claim] = Field(max_length=20)
