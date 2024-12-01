from pydantic import BaseModel


class getManager(BaseModel):
    """Модель для сериализации руководителя"""

    id: int
    email: str
    full_name: str
    quotas: int
    
    model_config = {"from_attributes": True}
