
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agents import Agent, Runner


# -----------------------------------------
# 1. Load environment configuration
# -----------------------------------------

load_dotenv(Path(__file__).with_name(".env"))


# -----------------------------------------
# 2. Load reunion knowledge
# -----------------------------------------

knowledge_file = (
    Path(__file__).parent
    / "knowledge"
    / "reunion_faq.md"
)

if not knowledge_file.exists():
    raise FileNotFoundError(
        f"Knowledge file not found: {knowledge_file}"
    )

reunion_knowledge = knowledge_file.read_text(
    encoding="utf-8"
)


# -----------------------------------------
# 3. Create the AI agent
# -----------------------------------------

reunion_agent = Agent(
    name="Reunion Event Assistant",

    instructions=f"""
    You are a friendly assistant for the
    NIT Jamshedpur 1998 batch reunion.

    Answer alumni questions using the
    reunion information provided below.

    Important rules:
    1. Use the provided information as your source.
    2. Never invent event details.
    3. If information is unavailable, say so.
    4. Be friendly and concise.
    5. Do not invent registration links.

    REUNION KNOWLEDGE:

    {reunion_knowledge}
    """
)


# -----------------------------------------
# 4. Create the FastAPI application
# -----------------------------------------

app = FastAPI(
    title="NIT Jamshedpur Reunion Assistant",
    description="AI assistant for the 1998 batch reunion",
    version="1.0.0"
)


# -----------------------------------------
# 5. Configure website access (CORS)
# -----------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# -----------------------------------------
# 6. Define the incoming question format
# -----------------------------------------

class ChatRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000
    )


# -----------------------------------------
# 7. Health check endpoint
# -----------------------------------------

@app.get("/health")
async def health_check():

    return {
        "status": "healthy",
        "message": "Reunion AI backend is running"
    }


# -----------------------------------------
# 8. Chat endpoint
# -----------------------------------------

@app.post("/chat")
async def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    try:

        result = await Runner.run(
            reunion_agent,
            question
        )

        return {
            "answer": result.final_output
        }

    except Exception as error:

        print("AI backend error:", type(error).__name__)

        raise HTTPException(
            status_code=500,
            detail="Sorry, I could not process your question. Please try again."
        )
