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



app = FastAPI()

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
        result:bool=add_encoding_to_csv(hashed_cin, get_image_encoding(Path(f"temp/{image.filename}")),Path(f"temp/{image.filename}"))
        if result:
            # Remove the temporary image file
            os.remove(f"temp/{image.filename}")
            return {"valid_image": valid_image}

    # Remove the temporary image file
    os.remove(f"temp/{image.filename}")

    return {"valid_image": valid_image}













# Include the API router in the main app
app.include_router(api_router)