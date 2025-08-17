### Booking Endpoints

Get Booking Details

- Endpoint: `/booking/<int:booking_id>`
- Method: `GET`
- Description: Retrieves the details of a booking by its ID.
- Response:
  - Status Code: `200 OK`
  - Body:
    ```json
    {
      "booking_id": "integer",
      "email": "string",
      "scooter_id": "integer",
      "start_datetime": "string (ISO 8601)",
      "end_datetime": "string (ISO 8601)",
      "actual_start_datetime": "string (ISO 8601)",
      "actual_end_datetime": "string (ISO 8601)",
      "cost": "float",
      "deposit_cost": "float",
      "google_id": "string",
      "status": "string"
    }
    ```
  - Status Code: `404 Not Found`
  - Body:
    ```json
    {
      "message": "Booking not found."
    }
    ```

Add a New Booking

- Endpoint: `/booking/add_booking`
- Method: `POST`
- Description: Adds a new booking with the provided details and returns the ID of the created booking.
- Request Body:

  ```json
  {
    "email": "string",
    "scooter_id": "integer",
    "start_datetime": "string (ISO 8601)",
    "end_datetime": "string (ISO 8601)",
    "cost": "float",
    "deposit_cost": "float"
  }
  ```

- Response:

  - Status Code: `201 Created`

    - Body:
      ```json
      {
        "message": "Booking added successfully.",
        "booking_id": "integer"
      }
      ```

  - Status Code: `400 Bad Request`
    - Body:
      ```json
      {
        "message": "Failed to add booking: <error message>"
      }
      ```

Cancel a Booking

- Endpoint: `/booking/cancel_booking/<int:booking_id>`
- Method: `DELETE`
- Description: Cancels a booking based on the booking ID.
- Response:

  - Status Code: `200 OK`
  - Body:

    ```json
    {
      "message": "Booking canceled successfully."
    }
    ```

  - Status Code: 400 Bad Request
  - Body:

    ```json
    {
      "error": "error_message"
    }
    ```

Start a Booking

- Endpoint: `/booking/start_booking`
- Method: `PUT`
- Description: Sets the actual start datetime for a booking.
- Request Body:

  ```json
  {
    "booking_id": "integer",
    "actual_start_datetime": "string (ISO 8601)"
  }
  ```

- Response:

  - Status Code: `200 OK`
  - Body:

    ```json
    {
      "message": "Booking started successfully."
    }
    ```

Get All Bookings for a Customer

- Endpoint: `/booking/get_bookings/<string:email>`
- Method: `GET`
- Description: Returns all the bookings for a customer, including past and future

- Response:

  - Status Code: `200 OK`
  - Body:

    ```json
    {
      "all_booked_scooters": [
        {
          "booking_id": "integer",
          "email": "string",
          "scooter_id": "integer",
          "start_datetime": "string (ISO 8601)",
          "end_datetime": "string (ISO 8601)",
          "actual_start_datetime": "string (ISO 8601)",
          "actual_end_datetime": "string (ISO 8601)",
          "cost": "float",
          "deposit_cost": "float",
          "google_id": "string",
          "status": "string"
        }
      ]
    }
    ```

  - Status Code: 400 Bad Request
  - Body:

    ```json
    {
      "error": "error_message"
    }
    ```

Get All Booked Scooter Times

- Endpoint: `/booking/get_booked_scooters_times`
- Method: `GET`
- Description: Returns all scooters that are currently booked and their booked time slots

- Response:

  - Status Code: `200 OK`
  - Body:

    ```json
    {
      "all_booked_scooters": [
        {
          "endDateTime": "string (ISO 8601)",
          "scooterID": "integer",
          "startDateTime": "string (ISO 8601)"
        }
      ]
    }
    ```

  - Status Code: 400 Bad Request
  - Body:

    ```json
    {
      "error": "error_message"
    }
    ```

Set Booking as Complete

- Endpoint: `/booking/complete/<int:booking_id>`
- Method: `PUT`
- Description: Marks a booking as "Complete" by its ID.
- Response:
  - Status Code: `200 OK`
  - Body:
    ```json
    {
      "message": "Booking <booking_id> marked as complete."
    }
    ```
  - Status Code: 400 Bad Request
  - Body:
    ```json
    {
      "error": "error_message"
    }
    ```

Update Booking Cost

- Endpoint: `/booking/update_cost/<int:booking_id>`
- Method: `PUT`
- Description: Updates the cost of a booking based on the booking ID.
- Request Body:
  ```json
  {
    "new_cost": "float"
  }
  ```
- Response
  - Status Code: `200 OK`
    - Body:
    ```json
    {
      "message": "Booking <booking_id> cost updated to <new_cost>."
    }
    ```
  - Status Code: `400 Bad Request`
    - Body:
    ```json
    {
      "error": "error_message"
    }
    ```

Get All Active Bookings

- Endpoint: `/booking/active`
- Method: `GET`
- Description: Gets all bookings with their status as "Active"
- Response:
  - Status Code: `200 OK`
  - Body:
    ```json
    {
      "booking_id": "integer",
      "email": "string",
      "scooter_id": "integer",
      "start_datetime": "string (ISO 8601)",
      "end_datetime": "string (ISO 8601)",
      "actual_start_datetime": "string (ISO 8601)",
      "actual_end_datetime": "string (ISO 8601)",
      "cost": "float",
      "deposit_cost": "float",
      "google_id": "string",
      "status": "string"
    }
    ```
  - Status Code: `400 Bad Request`
    - Body:
    ```json
    {
      "error": "error_message"
    }
    ```

Set Booking Google ID

- Endpoint: `/booking/<int:booking_id>set_googleID`
- Method: `PUT`
- Description: Updates the Google ID associated with a specific booking.
- Request Body:
  ```json
  {
    "google_id": "string"
  }
  ```
- Response:

  - Status Code: `200 OK`

    - Body:
      ```json
      {
        "message": "Google ID for booking <booking_id> set successfully."
      }
      ```

  - Status Code: `400 Bad Request`

    - Body:
      ```json
      {
        "error": "Google ID is required."
      }
      ```

  - Status Code: `404 Not Found`

    - Body:
      ```json
      {
        "error": "Booking not found."
      }
      ```

  - Status Code: 500 Internal Server Error
    - Body:
      ```json
      {
        "error": "error_message"
      }
      ```

Get All Bookings for a Scooter

- Endpoint: `/booking/scooter/<int:scooter_id>`
- Method: `GET`
- Description: Retrieves all bookings associated with a specific scooter ID.
- Response:

  - Status Code: `200 OK`

    - Body:
      ```json
      {
        "bookings": [
          {
            "booking_id": "integer",
            "email": "string",
            "scooter_id": "integer",
            "start_datetime": "string (ISO 8601)",
            "end_datetime": "string (ISO 8601)",
            "actual_start_datetime": "string (ISO 8601)",
            "actual_end_datetime": "string (ISO 8601)",
            "cost": "float",
            "deposit_cost": "float",
            "google_id": "string",
            "status": "string"
          }
        ]
      }
      ```

  - Status Code: `404 Not Found`

    - Body:
      ```json
      {
        "message": "No bookings found for this scooter."
      }
      ```

  - Status Code: 400 Bad Request
    - Body:
      ```json
      {
        "error": "error_message"
      }
      ```
