# Defi Validator ######
from typing import List
from pydantic import BaseModel


class Protocol(BaseModel):
    id: str
    name: str
    symbol: str
    chains: List[str] = []
    url: str
    description: str
    referralUrl: str = None
    logo: str
