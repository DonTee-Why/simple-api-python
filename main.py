from fastapi import FastAPI

app = FastAPI()

from src.endpoints import hello_world, calculate_age

__all__ = ["hello_world", "calculate_age"]
