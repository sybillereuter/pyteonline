from fastapi import FastAPI, Request, Query
import uvicorn
from .logging_config import setup_logging
from .summarizer_t5 import T5Summarizer
from .summarizer_bert import BertSummarizer

logger = setup_logging("pyte_service.log", "pyte_service-logger")

service = FastAPI(title='Pyte Service',
                  docs_url='/docs',
                  redoc_url='/redoc',
                  openapi_url='/openapi.json',
                  root_path='/pyteservice')
summarizer_t5 = T5Summarizer()
summarizer_bert = BertSummarizer()
size_warning = {"error": "Text is too long. Please provide a text between 50 and 5000 characters."}


@service.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


@service.get("/summarize_t5")
async def summarize_t5(
    text: str = Query(
        ...,
        max_length=5000,
        description="Text should be between 50 and 5000 characters"
    )
):
    if len(text) > 5000:
        logger.warning("Input text too long for T5 summarizer")
        return size_warning
    return summarizer_t5.summarize(text)


@service.get("/summarize_bert")
async def summarize_bert(text: str = Query(
        ...,
        max_length=5000,
        description="Text should be between 50 and 5000 characters"
    )
):
    if len(text) > 5000:
        logger.warning("Input text too long for BERT summarizer")
        return size_warning
    return summarizer_bert.summarize(text)


if __name__ == "__main__":
    uvicorn.run("pyte_service:service", host="0.0.0.0", reload=True)
