"""Collects test from program module"""
from program import Program


def test_fill_message_template():
    """Checks if method correctly fill message template with provided arguments"""

    # GIVEN
    test_program = Program()
    expected_message = "From: System alert\n" \
                       "Subject: Raw material 22REW needs review\n" \
                       "Reminder!\n Raw material 22REW has 200 kg " \
                       "stock and was reviewed last time on 2022-04-19"
    # WHEN
    message = test_program.fill_message_template("22REW", "200", "2022-04-19")
    # THEN
    assert message == expected_message
