import os

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel
from services import AIResponse

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
app = FastAPI()

response_manager = AIResponse()


class UserMessage(BaseModel):
    message: str


@app.get("/api")
def hello():
    return {"message": "Hello, World"}


@app.post(
    "/usersearch",
)
async def send_question(user_response: UserMessage):
    request_id = response_manager.generate_id()

    # generate ai repsponse
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a text message assistant, you are skilled in returning simple answers to a users query, all messages are done through text messages so be mindful of character limits",
            },
            {
                "role": "user",
                "content": user_response.message,
            },
        ],
    )

    response_manager.store_response(
        request_id, completion.choices[0].message.content.strip()
    )

    return {"request_id": request_id}


@app.get(
    "/response",
)
async def get_response(request_id: str):
    response = response_manager.get_response(request_id)

    if response is None:
        raise HTTPException(status_code=404, detail="Response not found")

    return {"response": response}
