from pydantic import BaseModel
from typing import List

class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
  username: str



class UserCreate(UserBase):
    password: str

class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    is_active: bool
    usertype: str
    class Config:
        orm_mode = True
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None





class UserInDB(User):
    hashed_password: str

class Domains(BaseModel):
    domains: List[str]

    class Config:
        schema_extra = {
            "example": {
            "domains":["https://www.rop.gov.om","https://www.evisa.rop.gov.om","https://webmail.rop.gov.om","https://mail.rop.gov.om"]
            }
        }
def json(value):
    return True
class NucleiConfig(BaseModel):
    scan_name: str
    time_delay: int
    templates : List[str]
    severty : List[str]
    domains : List[str]

    class Config:
                schema_extra = {
                    "example": {
                            "main_domain":"rop.gov.om",
                            "scan_name":"RopScan",
                            "time_delay": 5,
                            "templates": ["templates1", "templates2"],
                            "severty": ["Critical", "Medium", "Low", "Info"],
                            "domains": ["https://www.rop.gov.om", "https://www.evisa.rop.gov.om","https://webmail.rop.gov.om", "https://mail.rop.gov.om"],
                            "description":"Description of the scan"

                    }
                }

