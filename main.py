from fastapi import (
                    FastAPI, File, UploadFile, Form, status, HTTPException,APIRouter
                    )   
from computer_vision.take_image import detect_person_with_face_eyes_nose_mouth
from computer_vision.compare_image import compare_faces,compare_face_use_csv_encoding
from computer_vision.encoding_image import add_encoding_to_csv,extract_encodings,get_image_encoding
import shutil
from pathlib import Path
import os
import hashlib
from llm.main import get_answer
from fastapi.middleware.cors import CORSMiddleware
from voice_helper.main import process_voice_command,VoiceBotRequest
from emails.main import (
                            send_email_smtp,check_gmail_connection
                            )
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

EMAIL_PROJECT:str=os.getenv("EMAIL_PROJECT")
PASSWORD_EMAIL_PROJECT:str=os.getenv("PASSWORD_EMAIL_PROJECT")

app = FastAPI()
# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create a router for API endpoints
api_router = APIRouter(prefix="/api")


# Function to create the temporary folder if it doesn't exist
def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

@api_router.get("/")
async def index():
    """
    Index endpoint to check if the server is running.
    """
    return {"messgae":"I am working good !"}

@api_router.post("/image/save-image")
async def save_image(image: UploadFile = File(...), cin: str = Form(...)):
    # Check if CIN length is less than 10
    if len(cin) >= 10 or len(cin) <5:
        raise HTTPException(status_code=400, detail="CIN length must be less than 10 characters")
    
    # Hash the CIN using SHA-256
    hashed_cin = hashlib.sha256(cin.encode()).hexdigest()

    # Check if the temporary folder exists, create it if not
    create_folder("temp")
    create_folder("data")
    # Create the path
    csv_filename = Path("data/encodings.csv")

    # Check if the file exists, if not, create it
    if not csv_filename.exists():
        csv_filename.touch()
    # Check if the uploaded file has a valid image extension
    allowed_extensions = ('.jpg', '.jpeg', '.png')
    file_extension = Path(image.filename).suffix.lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid image format. Supported formats: jpg, jpeg, png")

    # Save the uploaded image
    with open(f"temp/{image.filename}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    # Perform image processing or any other operations here
    # For example, you can call your computer vision functions here
    valid_image:bool=detect_person_with_face_eyes_nose_mouth(Path(f"temp/{image.filename}"))
    print(valid_image)
    if valid_image:
        result:bool=add_encoding_to_csv(hashed_cin, get_image_encoding(Path(f"temp/{image.filename}")),csv_filename)
        if result:
            # Remove the temporary image file
            os.remove(f"temp/{image.filename}")
            return {"valid_image": valid_image}

    # Remove the temporary image file
    os.remove(f"temp/{image.filename}")

    return {"valid_image": valid_image}



@api_router.post("/image/is-valid")
async def check_image(image: UploadFile = File(...)):
    
    # Check if the temporary folder exists, create it if not
    create_folder("temp")

    # Check if the uploaded file has a valid image extension
    allowed_extensions = ('.jpg', '.jpeg', '.png')
    file_extension = Path(image.filename).suffix.lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid image format. Supported formats: jpg, jpeg, png")

    # Save the uploaded image
    with open(f"temp/{image.filename}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    # Perform image processing or any other operations here
    # For example, you can call your computer vision functions here
    valid_image:bool=detect_person_with_face_eyes_nose_mouth(Path(f"temp/{image.filename}"))
    # Remove the temporary image file
    os.remove(f"temp/{image.filename}")

    return {"valid_image": valid_image}



@api_router.post("/image/check-face")
async def save_image(image: UploadFile = File(...), cin: str = Form(...)):
    # Check if CIN length is less than 10
    if len(cin) >= 10 or len(cin) <5:
        raise HTTPException(status_code=400, detail="CIN length must be less than 10 characters")
    
    # Hash the CIN using SHA-256
    hashed_cin = hashlib.sha256(cin.encode()).hexdigest()

    # Check if the temporary folder exists, create it if not
    create_folder("temp")
    create_folder("data")
    # Create the path
    csv_filename = Path("data/encodings.csv")

    # Check if the file exists, if not, create it
    if not csv_filename.exists():
        csv_filename.touch()

    # Check if the uploaded file has a valid image extension
    allowed_extensions = ('.jpg', '.jpeg', '.png')
    file_extension = Path(image.filename).suffix.lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid image format. Supported formats: jpg, jpeg, png")

    # Save the uploaded image
    with open(f"temp/{image.filename}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    # Perform image processing or any other operations here
    # For example, you can call your computer vision functions here
    valid_image:bool=detect_person_with_face_eyes_nose_mouth(Path(f"temp/{image.filename}"))
    print( valid_image )
    if not valid_image:
        # Remove the temporary image file
        os.remove(f"temp/{image.filename}")
        return {"valid_image": valid_image}
    # Check if the image matches the face encoding in the CSV file
    result:bool=compare_face_use_csv_encoding(hashed_cin,Path(f"temp/{image.filename}") ,csv_filename)

    # Remove the temporary image file
    os.remove(f"temp/{image.filename}")

    return {"valid_image": result}


@api_router.get("/chat/{question}")
def answer_question(question: str):
    """
    This endpoint takes a user question and returns an answer generated by Gemini.
    """
    answer = get_answer(question)
    return {"answer": answer}

@api_router.post("/voicebot")
async def perform_action(request: VoiceBotRequest):
    response = process_voice_command(
        base64_audio_data=request.base64data,
        provider=request.provider,
        langue=request.langue,
        host=request.database_ip
    )
    return response


@api_router.post("/email/vote-success")
async def send_verification_email_code(to: str = Form(...),firstname:str=Form(...),lastname:str=Form(...)):
    """
    Send a verification code to the provided email address.
    """
    #Check the validity of email and password to connect to gmail
    if not check_gmail_connection(EMAIL_PROJECT,PASSWORD_EMAIL_PROJECT):
        raise HTTPException("Failed to connect to gmail.",4000)
    email_subject:str="لقد تم التصويت بنجاح !"
    email_body: str = f"""
    <div style="direction: rtl; text-align: right;">
        <h1>عزيزي {firstname} {lastname},</h1>
        <p>نشكركم على التصويت في الانتخابات المغربية لعام 2026. نود إعلامكم أن تصويتكم قد تم بنجاح.</p>
        <p>مع أطيب التحيات،</p>
        <p>فريق الانتخابات المغربية</p>
    </div>
    """
    is_send:bool=send_email_smtp(
        sender_email=EMAIL_PROJECT,
        sender_password=PASSWORD_EMAIL_PROJECT,
        to=to,
        email_subject=email_subject,
        email_body=email_body
    )

    return {"success":is_send}  

# Include the API router in the main app
app.include_router(api_router)