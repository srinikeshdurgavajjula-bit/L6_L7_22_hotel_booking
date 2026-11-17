import pytest
from hotel_booking import booking_cost, cancellation_refund, room_upgrade


def test_standard_two_nights():
    assert booking_cost("standard", 2, 2, False) == 4000


@pytest.mark.parametrize(
    "room, expected_rate",
    [("standard", 2000), ("deluxe", 3500), ("suite", 6000)],
)
def test_room_rates(room, expected_rate):
    assert booking_cost(room, 1, 2, False) == expected_rate


def test_peak_season_adds_25_percent():
    assert booking_cost("standard", 1, 2, True) == 2500


def test_extra_guest_cost():
    assert booking_cost("standard", 2, 3, False) == 5000


def test_seven_nights_gets_ten_percent_discount():
    assert booking_cost("standard", 7, 2, False) == 12600


def test_unknown_room_raises_error():
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("economy", 1, 2, False)


def test_zero_nights_raises_error():
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 2, False)


def test_full_refund():
    assert cancellation_refund(1000, 10, False) == 1000


def test_partial_refund_for_non_member():
    assert cancellation_refund(1000, 3, False) == 500


def test_partial_refund_plus_member_bonus():
    assert cancellation_refund(1000, 3, True) == 750


def test_no_refund_for_non_member():
    assert cancellation_refund(1000, 1, False) == 0


def test_member_bonus_when_base_refund_is_zero():
    assert cancellation_refund(1000, 1, True) == 250


def test_no_upgrade_when_no_rooms_are_free():
    assert room_upgrade("standard", True, 0) == "standard"


def test_member_standard_upgrades_to_deluxe():
    assert room_upgrade("standard", True, 1) == "deluxe"


def test_member_deluxe_upgrades_to_suite():
    assert room_upgrade("deluxe", True, 1) == "suite"


def test_non_member_does_not_upgrade():
    assert room_upgrade("standard", False, 1) == "standard"


def test_other_room_type_does_not_upgrade():
    assert room_upgrade("suite", True, 1) == "suite"
