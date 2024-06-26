# Author: LAAMIRI Ouail
# Contact: laamiriouail@gmail.com


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re

def message_from_file(EntrepriseContactName: str, EntrepriseName: str, EntrepriseSecteurActivite: str, MyEmail: str,
                      MyPhone: str, MyName: str, MyLinkedIn: str, file_path: str) -> str:
    """
    Generate an HTML message from a template file.

    Parameters:
    - EntrepriseContactName (str): The contact name of the enterprise.
    - EntrepriseName (str): The name of the enterprise.
    - EntrepriseSecteurActivite (str): The sector of activity of the enterprise.
    - MyEmail (str): The sender's email address.
    - MyPhone (str): The sender's phone number.
    - MyName (str): The sender's name.
    - MyLinkdIn (str): The sender's LinkedIn profile URL.
    - file_path (str): The path to the HTML template file.

    Returns:
    - str: The generated HTML message.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        html_template = file.read()

    html_message = html_template.format(
        EntrepriseContactName=EntrepriseContactName,
        EntrepriseName=EntrepriseName,
        EntrepriseSecteurActivite="DEVELOPMENT INFORMATIQUE" if EntrepriseSecteurActivite is None else EntrepriseSecteurActivite,
        MyEmail=MyEmail,
        MyPhone=MyPhone,
        MyName=MyName,
        MyLinkedIn=MyLinkedIn
    )

    return html_message


def send_email_smtp(sender_email: str, sender_password: str, to: str, email_subject: str, email_body: str,
                    attachment_path: str = None, attachment_name: str = None) -> bool:
    """
    Send an email using SMTP.

    Parameters:
    - sender_email (str): The sender's email address.
    - sender_password (str): The sender's email password.
    - to (str): The recipient's email address.
    - email_subject (str): The subject of the email.
    - email_body (str): The body of the email in HTML format.
    - attachment_path (str, optional): Path to the attachment file.
    - attachment_name (str, optional): Name of the attachment file.

    Returns:
    - bool: True if the email is sent successfully, False otherwise.
    """
    is_sent = False
    try:
        # Set up the SMTP server
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(sender_email, sender_password)

        # Compose the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to
        msg['Subject'] = email_subject

        msg.attach(MIMEText(email_body, 'html'))

        if attachment_path:
            if not attachment_name:
                attachment_name = attachment_path.split("/")[-1]
            attachment = open(attachment_path, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % attachment_name)
            msg.attach(part)

        # Send the email
        smtp_server.sendmail(sender_email, to, msg.as_string())
        smtp_server.quit()
        is_sent = True
    except Exception as e:
        print(f"Error sending email: {e}")
        is_sent = False
    finally:
        return is_sent




def message_from_html(MyEmail: str, MyPhone: str, MyName: str, MyLinkedIn: str, file_path: str) -> str:
    """
    Generate an HTML message from a template file.

    Parameters:
    - MyEmail (str): The sender's email address.
    - MyPhone (str): The sender's phone number.
    - MyName (str): The sender's name.
    - MyLinkedIn (str): The sender's LinkedIn profile URL.
    - file_path (str): The path to the HTML template file.

    Returns:
    - str: The generated HTML message.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        html_template = file.read()

    html_message = html_template.format(
        MyEmail=MyEmail,
        MyPhone=MyPhone,
        MyName=MyName,
        MyLinkedIn=MyLinkedIn
    )
    return html_message


def check_gmail_connection(email: str, password: str) -> bool:
    """
    Check the connection to a Gmail account using the provided email and password.

    Parameters:
    - email (str): The Gmail account's email address.
    - password (str): The password for the Gmail account.

    Returns:
    - bool: True if the connection is successful, False otherwise.
    """
    try:
        # Set up the SMTP server
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(email, password)
        smtp_server.quit()
        return True
    except:
        return False











