"""Contains the main FastAPI application object."""
import os
import time

from fastapi import FastAPI, UploadFile, File
from typing import Annotated
from pydantic import BaseModel, Field

from src.api_diagnostics.router import router as diagnostic_router
from src.api_diagnostics.schemas import ExceptionMessage
from src.chads_vasc_score.router import router as cvs_router
from src.config import settings

# It's good practice to set default server timezone to UTC for standardization.
os.environ["TZ"] = "UTC"
time.tzset()

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    debug=settings.DEBUG,
    version=settings.VERSION,
    openapi_url=settings.OPEN_API_URL,
    swagger_ui_parameters={"persistAuthorization": True},
    responses={
        400: {"model": ExceptionMessage},
        401: {"model": ExceptionMessage},
        403: {"model": ExceptionMessage},
        404: {"model": ExceptionMessage},
        422: {"model": ExceptionMessage},
    },
)

app.include_router(diagnostic_router, tags=["Diagnostics"])
app.include_router(cvs_router, prefix=settings.API_URL, tags=["CHA₂DS₂-VASc"])


class TestOutput(BaseModel):
    """Form-based output schema for file upload test."""
    filename1: str = Field(
        title="File 1",
        examples=["this_is_a_filename.txt"],
        description="The name of a file",
        format="display",
    )

    filename2: str = Field(
        title="File 2",
        examples=["this_is_a_filename.txt"],
        description="The name of a file",
        format="display",
    )

    filecontent1: str = Field(
        title="File content 1",
        examples=["this is some content"],
        description="The content of a file",
        format="display",
    )

    filecontent2: str = Field(
        title="File content 2",
        examples=["this is some content"],
        description="The content of a file",
        format="display",
    )


@app.post(
    "/test_upload/",
    response_model=TestOutput,
    summary="Files",
    description="Testing file uploads.",
)
def test_upload(
    corpus: Annotated[UploadFile, File()],
    queries: Annotated[UploadFile, File()],
):
    """Test uploading two files"""
    os.makedirs("data", exist_ok=True)  # Ensure the data directory exists

    corpus_location = f"data/{corpus.filename}"
    queries_location = f"data/{queries.filename}"

    # Save the uploaded files
    with open(corpus_location, "wb") as f:
        f.write(corpus.file.read())

    with open(queries_location, "wb") as f:
        f.write(queries.file.read())

    # Read the content of the saved files
    with open(corpus_location, "r", encoding="utf-8") as f:
        filecontent1 = f.read()

    with open(queries_location, "r", encoding="utf-8") as f:
        filecontent2 = f.read()

    return TestOutput(
        filename1=corpus.filename,
        filename2=queries.filename,
        filecontent1=filecontent1,
        filecontent2=filecontent2,
    )
