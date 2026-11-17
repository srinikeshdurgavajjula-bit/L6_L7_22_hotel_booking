import string

import pytest
from hypothesis import assume, given, strategies as st

from hotel_booking import nights_stayed, room_floor, booking_label


@given(st.text() | st.none())
def test_nights_stayed_handles_arbitrary_input(value):
    try:
        result = nights_stayed(value)
    except ValueError:
        return
    assert isinstance(result, int)


@given(st.text() | st.none())
def test_room_floor_handles_arbitrary_input(value):
    try:
        result = room_floor(value)
    except ValueError:
        return
    assert isinstance(result, int)


@given(st.text() | st.none())
def test_booking_label_handles_arbitrary_input(value):
    try:
        result = booking_label(value)
    except ValueError:
        return
    assert isinstance(result, str)


@given(
    check_in=st.integers(min_value=1, max_value=31),
    check_out=st.integers(min_value=1, max_value=31),
)
def test_nights_stayed_valid_days(check_in, check_out):
    assume(check_out >= check_in)
    assert nights_stayed(f"{check_in}-{check_out}") == check_out - check_in


@given(
    floor=st.integers(min_value=1, max_value=9),
    room_number=st.integers(min_value=0, max_value=999),
)
def test_room_floor_valid_room_codes(floor, room_number):
    room_code = f"D-{floor}{room_number:03d}"
    assert room_floor(room_code) == floor


@given(
    names=st.lists(
        st.text(alphabet=string.ascii_letters, min_size=1, max_size=12),
        min_size=1,
        max_size=5,
    )
)
def test_booking_label_valid_names(names):
    names_csv = ", ".join(names)
    expected = names[0][0].upper() + names[0][1:] + " +" + str(len(names) - 1)
    assert booking_label(names_csv) == expected


@pytest.mark.parametrize(
    "value", [None, "", "12", "12-15-18", "x-y", "15-12", "0-1"]
)
def test_invalid_nights_are_rejected(value):
    with pytest.raises(ValueError):
        nights_stayed(value)


@pytest.mark.parametrize(
    "value", [None, "", "D-", "305", "D-ABC", "D-030", "DD-305"]
)
def test_invalid_room_codes_are_rejected(value):
    with pytest.raises(ValueError):
        room_floor(value)


@pytest.mark.parametrize(
    "value", [None, "", " , ", "ravi,,priya", "ravi, "]
)
def test_invalid_guest_names_are_rejected(value):
    with pytest.raises(ValueError):
        booking_label(value)
