# Scooter Web Application

This web application allows customers to register, log in, and manage scooter bookings.

It also allows engineers to log in with the domain `@engineer.com` and view/repair scooter faults.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Usage](#usage)
- [Test Accounts](#test-accounts)

## Features

### Customers

- Customer registration and login
- Password Reset for forgotten password
- Dashboard to view available scooters
- Booking management
- Add bookings to Google Calendar
- Booking scooters
- Find and locate your scooter
- Top up account funds
- Report scooter faults
- Generate QR Code to log into and out of scooter

### Engineers

- Engineer registration and login
- Password Reset for forgotten password
- Seperate Dashboard to view engineer scooter details
- View Scooter Faults
- View location of scooter on maps
- Add fault repair notes
- Generate QR Code to log into and out of scooter

## Technologies Used

- [Flask](https://flask.palletsprojects.com/)
- Python
- HTML/CSS for front-end rendering
- WebSocket for communication with Master Pi
- Google Calendar API
- Google Maps
- QR Code Generator

## Usage

To start the application, run the following command from the `/agent-pi` directory:

```
python frontend/
```

Open the web browser on the host Pi and navigate to http://localhost:8000 to access the application.
d
Otherwise, you can also access the application from http://agent-pi-IP:8000, where _agent-pi-IP_ is the IP Address of the Pi hosting the frontend application

## Test Accounts

Below are test accounts available for use for customers. Otherwise, feel free to register your own account:

| Email                      | Password              |
| -------------------------- | --------------------- |
| alice.smith@example.com    | password123           |
| bob.jones@example.com      | securepass            |
| charlie.brown@example.com  | charlie123            |
| group12.cosc2674@gmail.com | Mayday-Bunny-Isotope8 |

Below are test accounts available for use for engineers. Otherwise, feel free to register your own account:

| Email             | Password |
| ----------------- | -------- |
| tony@engineer.com | ironman  |
