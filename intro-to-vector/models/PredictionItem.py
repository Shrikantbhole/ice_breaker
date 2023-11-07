from pydantic import BaseModel, Field

from models.CornerCoordinates import CornerCoordinate


class Coordinate(BaseModel):
    x: float
    y: float

class PredictionItem(BaseModel):
    x: float = Field(description="Left")
    y: float = Field(description="Top")
    width: float = Field(description="Width")
    height: float = Field(description="Height")
    confidence: float
    class_: str = None  # 'class' is a reserved keyword, so we use 'class_' instead
    class_id: int
    points: list[Coordinate]
    corner_coordinate: CornerCoordinate = None

