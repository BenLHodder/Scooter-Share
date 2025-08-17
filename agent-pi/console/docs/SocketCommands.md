# Socket Commands
### When sending data or wanting to get data from database through the Master Pi, a command is used to specify what is being sent or what is needing to be sent back.

## 1. AUTH
### AUTH is used when wanting to retrieve a hash for a username. The hash is used to compare with the password entered when trying to login to the Agent Pi, if there is no match for username in the database None should be returned and the user should be prompted to register an account.

## 2. GSS
### GSS is used to signify when wanting to get the current status of a scooter. A scooters status is used to check if it is free for use or if it has been booked ect.

## 3. SS 
### SS is used to set the status of the scooter in the Database. This might be because a user has logged into the scooter or it something has gone wrong with the scooter and needs fixing.

## 4. GSI
### GSI is used to get the scooter info, this is called when the Agent Pi is turned on and the scooter needs to get it's cost, location and status to init with.