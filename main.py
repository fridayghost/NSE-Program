# this file was previously named as open_verify_mail.py

import easyimap
import add_remove_email
import yagmail_send
import time
import json

# This function checks if the email has a subject NSE or if the sender is drzibrankhan@gmail.com and executes the
# code accordingly
def nse_getmail():
    print('Checking email for instructions.......')
    
    with open('secret.json') as f:
        text = json.load(f)
        dict = json.loads(text)

    username = dict['user']
    password = dict['password']

    to_mail = 'zibranpython@gmail.com'
    subject = 'Hello there'
    host = 'imap.gmail.com'
    mailbox = 'Inbox'

    mail_list = add_remove_email.read_authorised_id()


    imapper = easyimap.connect(host, username, password, mailbox, ssl=True, port=993)

    email = imapper.unseen()

    for message in email:
        from_str = message.from_addr
        email_start_br = int(from_str.find('<')) + 1
        email_end_br = int(from_str.find('>'))
        sender_email = from_str[email_start_br:email_end_br]

        location_openbracket = from_str.find('<')
        sender_name = from_str[0:location_openbracket]


        if message.title.upper() == 'NSE MY STATUS':
            if sender_email in mail_list:
                yagmail_send.yagsend(sender_name, sender_email, 'You are in the mailing list')

            else:
                yagmail_send.yagsend(sender_name, sender_email, 'You are not in the mailing list')

        if sender_email == "admin email id":
            if message.title.upper() == 'NSE REMOVE':
                old_new_list = add_remove_email.remove_id(message.body.strip())
                drzibran_mail_body = f'Mail ID removed - {old_new_list[2]}\n\nOld list : {old_new_list[0]}, \n\nNew list :{old_new_list[1]}'
                yagmail_send.yagsend(sender_name, sender_email, drzibran_mail_body)
                # print('Removed : ', message.body)


            if message.title.upper() == 'NSE ADD':
                old_new_list = add_remove_email.add_id(message.body.strip())
                drzibran_mail_body = f'Mail ID Added - {old_new_list[2]}\n\nOld list : {old_new_list[0]}, \n\nNew list :{old_new_list[1]}'
                yagmail_send.yagsend(sender_name, sender_email, drzibran_mail_body)

            if message.title.upper() == 'NSE VIEW':
                old_new_list = add_remove_email.read_authorised_id()
                drzibran_mail_body = f'Current authorized IDs are : {old_new_list}'
                yagmail_send.yagsend(sender_name, sender_email, drzibran_mail_body)

nse_getmail()