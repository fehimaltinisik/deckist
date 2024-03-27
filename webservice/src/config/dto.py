from pydantic import BaseModel
from pydantic import BaseConfig
from humps import camelize


class DataTransferObjectConfig(BaseConfig):
    orm_mode = True
    alias_generator = camelize
    allow_population_by_field_name = True


class DataTransferObject(BaseModel):
    class Config(DataTransferObjectConfig):
        pass
