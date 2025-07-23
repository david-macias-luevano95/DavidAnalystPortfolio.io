from flask import (
    Blueprint,render_template, request, redirect, url_for, current_app
)
from email.message import EmailMessage
import os
import ssl
import smtplib

class Email:
    def __init__(self, email, name=None):
        self.email = email
        self.name = name

    def get(self):
        return {"email": self.email, "name": self.name}
    
class Content:
    def __init__(self, content_type, value):
        self.type = content_type
        self.value = value

    def get(self):
        return {"type": self.type, "value": self.value}

class To(Email):
    pass

class Mail:
    def __init__(self, from_email, to_emails, subject, content):
        self.from_email = from_email
        self.to_emails = to_emails if isinstance(to_emails, list) else [to_emails]
        self.subject = subject
        self.content = content

    def get(self):
        return {
            "from": self.from_email.get(),
            "to": [to.get() for to in self.to_emails],
            "subject": self.subject,
            "content": self.content.get()
        }


bp = Blueprint('portfolio', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return render_template('portfolio/index.html') 

@bp.route('/mail', methods=['POST'])
def mail():
    to = os.environ.get('TO_EMAIL')
    subject = request.form.get('email')
    content = request.form.get('message')
    

    if request.method == 'POST':
        send_mail(to, subject, content)
        return render_template('portfolio/sent_mail.html')

    return redirect(url_for('portfolio.index'))
    

def send_mail(to, subject, content):
    
    PASSWORD = os.environ.get('PASSWORD_GMAIL')   
    from_email = os.environ.get('FROM_EMAIL')
    to_email = os.environ.get('TO_EMAIL')

    content = Content('text/plain', content)
    mail=Mail(from_email, to_email, subject,content)

    from_email = mail.from_email
    to_email = to
    
    em = EmailMessage()
    em['From'] = from_email
    em['To'] =  to
    em['Subject']= subject
    em.set_content(content.value)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(from_email, PASSWORD, )
        smtp.sendmail(from_email, to_email, em.as_string())

    



    return