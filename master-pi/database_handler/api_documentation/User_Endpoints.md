### User Endpoints

Get Customer Details

- Endpoint: `/user/<email>`
- Method: `GET`
- Description: Retrieves the details of a customer by their email.
- Response:
  - Status Code: `200 OK`
  - Body:
    ```json
    {
      "email": "string",
      "first_name": "string",
      "last_name": "string",
      "phone_no": "string",
      "funds": "float",
      "role": "string"
    }
    ```
  - Status Code: `404 Not Found`
  - Body:
    ```json
    {
      "message": "Customer not found."
    }
    ```

Register a New Customer

- Endpoint: `/user/register`
- Method: `POST`
- Description: Registers a new customer with the provided details.
- Request Body:

  ```json
  {
  "email": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "phone_no": "string",
  "funds": "float" (optional),
  "role": "string" (optional),
  }
  ```

- Response

  - Status Code: `201 Created`
  - Body:

    ```json
    {
      "message": "Customer registered successfully."
    }
    ```

  - Status Code: `500 Internal Server Error`
  - Body:

    ```json
    {
      "error": "An unexpected error occurred."
    }
    ```

Get Login Details

- Endpoint: `/user/login/<email>`
- Method: `GET`
- Description: Retrieves login details for a customer based on their email.
- Response:

  - Status Code: `200 OK`
  - Body:

    ```json
    {
      "email": "string",
      "password": "string"
    }
    ```

  - Status Code: 404 Not Found
  - Body:

    ```json
    {
      "message": "User not found."
    }
    ```

Delete a Customer

- Endpoint: `/user/delete/<email>`
- Method: `DELETE`
- Description: Deletes a customer from the database based on their email.
- Response:

  - Status Code: `200 OK`
  - Body:

    ```json
    {
      "message": "Customer deleted successfully."
    }
    ```

  - Status Code: `400 Bad Request`
  - Body:

    ```json
    {
      "error": "error_message"
    }
    ```

Update Customer Funds

- Endpoint: `/user/update_funds`
- Method: `PUT`
- Description: Updates the funds of a customer.
- Request Body:

  ```json
  {
    "email": "string",
    "funds": "float"
  }
  ```

- Response:

  - Status Code: `200 OK`
  - Body:

    ```json
    {
      "message": "Customer funds updated successfully."
    }
    ```

Get All Customers

- Endpoint: `/user/customers`
- Method: `GET`
- Description: Retrieves the details of all customers in the system.
- Response:
  - Status Code: `200 OK`
    - Body:
      ```json
      [
        {
          "email": "customer1@example.com",
          "first_name": "John",
          "last_name": "Doe",
          "phone_no": "1234567890",
          "funds": 100.0,
          "role": "Customer"
        },
        {
          "email": "customer2@example.com",
          "first_name": "Jane",
          "last_name": "Smith",
          "phone_no": "0987654321",
          "funds": 250.5,
          "role": "Customer"
        }
      ]
      ```
  - Status Code: `404 Not Found`
    - Body:
      ```json
      {
        "message": "No customers found."
      }
      ```

Update User Details

- Endpoint: `/user/update_details/<email>`
- Method: `PUT`
- Description: Updates the details of a user based on the provided email address.
- Request Body:

  ```json
  {
  "password": "string" (optional),
  "first_name": "string" (optional),
  "last_name": "string" (optional),
  "phone_no": "string" (optional),
  "funds": "float" (optional),
  "role": "string" (optional)
  }
  ```

- Response:
  - Status Code: `200 OK`
    - Body:
      ```json
      {
        "message": "User details updated successfully."
      }
      ```

Get Engineer Emails

- Endpoint: `/user/engineers/emails`
- Method: `GET`
- Description: Retrieves the email addresses of all users with the role of "Engineer."
- Response:

  - Status Code: `200 OK`

    - Body:
      ```json
      {
        "engineer1@example.com",
        "engineer2@example.com"
      }
      ```

  - Status Code: `404 Not Found`
    - Body:
      ```json
      {
        "message": "No engineers found."
      }
      ```
