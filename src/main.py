"""Contains the main FastAPI application object."""
import os
import time

from fastapi import FastAPI, UploadFile, File
from typing import Annotated, List
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
    files: List[UploadFile] = File(...),
):
    """Test uploading two files"""
    
    if len(files) < 2:
        return {"error": "Please upload exactly two files."}

    corpus_location = f"{files[0].filename}"
    queries_location = f"{files[1].filename}"

    # Save the uploaded files
    with open(corpus_location, "wb") as f:
        f.write(files[0].file.read())

    with open(queries_location, "wb") as f:
        f.write(files[1].file.read())

    # Read the content of the saved files
    with open(corpus_location, "r", encoding="utf-8") as f:
        filecontent1 = f.read()

    with open(queries_location, "r", encoding="utf-8") as f:
        filecontent2 = f.read()

    return TestOutput(
        filename1=files[0].filename,
        filename2=files[1].filename,
        filecontent1=filecontent1,
        filecontent2=filecontent2,
    )
