import cv2
from pathlib import Path
import os
import sys
from pathlib import Path

# Add parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)


def take_image(image_path: Path = Path(("temp/captured_photo.jpg"))):
    # Load pre-trained face and eye cascade classifiers
    # Load the Haar cascades for face, eyes, nose, and mouth
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
    mouth_cascade = cv2.CascadeClassifier( 'haarcascade_mcs_mouth.xml')

    # Initialize video capture
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        var= True

        # Check if exactly one face is detected
        if len(faces) == 1:
            # Get the coordinates and dimensions of the face
            x, y, w, h = faces[0]

            # Get the region of interest (ROI) for eyes detection
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            # Detect eyes in the face ROI
            eyes = eye_cascade.detectMultiScale(roi_gray)
            if len(faces) != 1:
                var= False
    
            # Extract the region of interest (ROI) for the detected face
            x, y, w, h = faces[0]
            face_roi = gray[y:y+h, x:x+w]

            # Detect eyes in the face region
            eyes = eye_cascade.detectMultiScale(face_roi)
            if len(eyes) != 2:
                var= False
            
            # Detect nose in the face region
            noses = nose_cascade.detectMultiScale(face_roi)
            if len(noses) !=1:
                var= False
            
            # Detect mouth in the face region
            mouths = mouth_cascade.detectMultiScale(face_roi)
            if len(mouths) != 1:
                var= False

            # If both eyes are detected, take a photo and close the video capture
            if var:
                cv2.imwrite(str(image_path), frame)
                cap.release()
                cv2.destroyAllWindows()
                exit()

        # Display the resulting frame without drawing the rectangle around the face
        cv2.imshow('Frame', frame)

        # Check for user input to close the video capture
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()


def detect_person_with_face_eyes_nose_mouth(image_path: Path) -> bool:
    """
    Detects a person in an image based on the presence of a face, eyes, nose, and mouth.

    Parameters:
        image_path (Path): The path to the image file to be processed.

    Returns:
        bool: True if the image contains one person with a face, eyes, nose, and mouth, False otherwise.
    """
    # Check if the image exists
    if not image_path.exists():
        print(f"\nError: Image {image_path} does not exist.")
        return False

    # Load the Haar cascades for face, eyes, nose, and mouth
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    nose_cascade = cv2.CascadeClassifier('./computer_vision/haarcascade_mcs_nose.xml')
    mouth_cascade = cv2.CascadeClassifier( './computer_vision/haarcascade_mcs_mouth.xml')
    
    # Check if cascades are loaded properly
    if face_cascade.empty() or eye_cascade.empty() or nose_cascade.empty() or mouth_cascade.empty():
        print("Error: One or more cascade files failed to load.")
        return False

    # Load the image
    img = cv2.imread(str(image_path))
    if img is None:
        print("Error: Failed to load image.")
        return False
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Check if only one face is detected
    if len(faces) != 1:
        return False
    
    # Extract the region of interest (ROI) for the detected face
    x, y, w, h = faces[0]
    face_roi = gray[y:y+h, x:x+w]

    # Detect eyes in the face region
    eyes = eye_cascade.detectMultiScale(face_roi)
    if len(eyes) < 2:
        return False
    
    # Detect nose in the face region
    noses = nose_cascade.detectMultiScale(face_roi)
    if len(noses) == 0:
        return False
    
    # Detect mouth in the face region
    mouths = mouth_cascade.detectMultiScale(face_roi)
    if len(mouths) == 0:
        return False
    
    return True




if __name__ == "__main__":
    # take_image()
    print(detect_person_with_face_eyes_nose_mouth(Path("images/taked_1.jpg")))









