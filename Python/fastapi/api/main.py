from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import Field

app = FastAPI(
    title="Learn FastAPI",
    version="1.0"
)

class SInput(BaseModel):
    x:int
    y:int

class MInput(BaseModel):
    a:int = Field(ge=0,le=5000)
    b:int
    c:int

@app.post("/sum")
def sum(data: SInput):
    return {"result": data.x + data.y}

@app.post("/mul")
def multiply(data: MInput, limit: int=3):
    M = data.a * data.b * data.c
    return {"result": M}
    
