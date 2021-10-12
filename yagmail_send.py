import yagmail
import json

with open('secret.json') as f:
    text = json.load(f)
    dict = json.loads(text)

username = dict['user']
password = dict['password']

def yagsend(sender_name,sender_email,body):

    yag = yagmail.SMTP(username, password)
    yag.send(
        to=sender_email,
        subject= 'NSE Response',
        contents=sender_name + ' - ' + body,
    )
def yagsend_nse(sender_email, subject, body, attachment):

    yag = yagmail.SMTP(username, password)
    yag.send(
        to=sender_email,
        subject= subject,
        contents= "Good Evening" + ' - ' + body,
        attachments=attachment
    )
