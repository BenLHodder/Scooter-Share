### Fault Log Endpoints

Update Scooter Fault Notes

- Endpoint: `/fault/update_scooter_fault`
- Method: `PUT`
- Description: Updates the fault notes for a specific scooter. If the scooter already has an open fault entry, the existing entry will be updated; otherwise, a new entry will be created.
- Request Body:

  ```json
  {
    "scooter_id": "integer",
    "fault_notes": "string"
  }
  ```

- Response:
  - Status Code: `200 OK`
  - Body:
    ```json
    {
      "message": "Scooter fault updated successfully."
    }
    ```

Resolve Scooter Fault

- Endpoint: `/fault/resolve_scooter_fault/<int:fault_id>`
- Method: `PUT`
- Description: Resolves a fault entry for a scooter by its fault ID, marking it as resolved and adding resolution notes.
- Request Body:

  ```json
  {
    "resolution_notes": "string"
  }
  ```

- Response:
  - Status Code: `200 OK`
  - Body:
    ```json
    {
      "message": "Scooter fault resolved successfully."
    }
    ```

Get Open Faults

- Endpoint: `/fault/open_faults`
- Method: `GET`
- Description: Retrieves a list of all open faults in the system.
- Response:
  - Status Code: `200 OK`
    - Body:
    ```json
    [
      {
        "faultID": "integer",
        "scooterID": "integer",
        "startDateTime": "string (ISO 8601)",
        "status": "string",
        "faultNotes": "string",
        "resolution": "string or null"
      },
      ...
    ]
    ```

Get Latest Fault by Scooter ID

- Endpoint: `/fault/scooter/<int:scooter_id>`
- Method: `GET`
- Description: Retrieves the latest fault entry for a specific scooter.
- Response:

  - Status Code: `200 OK`

    - Body:

      ```json
      {
        "faultID": "integer",
        "scooterID": "integer",
        "startDateTime": "string (ISO 8601)",
        "status": "string",
        "faultNotes": "string",
        "resolution": "string or null"
      }
      ```

    - Status Code: `404 Not Found`
      - Body:
        ```json
        {
          "message": "Fault not found for the specified scooter."
        }
        ```

Get Fault by ID

- Endpoint: `/fault/<int:fault_id>`
- Method: `GET`
- Description: Retrieves a fault entry by its fault ID.
- Response:

  - Status Code: `200 OK`
  - Body:

    ```json
    {
      "faultID": "integer",
      "scooterID": "integer",
      "startDateTime": "string (ISO 8601)",
      "status": "string",
      "faultNotes": "string",
      "resolution": "string or null"
    }
    ```

  - Status Code: `404 Not Found`
    - Body:
      ```json
      {
        "message": "Fault not found."
      }
      ```
