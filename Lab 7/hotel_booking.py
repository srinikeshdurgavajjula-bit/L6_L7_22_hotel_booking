import re


def nights_stayed(days):
    if not isinstance(days, str):
        raise ValueError("days must be text in check-in-check-out format")

    match = re.fullmatch(r"\s*(\d{1,2})\s*-\s*(\d{1,2})\s*", days)
    if not match:
        raise ValueError("days must contain two day numbers separated by a hyphen")

    check_in, check_out = map(int, match.groups())

    if not (1 <= check_in <= 31 and 1 <= check_out <= 31):
        raise ValueError("days must be between 1 and 31")
    if check_out < check_in:
        raise ValueError("check-out day cannot be before check-in day")

    return check_out - check_in


def room_floor(room_code):
    if not isinstance(room_code, str):
        raise ValueError("room code must be text")

    match = re.fullmatch(r"\s*([A-Za-z])-([1-9]\d*)\s*", room_code)
    if not match:
        raise ValueError("room code must look like D-305")

    room_number = match.group(2)
    return int(room_number[0])


def booking_label(names_csv):
    if not isinstance(names_csv, str):
        raise ValueError("guest names must be text")

    names = [name.strip() for name in names_csv.split(",")]

    if not names or any(not name for name in names):
        raise ValueError("enter one or more non-empty guest names")

    lead = names[0]
    return lead[0].upper() + lead[1:] + " +" + str(len(names) - 1)


def main():
    print("==== Running nights_stayed ====")
    user_input = input("Enter check-in and check-out day (e.g. 12-15): ")
    print("Nights:", nights_stayed(user_input))

    print("\n==== Running room_floor ====")
    user_input = input("Enter a room code (e.g. D-305): ")
    print("Floor:", room_floor(user_input))

    print("\n==== Running booking_label ====")
    user_input = input("Enter guest names as CSV (e.g. ravi, priya): ")
    print("Booking Label:", booking_label(user_input))


if __name__ == "__main__":
    main()
