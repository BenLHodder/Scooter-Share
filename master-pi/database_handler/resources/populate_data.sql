-- Inserting data into Customer table
INSERT INTO SystemUser (email, password, firstName, lastName, phoneNo, funds)
VALUES 
    -- Password: password123
    ('alice.smith@example.com', 'pbkdf2:sha256:260000$9dm3GfAdiFbeLvpp$53d16bff6f7a6e2a5bfde3eefdd77e22498eb101000fa899604a72df5ade7383', 'Alice', 'Smith', '555-1234', 150.50),
    -- Password: securepass
    ('bob.jones@example.com', 'pbkdf2:sha256:260000$eEiJtSmRK6V4Vuc6$d322ea4221bc1741c5d180ce380e100136b46f40bc08334c940c8b776536febb', 'Bob', 'Jones', '555-5678', 75.00),
    -- Password: charlie123
    ('charlie.brown@example.com', 'pbkdf2:sha256:260000$gJBcDmjIlT11JdIH$ff95c387d067544d835496b883243712149090ea1b1ddabf43ae7daae79df8f9', 'Charlie', 'Brown', '555-8765', 200.00),
    -- Password: Mayday-Bunny-Isotope8
    ('group12.cosc2674@gmail.com', 'pbkdf2:sha256:260000$iVAnpqGRgseplQ00$3d5ed9e530fce9756cc0029381c5070cb6be2f37555f47f7ef5edc6772fe14b8', 'John', 'Doe', '1234567890', 100.00);

INSERT INTO SystemUser (email, password, firstName, lastName, phoneNo, funds, role)
VALUES
    -- Username: admin || Password: admin
    ('admin', 'pbkdf2:sha256:600000$Zl15CGx1wlFRsSwa$48f1ffd14f24002c829b92592a1375965f1e6cc26b5a01dcf4b5e6aac64a525b', 'admin', 'admin', '1234567890', 1000000.00, 'Admin'),
    -- Username: tony@engineer.com || Password: ironman
    ('8dbc91ced24bf407c4cf1aed3781f12cb9969f08f492ecd5f0f17b593a20e074', 'pbkdf2:sha256:600000$BL7GVo6vmZwzppaE$a6ca274086afa7069983d52e601b4bb121aa7383ae4a961168a5ed60fff7e6d0', 'Tony', 'Stark', '555-1234', 1000000.00, 'Engineer');

-- Inserting data into Scooter table
INSERT INTO Scooter (make, colour, costMin, batteryPercentage, status, ipAddress, longitude, latitude)
VALUES 
    ('Xiaomi', 'Black', 0.15, 85, 'Available', '192.168.1.10', -74.0059413, 40.7127837),
    ('Segway', 'Red', 0.18, 60, 'In Use', '192.168.1.11', -73.968285, 40.785091),
    ('Ninebot', 'Blue', 0.12, 100, 'Available', '192.168.1.12', -73.977622, 40.758896),
    ('Bird', 'White', 0.20, 45, 'Charging', '192.168.1.13', -73.935242, 40.730610);

-- Inserting data into Booking table
INSERT INTO Booking (email, scooterID, startDateTime, endDateTime, actualStartDateTime, actualEndDateTime, cost, depositCost, googleID, status)
VALUES
    ('alice.smith@example.com', 1, '2024-09-01 10:00:00', '2024-09-01 10:30:00', '2024-09-01 10:00:00', '2024-09-01 10:30:00', 4.50, 1.50, NULL, 'Complete'),
    ('bob.jones@example.com', 2, '2024-09-02 12:00:00', '2024-09-02 12:45:00', '2024-09-02 12:00:00', '2024-09-02 12:45:00', 8.10, 2.00, NULL, 'Complete'),
    ('charlie.brown@example.com', 3, '2024-09-03 08:00:00', '2024-09-03 08:20:00', '2024-09-03 08:00:00', '2024-09-03 08:20:00', 2.40, 1.00, NULL,'Complete'),
    ('alice.smith@example.com', 4, '2024-09-04 15:00:00', '2024-09-04 15:30:00', '2024-09-04 15:00:00', '2024-09-04 15:30:00', 6.00, 1.80, NULL,'Complete');

-- Inserting data into Transaction table
INSERT INTO Transaction (email, datetime, transactionAmount)
VALUES
    ('alice.smith@example.com', '2024-09-01 10:35:00', -4.50),
    ('bob.jones@example.com', '2024-09-02 12:50:00', -8.10),
    ('charlie.brown@example.com', '2024-09-03 08:25:00', -2.40),
    ('alice.smith@example.com', '2024-09-04 15:35:00', -6.00);

-- Inserting data into FaultLog table
INSERT INTO FaultLog (scooterID, startDateTime, endDateTime, status, resolution)
VALUES
    (2, '2024-09-02 13:00:00', '2024-09-02 16:00:00', 'Resolved', 'Battery replaced'),
    (4, '2024-09-04 09:00:00', '2024-09-04 11:00:00', 'Resolved', 'Low battery issue fixed'),
    (3, '2024-09-05 14:30:00', NULL, 'Open', NULL),
    (1, '2024-09-06 08:00:00', '2024-09-06 09:30:00', 'Resolved', 'Scooter software updated');
