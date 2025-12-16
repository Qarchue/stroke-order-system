from pydantic_settings import BaseSettings

class Config(BaseSettings):

    canva_size: set = (500, 500)

    CANVAS_WIDTH: int = 500
    
    CANVAS_HEIGHT: int = 500
    
    OUTPUT_CSV_PATH: str = "handwriting_data.csv"
    
    PLAYBACK_SPEED: float = 0.05

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Config()  # type: ignore