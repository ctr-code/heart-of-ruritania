# The Heart of Ruritania

A warm welcome awaits at The Heart of Ruritania, the UK's first Ruritanian restaurant.

[Learn more and book online at our website](https://ruritania-a4a079b504db.herokuapp.com/).

# Entity-Relationship Diagram


``` mermaid
erDiagram
    User ||--o{ Reservation : booked
    User {
        int user_id PK
        string name
        string email
        string first_name
        string last_name
        string phone_number
    }
    Reservation {
        int reservation_id PK
        string date
        string time
        int guest_count
        string status
        int user_id FK
    }
    Table {
        int table_id PK
        int table_number
        int seat_count
    }
    OpeningHours {
        int hours_id PK
        int day_of_week "1-mon to 7-sun"
        string start_time "24-hour clock"
        string end_time "24-hour clock"
    }
    OpeningExceptions {
        int exception_id PK
        string date
        string start_time "24-hour clock"
        string end_time "24-hour clock"
    }
```

If Reservations are proactively mapped to Tables you can arrive in a situation where there is always a table free but never for long enough to accept a booking, so the restaurant capacity is underutilised.

To achieve an optimal mapping reservations need to be mapped to tables every time the reservations change.  Since it needs to be recalculated repeatedly there is little point in keeping the mapping in the database.
