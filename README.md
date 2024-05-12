

# Project Title

Brief description of the project.

## Description

More detailed description of the project, including its purpose, features, and technologies used.

## Installation

```bash
# Create virtual envirenment
$ python3 -m venv backend-api
# Activate virtual envirenment
$ source backend-api/bin/activate
# Install dependencies
$ pip install -r requirements.txt
```
## Usage

```bash
# Run application
$ uvicorn main:app --host 127.0.0.1 --port 5000 --reload
```

## Endpoints


### `/api/image/save-image`

#### Request

- **Method:** POST
- **URL:** `/api/image/save-image`
- **Request Body:**
  - `image`: (multipart/form-data) - The image file to be uploaded.
  - `cin`: (form) - The Customer Identification Number (CIN) associated with the image. Must be between 5 and 10 characters long.

#### Responses

- **Successful Response:**
  - **Status Code:** 200
  - **Content:** `{ "valid_image": true }`
  - **Description:** The image was successfully processed. A face was detected, and the encoding along with the hashed CIN was added to the CSV file.

- **Error Responses:**
  - **Status Code:** 400
    - **Content:** `{ "detail": "Invalid image format. Supported formats: jpg, jpeg, png" }`
    - **Description:** The uploaded image has an invalid format. Supported formats are jpg, jpeg, and png.
  - **Status Code:** 400
    - **Content:** `{ "detail": "CIN length must be less than 10 characters" }`
    - **Description:** The length of the CIN provided in the request is greater than or equal to 10 characters.
  - **Status Code:** 400
    - **Content:** `{ "detail": "CIN length must be at least 5 characters" }`
    - **Description:** The length of the CIN provided in the request is less than 5 characters.
  - **Status Code:** 500
    - **Content:** `{ "detail": "Internal Server Error" }`
    - **Description:** An internal server error occurred during processing.


