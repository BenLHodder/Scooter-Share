### Scooter Endpoints

Get Scooter Details

- Endpoint: `/scooter/<int:scooter_id>`
- Method: `GET`
- Description: Retrieves the details of a scooter by its ID.
- Response:
  - Status Code: `200 OK`
  - Body:
    ```json
    {
      "scooterID": "integer",
      "make": "string",
      "colour": "string",
      "longitude": "float",
      "latitude": "float",
      "costMin": "float",
      "batteryPercentage": "float",
      "status": "string",
      "ipAddress": "string"
    }
    ```
  - Status Code: `404 Not Found`
  - Body:
    ```json
    {
      "message": "Scooter not found."
    }
    ```

Update Scooter Status

- Endpoint: `/scooter/update_scooter_status`
- Method: `PUT`
- Description: Updates the status of a scooter.
- Request Body:

  ```json
  {
    "scooter_id": "integer",
    "status": "string"
  }
  ```

- Response:

  - Status Code: `200 OK`
  - Body:

    ```json
    {
      "message": "Scooter status updated successfully."
    }
    ```

Get All Scooters

- Endpoint: `/scooter/scooters`
- Method: `GET`
- Description: Retrieves the details of all scooters in the system.
- Response:
  - Status Code: `200 OK`
  - Body:
    ```json
    [
      {
        "scooterID": "integer",
        "make": "string",
        "colour": "string",
        "longitude": "float",
        "latitude": "float",
        "costMin": "float",
        "batteryPercentage": "float",
        "status": "string",
        "ipAddress": "string"
      },
      ...
    ]
    ```

Update Scooter IP Address

- Endpoint: `/scooter/update_ip_address/<int:scooter_id>`
- Method: `PUT`
- Description: Updates the IP address for a scooter.
- Request Body:
  ```json
  {
    "ip_address": "string"
  }
  ```
- Response:
  - Status Code: `200 OK`
    - Body:
      ```json
      {
        "message": "Scooter IP address updated successfully."
      }
      ```

Update Scooter Location

- Endpoint: `/scooter/update_location/<int:scooter_id>`
- Method: `PUT`
- Description: Updates the latitude and longitude for a scooter.
- Request Body:
  ```json
  {
    "latitude": "float",
    "longitude": "float"
  }
  ```
- Response:
  - Status Code: 200 OK
    - Body:
      ```json
      {
        "message": "Scooter location updated successfully."
      }
      ```

Update Scooter Details

- Endpoint: `/scooter/update_details/<scooter_id>`
- Method: `PUT`
- Description: Updates all details of a scooter based on the provided scooter ID.
- Request Body:

  ```json
  {
    "make": "string",
    "colour": "string",
    "latitude": "float",
    "longitude": "float",
    "cost_min": "float",
    "battery_percentage": "int",
    "status": "string",
    "ip_address": "string"
  }
  ```

- Response:

  - Status Code: `200 OK`
    - Body:
      ```json
      {
        "message": "Scooter details updated successfully."
      }
      ```
