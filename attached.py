# -*- coding: utf-8 -*
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from hardware import Hardware, proxies
from email.mime.text import MIMEText
import socks
import time

search_key = ["itx", "Z390-I", "z390-I", "Z390-i", "ITX"]
rollback = 4
proxy = False

subject = "Hardware List"
body = "This is an email with attachment sent from Python"
sender_email = "diaper151@gmail.com"
receiver_email = "diaper151@gmail.com"
password = "morris050"

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  # Recommended for mass emails


if __name__ == "__main__":
    s = Hardware()
    get = s.get_data(get_first=True, proxy=proxy)
    result = s.data_processing(
        get,
        rollback=rollback,
        proxy=proxy,
        words=search_key)

    text = u''.join('{} : {}\n'.format(key, val) for key, val in result.items())
    message.attach(MIMEText(text, 'plain', 'utf-8'))
    print(text)
    # socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, "proxy-chain.intel.com", 912)
    # socks.wrapmodule(smtplib)
    # socks.wrapmodule(ssl)
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    # 587 is tls and 465 is ssl 
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
