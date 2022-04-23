"""Contains tests for mail manager module"""
import builtins
import mock
from unittest.mock import patch

from mail_manager import Email


@patch("smtplib.SMTP_SSL")
def test_log_to_admin_email(mock_smtp):
	"""Checks if method correctly calls smtp connection (it is mocked) and checks if logging into
	account is also called with provided arguments (password input also had to be mocked"""

	# GIVEN
	test_email = Email()
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

