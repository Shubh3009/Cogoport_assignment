from pydantic import BaseModel
from typing import Dict

class ConfigurationBase(BaseModel):
    country_code: str
    configuration: Dict[str, str]

class ConfigurationCreate(ConfigurationBase):
    pass

class ConfigurationUpdate(BaseModel):
    configuration: Dict[str, str]

class Configuration(ConfigurationBase):
    id: int

    class Config:
        orm_mode = True
