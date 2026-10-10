import pandas as pd
from datetime import datetime

CSV_FILE = "data.csv"

df = pd.read_csv(CSV_FILE)


AUDITORIUMS = ["Audi 1", "Audi 2", "Audi 3", "Audi 4"]


def load_bookings():
    try:
        return pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        return pd.DataFrame(
            columns=[
                "booking_id",
                "audi_name",
                "user_name",
                "date",
                "start_time",
                "end_time"
            ]
        )


def check_availability(df, audi_name, date, start_time, end_time):

    # Select only bookings for same auditorium and date
    existing = df[
        (df["audi_name"] == audi_name) &
        (df["date"] == date)
    ]

    new_start = datetime.strptime(start_time, "%H:%M")
    new_end = datetime.strptime(end_time, "%H:%M")

    for _, booking in existing.iterrows():

        booked_start = datetime.strptime(
            booking["start_time"], "%H:%M"
        )

        booked_end = datetime.strptime(
            booking["end_time"], "%H:%M"
        )

        # Check time overlap
        if new_start < booked_end and new_end > booked_start:
            return False

    return True


def make_booking():

    df = load_bookings()

    print("\nAvailable Auditoriums:")
    for audi in AUDITORIUMS:
        print("-", audi)

    audi_name = input("\nEnter auditorium: ")

    if audi_name not in AUDITORIUMS:
        print("Invalid auditorium.")
        return

    user_name = input("Enter your name: ")
    date = input("Enter date (YYYY-MM-DD): ")
    start_time = input("Enter start time (HH:MM): ")
    end_time = input("Enter end time (HH:MM): ")

    # Convert time to validate
    start = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")

    # Auditorium can only be booked between 9 AM and 4 PM
    opening = datetime.strptime("09:00", "%H:%M")
    closing = datetime.strptime("16:00", "%H:%M")

    if start < opening or end > closing or start >= end:
        print("Booking must be between 09:00 AM and 04:00 PM.")
        return

    # Check availability
    available = check_availability(
        df,
        audi_name,
        date,
        start_time,
        end_time
    )

    if not available:
        print("\nAlready booked - choose a different time.")
        return

    # Generate booking ID
    if df.empty:
        booking_id = 1
    else:
        booking_id = df["booking_id"].max() + 1

    new_booking = pd.DataFrame([{
        "booking_id": booking_id,
        "audi_name": audi_name,
        "user_name": user_name,
        "date": date,
        "start_time": start_time,
        "end_time": end_time
    }])

    # Add booking
    df = pd.concat([df, new_booking], ignore_index=True)

    # Save to CSV
    df.to_csv(CSV_FILE, index=False)

    print("\nBooking successful!")
    print(new_booking)


def show_bookings():

    df = load_bookings()

    if df.empty:
        print("\nNo bookings found.")
    else:
        print("\nCurrent Bookings:")
        print(df)

def cancel_booking():

    df = load_bookings()

    if df.empty:
        print("\nNo bookings available to cancel.")
        return

    print("\nCurrent Bookings:")
    print(df)

    booking_id = int(input("\nEnter booking ID to cancel: "))

    if booking_id not in df["booking_id"].values:
        print("\nBooking ID not found.")
        return

    # Remove the booking
    df = df[df["booking_id"] != booking_id]

    # Save updated data
    df.to_csv(CSV_FILE, index=False)

    print("\nBooking cancelled successfully.")

while True:

    print("\n----> AUDITORIUM BOOKING SYSTEM <----")
    print("1. Make Booking")
    print("2. Show Bookings")
    print("3. cancel booking")
    print("4. Exit")

    choice = input("Enter your choice: ")

    match choice:

        case "1":
            make_booking()

        case "2":
            show_bookings()
        
        case "3":
            cancel_booking()

        case "4":
            print("Thank you!")
            break

        case _:
            print("Invalid choice.")