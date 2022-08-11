from fastapi import FastAPI

app = FastAPI()

from src.endpoints import *

__all__ = ["hello_world", "calculate_age"]
