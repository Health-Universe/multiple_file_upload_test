"""Contains the main FastAPI application object."""
import os
import time

from fastapi import FastAPI, UploadFile, File
from typing import Annotated
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Multiple File Upload",
    description="Multiple file upload test",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
