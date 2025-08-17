-- Drop tables if they exist to avoid conflicts
DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS Transaction;
DROP TABLE IF EXISTS FaultLog;
DROP TABLE IF EXISTS Scooter;
DROP TABLE IF EXISTS SystemUser;

-- Creating Customer table
CREATE TABLE SystemUser (
    email VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    firstName VARCHAR(100),
    lastName VARCHAR(100),
    phoneNo VARCHAR(20),
    funds REAL,
    role VARCHAR(50) DEFAULT 'Customer' CHECK (role IN ('Customer', 'Admin', 'Engineer'))
);

-- Creating Scooter table
CREATE TABLE Scooter (
    scooterID SERIAL PRIMARY KEY,
    make VARCHAR(100),
    colour VARCHAR(50),
    longitude REAL,
    latitude REAL,
    costMin REAL,
    batteryPercentage INT,
    status VARCHAR(50),
    ipAddress VARCHAR(50)
);

-- Creating Booking table with foreign keys
CREATE TABLE Booking (
    email VARCHAR(255),
    scooterID INT,
    bookingID SERIAL PRIMARY KEY,
    startDateTime TIMESTAMP WITH TIME ZONE NOT NULL,  -- Use TIMESTAMP WITH TIME ZONE
    endDateTime TIMESTAMP WITH TIME ZONE,              -- Use TIMESTAMP WITH TIME ZONE
    actualStartDateTime TIMESTAMP WITH TIME ZONE,      -- Actual start time
    actualEndDateTime TIMESTAMP WITH TIME ZONE,        -- Actual end time
    cost REAL,
    depositCost REAL,
    googleID VARCHAR(255),
    status VARCHAR(50) DEFAULT 'Active' CHECK (status IN ('Active', 'Complete', 'Cancelled')),
    FOREIGN KEY (email) REFERENCES SystemUser(email) ON DELETE CASCADE,
    FOREIGN KEY (scooterID) REFERENCES Scooter(scooterID) ON DELETE SET NULL
);

-- Creating Transaction table with foreign keys
CREATE TABLE Transaction (
    email VARCHAR(255),
    transactionID SERIAL PRIMARY KEY,
    datetime TIMESTAMP WITH TIME ZONE NOT NULL,        -- Use TIMESTAMP WITH TIME ZONE
    transactionAmount REAL,
    FOREIGN KEY (email) REFERENCES SystemUser(email) ON DELETE CASCADE
);

-- Creating FaultLog table
CREATE TABLE FaultLog (
    faultID SERIAL PRIMARY KEY,  -- Primary Key
    scooterID INT,               -- Foreign Key referring to Scooter table
    startDateTime TIMESTAMP WITH TIME ZONE NOT NULL,  -- Start time of fault
    endDateTime TIMESTAMP WITH TIME ZONE,            -- End time of fault
    status VARCHAR(50) CHECK (status IN ('Open', 'Resolved', 'In Progress')),  -- Status of the fault
    resolution TEXT,             -- Notes on the fault resolution
    faultNotes TEXT,             -- Notes on the fault
    FOREIGN KEY (scooterID) REFERENCES Scooter(scooterID) ON DELETE CASCADE
);

-- Set the timezone to AEST for the current session
ALTER DATABASE scooter_system SET timezone TO 'Australia/Sydney';