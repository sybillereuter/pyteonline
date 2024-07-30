from fastapi import FastAPI, Request
import uvicorn
from .logging_config import setup_logging
from .summarizer_t5 import T5Summarizer
from .summarizer_bert import BertSummarizer
from .summarizer_translated import TranslationSummarizer

logger = setup_logging("pyte_service.log", "pyte_service-logger")

service = FastAPI()
summarizer_t5 = T5Summarizer()
summarizer_bert = BertSummarizer()
summarizer_translation = TranslationSummarizer()
size_warning = "Input text must be >5000 characters!"


@service.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


@service.get("/summarize_t5")
async def summarize_t5(text: str):
    if len(text) > 5000:
        logger.warning("Input text too long for T5 summarizer")
        return size_warning
    return summarizer_t5.summarize(text)


@service.get("/summarize_bert")
async def summarize_bert(text: str):
    if len(text) > 5000:
        logger.warning("Input text too long for BERT summarizer")
        return size_warning
    return summarizer_bert.summarize(text)


@service.get("/summarize_bart_via_translation")
async def summarize_bart_via_translation(text: str):
    if len(text) > 5000:
        logger.warning("Input text too long for translation summarizer")
        return size_warning
    return summarizer_translation.summarize(text)


if __name__ == "__main__":
    uvicorn.run("pyte_service:service", host="0.0.0.0", reload=True)
