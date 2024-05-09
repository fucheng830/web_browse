from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from browse import get_content_from_url

app = FastAPI()

class UrlData(BaseModel):
    url: str

@app.post("/get_content")
async def get_content(data: UrlData):
    return await get_content_from_url(data.url)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9998)