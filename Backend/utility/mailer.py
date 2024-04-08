from dotenv import load_dotenv
import smtplib 

from email.mime.text import MIMEText
import logging

class Mail():
    def __init__(self, app: dict) -> None:
        """
        Initialize the email settings.

        Args:
        app (dict): The dictionary containing the email configuration settings.
        """
        self.from_email = app.config['EMAIL']        
        self.password = app.config['EMAIL_PASSWORD']        
        self.smtp_server = app.config['SMTP_SERVER']
        self.smtp_port = app.config['SMTP_PORT']

    def send(self, subject: str, to_email: str, htmlbody: str) -> bool:
        """
        Send an email with the given subject and HTML body to the specified email address.

        Args:
            subject (str): The subject of the email.
            to_email (str): The recipient's email address.
            htmlbody (str): The HTML body of the email.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """

        # TODO: Remove

        print("\n============================================================\n")
        print("Email Metadata : " ,self.from_email , subject, to_email)

        try:
            msg = MIMEText(htmlbody, 'html')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            # server.debuglevel = 1
            # server.starttls()
            # server.login(self.from_email, self.password)
            server.sendmail("Admin", to_email, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            logging.error(e)
            return False


