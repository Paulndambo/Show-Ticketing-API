# Show Ticketing
This is a simple backend application enabling admins to manage theaters and seating arrangements, and users
to view and reserve seats for specific dates and shows.

Application functionality;
- User Management.
- Theater management (CRUD).
- Show Management.
- Seat Arrangment Management.
- Seat Reservation.
- Seat Reservation notification.
- Reservation Cancellation.

# Models
- Theater: Contains information about movie theaters.
- Show: A show happening in a certain theater on a certain day.
- TheaterSeating: Contains information on seating arrangement for a certain show in a certain theater.
- Reservation: Contains information about seat reservations.
- User: Information about users.
- AbstractBaseModel: contains information that is common to all models.

# Notes
These are the guidelines on which the application is built;-
1. It is assumed that, that the expected attendance for every show is equal to the capacity of the theater.
2. For every show, the admin has the ability to decide the seating arrangement. This means, Even though the number of available seats remains the same(remember this is determined by the capacity of the theater), The admin will be able to decide on the number of rows, which will then be the basis on which the seat numbers are generated.
3. For simplicity purposes, it is assumed that all seats will cost the same.
4. A theater is considered available on a specific date if it does not have a show planned on that date.

# Additionals
1. The test email server (mailhog) is accessible on: <link>http://34.173.224.151:8025/</link>
2. The test redis server is accessible on: <link>http://34.123.255.211:8001/</link>
3. A deployed version of the project is accessible on: <link>http://34.173.224.151:8000</link>

# How to run
### Clone the repo
1. You can clone the repo using any of the following commands
```sql
git clone https://github.com/Paulndambo/Show-Ticketing-API.git
```
or
```sql
git clone git@github.com:Paulndambo/Show-Ticketing-API.git
```

2. After cloning the repo ()
- Change directory into cloned folder using;-
```sql 
cd Show-Ticketing-API
```

- Create a virtual environment for the project using;-
```sql
python -m venv venv
```
or
```sql 
python3 -m venv venv
```
- Install required packages using the command;-
```sql
pip install -r requirements.txt
```

- Activate the virtual environment, using the command;-
```sql
source venv/bin/activate
```
or 
```sql
source venv/Scripts/activate
```

- Start Server, using the command;-
```sql
python manage.py runserver
```
or 
```sql
python3 manage.py runserver
```

- The server is now accessible on <link>http://127.0.0.1:8000</link>

2. Running Using Docker
To run the project using docker, use the command below;-
```sql
docker compose up --build
```

### Running tests
- Using pytest
```sql
pytest -s -v
```
- Using builtin test command
```sql
python manage.py test
```
or
```sql
python3 manage.py test
```


# Assessment Parts samples requests & Payloads
- BASE_URL ```http://localhost:8000```

### User Authentication

- Register a new user
```sql
curl  -X POST \
  'http://127.0.0.1:8000/users/register/' \
  --header 'Accept: */*' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "first_name": "John",
  "last_name": "Smith",
  "email": "johnsmith@gmail.com",
  "phone_number": "07123456789",
  "username": "johnsmith",
  "password": "1234",
  "gender": "Male",
  "role": "Customer"
}'
```

- Login to obtain a JWT token
```sql
curl  -X POST \
  'http://127.0.0.1:8000/users/login/' \
  --header 'Accept: */*' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "username": "janedoe",
  "password": "1234"
}'
```

- Use the JWT token to authenticate requests
```sql
curl  -X GET \
  'http://127.0.0.1:8000/users/' \
  --header 'Accept: */*' \
  --header 'Authorization: Bearer {{token}}'
```

### Admin Management
- Create a new theater with a specified number of seats
```sql
curl  -X POST \
  'http://127.0.0.1:8000/theaters/' \
  --header 'Accept: */*' \
  --header 'Authorization: Bearer {{token}}' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "name": "Nairobi Cinema",
  "location_description": "Next to KICC",
  "location": [1.234, 36.789],
  "town": "CBD, Nairobi",
  "number_of_seats": 150,
  "number_of_screens": 5,
  "opened_on": "2000-01-23"
}'
```
- Create seating for a specific date
```sql
curl  -X POST \
  'http://127.0.0.1:8000/theaters/shows/' \
  --header 'Accept: */*' \
  --header 'Authorization: Bearer {{token}}' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "title": "AFCON 2027 Opening Ceremony",
  "theater": 5,
  "ticket_cost": 350,
  "show_date": "2027-06-07",
  "show_time": "16:00",
  "seating_arrangement": {
    "number_of_rows": 10
  }
}'
```
- List all reservation details for every seating
```sql
curl  -X GET \
  'http://127.0.0.1:8000/theaters/shows/' \
  --header 'Accept: */*' \
  --header 'Authorization: Bearer {{token}}'
```

### User Interaction
- List all theaters available for specific dates
```sql
curl  -X GET \
  'http://127.0.0.1:8000/theaters/?date=2024-07-14' \
  --header 'Accept: */*' \
  --header 'Authorization: Bearer {{token}}'
```
- List available seats selected theater.
```sql
curl  -X GET \
  'http://127.0.0.1:8000/theaters/seatings/?theater=2&booked=false' \
  --header 'Accept: */*' \
  --header 'Authorization: Bearer {{token}}'
```
- Reserve a preferred seat for a specific show
1. Single seat reservation
```sql
curl  -X POST \
  'http://127.0.0.1:8000/reservations/reserve-seat/' \
  --header 'Accept: */*' \
  --header 'Authorization: Bearer {{token}}' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "seats": [269],
  "show": 6,
  "ticket_cost": 500 
}'
```
2. Multiple seats reservation
```sql
curl  -X POST \
  'http://127.0.0.1:8000/reservations/reserve-seat/' \
  --header 'Accept: */*' \
  --header 'Authorization: Bearer {{token}}' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "seats": [265, 266, 267],
  "show": 6,
  "ticket_cost": 500 
}'
```