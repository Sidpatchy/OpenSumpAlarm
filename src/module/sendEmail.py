# Email sender for OpenSumpAlarm by Sidpatchy
# A project to detect sump pump failure or inadequacy
# More info on GitHub: https://github.com/Sidpatchy/OpenSumpAlarm

# Import libraries
import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

# sendEmail() sends an email
# Usage:
#   apikey: string, sendgrid apikey
#   from_email: string, email to send the email from
#   to_email: string, address to send email to
#   subject: string, subject of email
#   content: string, content of email
def sendEmail(apikey, from_email, to_email, subject, content):
    from_email = Email(str(from_email))
    to_email = To(str(to_email))
    subject = str(subject)
    content = Content("text/plain", (str(content)))

    mail = Mail(from_email=from_email, to_emails=to_email, subject=subject, plain_text_content=content)

    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get(str(apikey)))
        response = sg.send(mail)
        return response
    except Exception as e:
        print(e)
        return e