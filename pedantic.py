from pydantic import BaseModel

class FoodLookupModel(BaseModel):
    food_index: int
    food_type: str
    unit_calorie_g: float  # calories per gram

