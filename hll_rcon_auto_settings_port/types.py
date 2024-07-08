import pydantic


class MapCondition(pydantic.BaseModel):
    not_: bool
    maps: list[str]


class NumberCondition(pydantic.BaseModel):
    min: int = pydantic.Field(ge=0, le=100)
    max: int = pydantic.Field(ge=0, le=100)
    not_: bool


class TimeCondition(pydantic.BaseModel):
    max: str
    min: str
    not_: bool
    timezone: str
