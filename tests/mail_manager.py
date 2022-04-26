"""Contains tests for mail manager module"""
import builtins
import smtplib
from unittest.mock import patch
import mock
from mail_manager import Email


@patch("smtplib.SMTP_SSL")
def test_log_to_admin_email(mock_smtp):
    """Checks if logging into account is called with
    provided arguments (password input had to be mocked)"""

    test_email = Email()
    with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) as test_email.server:
        # GIVEN

        test_fake_password = "fake_pass_content"
        context = mock_smtp.return_value.__enter__.return_value
        # WHEN
        with mock.patch.object(builtins, "input", lambda _: test_fake_password):
            test_email.log_to_admin_email()
        # THEN
        mock_smtp.assert_called()
        context.login.assert_called()
        context.login.assert_called_with(
            user="autoadmfactor@gmail.com",
            password=test_fake_password
        )


@patch("smtplib.SMTP_SSL")
def test_log_to_admin_email_wrong_password(mock_smtp):
    """Checks if logging into account is called with provided
    arguments (password input had to be mocked)"""

    test_email = Email()
    with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) as test_email.server:
        # GIVEN

        test_fake_password = "fake_pass_content"
        context = mock_smtp.return_value.__enter__.return_value

        # WHEN
        with mock.patch.object(builtins, "input", lambda _: test_fake_password):
            test_email.log_to_admin_email()
        # THEN
        mock_smtp.assert_called()
        context.login.assert_called()
        context.login.assert_called_with(
            user="autoadmfactor@gmail.com",
            password=test_fake_password
        )


@patch("smtplib.SMTP_SSL")
def test_send_email(mock_smtp):
    """Checks if method correctly calls submethod directly responsible for sending email
    with provided arguments. Used mocked connection instead of real one"""

    #GIVEN
    test_email = Email()
    with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) as test_email.server:

        context = mock_smtp.return_value.__enter__.return_value
        test_fake_password = "test_fake_pass"
        with mock.patch.object(builtins, "input", lambda _: test_fake_password):
            test_email.log_to_admin_email()

        #WHEN
        test_email.send_email(mail_to=test_email.admin_email, msg_content="witam")
        #THEN
        context.login.assert_called()
        context.sendmail.assert_called_with(
            from_addr=test_email.admin_email,
            to_addrs=test_email.admin_email,
            msg="witam")


def test_create_email_template():
    """Checks if methos correctly creates complete email message from template"""

    #GIVEN
    test_email = Email()
    expected_email_content = "From: Alert from system\n"\
                             "Subject: Raw material RAW23 needs review\n"\
                             "Reminder!\nRaw material RAW23 has 2010 kg "\
                             "stock and was reviewed last time on 22-04-2022"
    #WHEN
    test_email_content = test_email.create_email_template(
        material_name="RAW23", stock="2010",last_review_date="22-04-2022")
    #THEN
    assert test_email_content == expected_email_content
