

# e-elections
![Face Recognition System](./docs/api-image.png)
The e-elections project aims to provide a comprehensive backend API solution for various election-related functionalities. Leveraging modern technologies such as FastAPI, Langchain, and computer vision, the system facilitates tasks like face detection, chatbot interaction, and data management.

## Description

This project serves as the backbone for e-elections applications, offering a robust and scalable API architecture. It enables seamless integration of features like face detection for identity verification, chatbot assistance for user inquiries, and efficient data handling for election management.
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


### `/api/image/is-valid`

This endpoint checks whether an uploaded image is valid by performing basic checks like file extension and face detection.

#### Request

- **Method:** GET
- **URL:** `/api/image/is-valid`
- **Query Parameters:** None
- **Request Body:**
  - `image`: (multipart/form-data) - The image file to be validated.

#### Responses

- **Successful Response:**
  - **Status Code:** 200
  - **Content:** 
    ```json
    {
      "valid_image": true
    }
    ```
  - **Description:** The image is valid. A face was detected in the image.

- **Error Responses:**
  - **Status Code:** 400
    - **Content:** 
      ```json
      {
        "detail": "Invalid image format. Supported formats: jpg, jpeg, png"
      }
      ```
    - **Description:** The uploaded image has an invalid format. Supported formats are jpg, jpeg, and png.
  - **Status Code:** 500
    - **Content:** 
      ```json
      {
        "detail": "Internal Server Error"
      }
      ```
    - **Description:** An internal server error occurred during processing.


### `/api/image/check-face`

#### Request

- **Method:** GET
- **URL:** `/api/image/check-face`
- **Query Parameters:** None
- **Request Body:**
  - `image`: (multipart/form-data) - The image file to be checked.
  - `cin`: (form) - The Customer Identification Number (CIN) associated with the image. Must be between 5 and 10 characters long.

#### Responses

- **Successful Response:**
  - **Status Code:** 200
  - **Content:** 
    ```json
    {
      "valid_image": true
    }
    ```
  - **Description:** The face in the uploaded image matches a face encoding stored in the system.

- **Error Responses:**
  - **Status Code:** 400
    - **Content:** 
      ```json
      {
        "detail": "CIN length must be less than 10 characters"
      }
      ```
    - **Description:** The length of the CIN provided in the request is greater than or equal to 10 characters.
  - **Status Code:** 400
    - **Content:** 
      ```json
      {
        "detail": "Invalid image format. Supported formats: jpg, jpeg, png"
      }
      ```
    - **Description:** The uploaded image has an invalid format. Supported formats are jpg, jpeg, and png.
  - **Status Code:** 500
    - **Content:** 
      ```json
      {
        "detail": "Internal Server Error"
      }
      ```
    - **Description:** An internal server error occurred during processing.

### `/api/chat/{question}`

#### Request

- **Method:** GET
- **URL:** `/api/chat/{question}`
- **Description:** This endpoint takes a user question and returns an answer generated by Gemini.

#### Responses

- **Successful Response:**
  - **Status Code:** 200
  - **Content:** `{ "answer": "The generated answer from Gemini." }`
  - **Description:** The question was successfully processed, and an answer was generated by Gemini.

- **Error Responses:**
  - **Status Code:** 500
    - **Content:** `{ "detail": "Internal Server Error" }`
    - **Description:** An internal server error occurred during processing.

### `api/email/vote-success`

#### Request

- **Method:** POST
- **URL:** `/email/vote-success`
- **Request Body:**
  - `to`: (form) - The email address to send the verification email to.
  - `firstname`: (form) - The first name of the person.
  - `lastname`: (form) - The last name of the person.

#### Responses

- **Successful Response:**
  - **Status Code:** 200
  - **Content:** `{ "success": true }`
  - **Description:** The email was successfully sent to the provided email address.

- **Error Responses:**
  - **Status Code:** 400
    - **Content:** `{ "detail": "Failed to connect to gmail." }`
    - **Description:** There was an error connecting to Gmail with the provided credentials.

### `api/voicebot`

#### Request

- **Method:** POST
- **URL:** `/voicebot`
- **Request Body:**
  - `base64data`: (string) - The base64 encoded audio data of the voice command.
  - `provider`: (string) - The service provider for processing the voice command.
  - `langue`: (string) - The language of the voice command.
  - `database_ip`: (string) - The IP address of the database host.

#### Responses

- **Successful Response:**
  - **Status Code:** 200
  - **Content:** The response from processing the voice command.
  - **Description:** The voice command was successfully processed and the appropriate action was taken.

- **Error Responses:**
  - **Status Code:** 400
    - **Content:** `{ "detail": "Invalid request data" }`
    - **Description:** The request data is invalid or incomplete.
  - **Status Code:** 500
    - **Content:** `{ "detail": "Internal Server Error" }`
    - **Description:** An internal server error occurred during processing.

## Contributing

Contributions to this project are welcome! If you have any ideas, suggestions, or bug fixes, feel free to open an issue or submit a pull request.

## License

This project is licensed under the GPL License. See the [LICENSE](LICENSE) file for details.






