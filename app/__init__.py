from fastapi import FastAPI
from contextlib import asynccontextmanager

from .db import init_db
from .ai import scraper_router, crud_router

import logging
logging.basicConfig(level = logging.INFO)

version = "v1"

description = """
A REST API to expose access to AI model ensemble for Webscraping.

This REST API is able to;
- Scrape Event details from the web
- Process the scraped data
- Generate brief description of the events utilizing multiple LLM options
- Save processed event details to database.
    """

version_prefix =f"/api/{version}"

@asynccontextmanager
async def model_lifespan(app: FastAPI): 
    logging.info('loading DB')
    await init_db()
    yield
    logging.info("Shutting down DB")


app = FastAPI(
    title="Webscraper AI",
    description=description,
    version=version,
    license_info={"name": "Apache License", "url": "https://opensource.org/license/apache-2-0"},
    contact={
        "name": "Udhtaz",
        "url": "https://github.com/udhtaz/",
        "email": "reachtaye@gmail.com",
    },
    terms_of_service="https://example.com/tos",
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc",
    lifespan=model_lifespan
)


app.include_router(scraper_router, prefix= "/scraper", tags=["Webscraper AI"])
app.include_router(crud_router, prefix= "/crud", tags=["C-R-U-D Operations"])
