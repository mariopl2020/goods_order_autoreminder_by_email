"""Contains functionalities to manage and works with administrator email account"""
from string import Template


class Email():
    """Represents email account"""

    def __init__(self):
        """Initiates email account"""
        self.admin_email = "autoadmfactor@gmail.com"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465
        self.server = None

    def log_to_admin_email(self):
        """Allows administrator to login into his account."""

        admin_password = input("Enter your email password\n")
        self.server.login(user=self.admin_email, password=admin_password)

    def send_email(self, mail_to, msg_content):
        """Sends mail from admin email account to chosen address with parametrized content

        Arguments:
            mail_to (str): email address what will be receiver of message
            msg_content (str): message content"""

        self.server.sendmail(from_addr=self.admin_email, to_addrs=mail_to, msg=msg_content)

    def logout(self):
        """Ends connection with administrator's email server"""

        self.server.close()

    @staticmethod
    def create_email_template(material_name, stock, last_review_date):
        """Creates custom email content to be sent as reminder by using Template class object

        Arguments:
            material_name (str): name of material
            stock (str): stock level [kg]
            last_review_date (str): date of last stock review

        Returns:
            message (str): complete email message content to be sent"""

        message_template = Template("From: $sender\n"
                                    "Subject: $subject\n"
                                    "$body")
        subject_template = Template("Raw material $material_name needs review")
        body_template = Template("Reminder!\nRaw material $material_name has $stock kg " \
                                 "stock and was reviewed last time on $last_review_date")
        sender = "Alert from system"
        subject = subject_template.substitute(material_name=material_name)
        body = body_template.substitute(material_name=material_name, stock=stock,
                                        last_review_date=last_review_date)
        message = message_template.substitute(sender=sender, subject=subject, body=body)

        return message
