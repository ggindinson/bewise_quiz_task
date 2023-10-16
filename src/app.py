import asyncio
from typing import Annotated, Any, AsyncIterator, Dict, List

import uvicorn
from aiohttp import ClientSession
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_utils import create_engine, create_session, create_tables
from database.models import Questions
from typings.server_types import FormattedQuestion, LoadQuestionsBody

app = FastAPI()


async def get_db_session() -> AsyncIterator[AsyncSession]:
    session = create_session(engine=create_engine())
    async with session() as session:
        yield session


async def request_api(
    questions_amount: int,
) -> List[FormattedQuestion]:
    async with ClientSession() as aiohttp_session:
        response = await aiohttp_session.get(
            url=f"https://jservice.io/api/random?count={questions_amount}"
        )
        json_data: List[Dict[str, Any]] = await response.json()
        logger.debug("response got")
    logger.debug(f"{json_data=}")
    formatted_questions = [
        FormattedQuestion(**json_question_data) for json_question_data in json_data
    ]
    logger.debug("formatted")

    return formatted_questions


@app.post(path="/load_questions")
async def load_questions_handler(
    body: LoadQuestionsBody,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> JSONResponse:
    requested_questions_amount = body.questions_num
    unique_questions: List[Questions] = []

    while len(unique_questions) != requested_questions_amount:
        questions = await request_api(
            questions_amount=requested_questions_amount - len(unique_questions)
        )
        unique_questions.append(
            *(
                await Questions.create_unique_and_return(
                    session=db_session,
                    data=[question.model_dump() for question in questions],
                )
            )
        )
    logger.debug(f"{unique_questions=}")

    return JSONResponse(
        {
            "status": "success",
            "data": [
                {
                    c.name: str(getattr(question, c.name))
                    for c in question.__table__.columns
                }
                for question in unique_questions
            ],
        }
    )


if __name__ == "__main__":
    # Creating db tables if they do not exist.
    asyncio.run(create_tables(engine=create_engine()))

    # Server launch
    uvicorn.run(app, host="0.0.0.0", port=8080)
