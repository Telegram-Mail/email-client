# import os
import email
import imaplib
from tools.errors import LoginException
from tools.read_config import read_config
# import base64

# Very important Use "ISO-8859-1" as encoding method to avoid errors decoding the emais

def recieve_mail(email_user:str, email_pwd:str, get_all: bool=False):
    # Read the email config file
    config = read_config('./config/config_email.json')
    # create conection with the imap server
    mail = imaplib.IMAP4_SSL(host=config['imap_host'], port=config['imap_port'])      
    # login with the username and password
    try:
        mail.login(email_user, email_pwd)                                               
    except:
        raise LoginException
    else:
        # TODO allow to select other folders 
        # select all the inbox folder 
        mail.select(readonly=True)                                                            

        # select all mails in the inbox or the onread ones only
        if not get_all:
            type, data = mail.search(None, 'UNSEEN')                                           
        else:    
            type, data = mail.search(None, 'ALL')                                           
    
        # get the list with the email ids
        mail_ids = data[0]                                                              
        id_list = mail_ids.split()                                                  
        msg_list = []

        # loop throw the emails
        for num in id_list:                                                             
            # get the mail and decode it
            typ, data = mail.fetch(num, '(RFC822)')                                             
            # TODO get the unread mails separately
            # loop throw the parts of the message          
            for response_part in data:                                                  
                if isinstance(response_part, tuple):                                    
                    # get the message data and decode it
                    msg = email.message_from_string(response_part[1].decode("ISO-8859-1"))   
                    # extract email subject
                    email_subject = msg['subject']                                      
                    # extract email sender
                    email_from = msg['from']                                            

                    # typ, data = mail.store(num,'-FLAGS', '\\Seen')
                    # output extracted Data to the console
                    print('From: ' + email_from + '\n')                                 
                    print('Subject: ' + email_subject + '\n')
                    print(msg.get_payload(decode=True))
                
                    # append the mail to a list with all the emails
                    msg_list.append((email_subject, email_from, msg.get_payload(decode=True))) 
                    # TODO for debug reasons we are only sending back one email, remove before deploy
                    return msg_list
                
    return msg_list
# to download attachments
# raw_email = data[0][1]
# raw_email_string = raw_email.decode("ISO-8859-1")
#
# email_message = ''                                                      #
# email_message = email.message_from_string(raw_email_string) 
# 
# for part in email_message.walk():
#     if part.get_content_maintype() = 'multipart':
#         continue
#     if part.get('Content-Disposition') is None:
#         continue
#     filename = part.get_filename()
#     if bool(filename):
#         filepath = os.join('./downloads', filename)
#         if not os.path.isfile(filepath)
#         fp = open(filepath, 'wb')
#         fp.write(part.get_payload(decode=True))
#         fp.close()
#         subject = str(email_message).split('Subject', 1)[1].split('\nTo', 1)[0]
#         print('Downloaded "{file}" from email titled "{subject}" with uid \
#         "{uid}".'.format(file=filename, subject=subject, uid=latest_email_uid.decode('utf-8')))
