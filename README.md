# Show Ticketing
This is a simple backend application enabling admins to manage theaters and seating arrangements, and users
to view and reserve seats for specific dates and shows.

Application functionality;
- User Management.
- Theater management (CRUD).
- Show Management.
- Seat Arrangment Management.
- Seat Reservation.


# Notes
These are the guidelines on which the application is built;-
1. It is assumed that, that the expected attendance for every show is equal to the capacity of the theater.
2. For every show, the admin has the ability to decide the seating arrangement. This means, Even though the number of available seats remains the same(remember this is determined by the capacity of the theater), The admin will be able to decide on the number of rows, which will then be the basis on which the seat numbers are generated.
3. For simplicity purposes, it is assumed that all seats will cost the same.
4. A theater is considered available on a specific date if it does not have a show planned on that date.