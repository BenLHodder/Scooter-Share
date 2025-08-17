### Transaction Endpoints

Get Transaction Details

- Endpoint: `/transaction/<int:transaction_id>`
- Method: `GET`
- Description: Retrieves the details of a transaction by its ID.
- Response:
  - Status Code: `200 OK`
  - Body:
    ```json
    {
      "transaction_id": "integer",
      "email": "string",
      "transaction_amount": "float",
      "transaction_datetime": "string (ISO 8601)"
    }
    ```
  - Status Code: `404 Not Found`
  - Body:
    ```json
    {
      "message": "Transaction not found."
    }
    ```

Add a New Transaction

- Endpoint: `/transaction/add_transaction`
- Method: `POST`
- Description: Adds a new transaction for a customer.
- Request Body:

  ```json
  {
    "email": "string",
    "transaction_amount": "float",
    "transaction_datetime": "string (ISO 8601)"
  }
  ```

- Response:

  - Status Code: `200 OK`
  - Body:

    ```json
    {
      "message": "Transaction added successfully."
    }
    ```

Get All Transactions for a Customer

- Endpoint: `/transaction/get_transactions/<string:email>`
- Method: `GET`
- Description: Retrieves all transactions associated with a specific customer.
- Response:
  - Status Code: `200 OK`
  - Body:
    ```json
    {
      "transactions": [
        {
          "transaction_id": "integer",
          "email": "string",
          "transaction_amount": "float",
          "transaction_datetime": "string (ISO 8601)"
        }
      ]
    }
    ```
  - Status Code: `400 Bad Request`
  - Body:
    ```json
    {
      "error": "error_message"
    }
    ```
