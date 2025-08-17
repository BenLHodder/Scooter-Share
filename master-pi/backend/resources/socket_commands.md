# Sockets Commands

## How To Use

When Sending a request to the master pi though sockets, the socket handler reads a single message that has the command and payload. The message may be sent in multiple partitions depending on size, the message is split as following:

```python
message = {
    "command": command: str,
    "payload": payload: json{}
}
```

For an example lets use the Add Booking command, taken from the API documentation we need the request body to have:

```json
{
  "email": "string",
  "scooter_id": "integer",
  "start_datetime": "string (ISO 8601)",
  "end_datetime": "string (ISO 8601)",
  "cost": "float"
}
```

![alt text](<Screenshot 2024-09-15 at 11.14.25 PM.png>)
The command to add a booking is "AB" taken from the table below, to send this through sockets from the agent pi to the master pi the message needs to look like this to be succesfully read and handled by socket_handler:

```python
message = {
    "command": "AB",
    "payload": {
        "email": "test@mail.com",
        "scooter_id": 1,
        "start_datetime": "Sun, 01 Sep 2024 10:00:00 GMT",
        "end_datetime": "Sun, 01 Sep 2024 10:30:00 GMT",
        "cost": 15.00
    }
}
```

The socket handler always returns a json message back, this is either a success, error message or in the case of requesting data a json format just like the payload in the above code but without the command.

## Booking API

| Command | Description                   |
| ------- | ----------------------------- |
| GBD     | Get Booking Details           |
| AB      | Add Booking                   |
| CB      | Cancel Booking                |
| SB      | Start Booking                 |
| EB      | End Booking                   |
| GAB     | Get All Bookings              |
| GABS    | Get All Booked Scooters Times |
| GBI     | Get booking ID                |
| SBG     | Set booking google ID         |

---

## Customer API

| Command | Description              |
| ------- | ------------------------ |
| GCD     | Get Customer Details     |
| RNC     | Register New Customer    |
| GLD     | Get Login Details        |
| DC      | Delete Customer          |
| UCF     | Update Customer Funds    |
| GAC     | Get All Customer Details |
| UCD     | Update Customer Details  |

---

## Scooter API

| Command | Description             |
| ------- | ----------------------- |
| GSD     | Get Scooter Details     |
| USS     | Update Scooter Status   |
| RSF     | Report Scooter Fault    |
| GAS     | Get All Scooters        |
| USI     | Update Scooter IP       |
| USL     | Update Scooter Location |
| FMS     | Find My Scooter         |

---

## Transaction API

| Command | Description                   |
| ------- | ----------------------------- |
| GTD     | Get Transaction Details       |
| ANT     | Add New Transaction           |
| GACT    | Get All Customer Transactions |

---

## Fault Log API

| Command | Description             |
| ------- | ----------------------- |
| GFBI    | Get fault by ID         |
| GOF     | Get open faults         |
| GFBS    | Get fault by scooter ID |
| USF     | Update scooter fault    |
| RESF    | Resolve scooter fault   |

---

---
