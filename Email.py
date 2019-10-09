import os
import smtplib
from em.ol.olProps import olProps_var
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def bscEM(b,t,s):
    msg = MIMEMultipart()
    msg['To'] = t
    msg['From'] = "<your email>"
    msg['Subject'] = s
    body = MIMEText(b,'html','utf-8')
    msg.attach(body)  # add message body (text or html)
    olp = olProps_var()
    ol_US = ol.US
    ol_PS = ol.PS
    s = smtpserver = smtplib.SMTP("smtp-mail.outlook.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(ol_US, ol_PS)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    print('done!')
    s.close()

def emPL(recp,sub,emHTML):
    msg = MIMEMultipart()
    recipients = recp
    sender = "<your email>"
    msg['To'] = ", ".join(recipients)
    msg['From'] = sender
    msg['Subject'] = sub
    body = MIMEText(emHTML, 'html', 'utf-8')
    msg.attach(body)
    olp = olProps_var()
    ol_US = ol.US
    ol_PS = ol.PS
    s = smtpserver = smtplib.SMTP("smtp-mail.outlook.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(ol_US, ol_PS)
    s.sendmail(sender, recipients, msg.as_string())
    print('done!')
    s.close()

def sendMultiAttEm(dir,files,title,recp,sub):
    print('Started: ' + title)
    dir_path = dir
    files = files

    msg = MIMEMultipart()
    recipients = recp
    sender = "<your email>"
    msg['To'] = ", ".join(recipients)
    msg['From'] = sender
    msg['Subject'] = sub


    body = MIMEText("""<html><body><p1>test</p1></body></html>""", 'html', 'utf-8')
    msg.attach(body)  # add message body (text or html)

    for f in files:  # add files to the message
        file_path = os.path.join(dir_path, f)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition','attachment', filename=f)
        msg.attach(attachment)
    olp = olProps_var()
    ol_US = ol.US
    ol_PS = ol.PS
    s = smtpserver = smtplib.SMTP("smtp-mail.outlook.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(ol_US, ol_PS)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    print('Finished: ' + title)
    s.close()