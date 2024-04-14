import logging
import smtplib 
from dotenv import load_dotenv

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

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

    def send(self, subject: str, to_email: str, htmlbody: str, pdf_file_path = None) -> bool:
        """
        Send an email with the given subject, HTML body, and attached PDF file to the specified email address.

        Args:
            subject (str): The subject of the email.
            to_email (str): The recipient's email address.
            htmlbody (str): The HTML body of the email.
            pdf_file_path (str): The file path of the PDF file to be attached.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        if(pdf_file_path):
            msg = MIMEMultipart()
        else:
            msg = MIMEText(htmlbody, 'html')
        msg['Subject'] = subject
        msg['From'] = self.from_email
        msg['To'] = to_email


        if(pdf_file_path):
            msg.attach(MIMEText(htmlbody, 'html'))
            with open(pdf_file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {pdf_file_path}')
                msg.attach(part)
        
        # Send email
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.sendmail(self.from_email, to_email, msg.as_string())
        server.quit()
        return True

