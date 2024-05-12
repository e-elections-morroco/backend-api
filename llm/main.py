import os
import sys
import uuid
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
import re



load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
MODEL_NAME=os.getenv("MODEL_NAME")
PROJECT_NAME=os.getenv("PROJECT_NAME")

def get_pages_contents_from_pdf(resume_pdf_path:str)->str:
    """
    Extracts the content of all pages from a PDF file.

    Args:
        resume_pdf_path (str): The path to the PDF file.

    Returns:
        str: The concatenated content of all pages in the PDF.

    Example:
        >>> get_pages_contents_from_pdf("./resume.pdf")
        'Page 1 content\nPage 2 content\n...'
    """
    loader = PyPDFLoader(resume_pdf_path)
    documents=loader.load()
    page_contents:str=""
    for document in documents:
        page_contents+=dict(document)["page_content"]+"\n"
    return page_contents

def get_answer(question: str) -> str:
  """
  This function takes a user question and uses Gemini to answer it 
  in the context of Moroccan elections.

  Args:
      question: The user's question as a string.

  Returns:
      The answer generated by Gemini as a string.
  """
  print(GEMINI_API_KEY)
  print(MODEL_NAME)
  print(PROJECT_NAME)

  # Specify the Gemini model and API key
  llm = ChatGoogleGenerativeAI(
      model=MODEL_NAME, google_api_key=GEMINI_API_KEY, project=PROJECT_NAME
  )

  # Craft the prompt template for Gemini
  prompt = f"**I am Bard, a helpful large language model designed to assist you with questions about Moroccan elections. Ask me anything!**\nHere is the user's question: {question}"

  # Call Gemini to generate the answer
  result = llm.invoke(prompt)

  # Extract the answer from the response (assuming it's the first sentence)
  answer = result.content.split(".")[0].strip()  # Might need adjustment based on output format

  return answer

