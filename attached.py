# -*- coding: utf-8 -*
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from hardware import Hardware
from email.mime.text import MIMEText
import pickle
from collections import deque
from logging.handlers import SMTPHandler
from logging import getLogger

search_key = [
    "ASUS",
    "itx",
    "Z390-I",
    "z390-I",
    "Z390-i",
    "ITX",
]
rollback = 4
proxy = False

subject = "Hardware List"
body = "This is an email with attachment sent from Python"
sender_email = "diaper151@gmail.com"
receiver_email = "diaper151@gmail.com"
password = "yourpassword"

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email

err_log = getLogger()
handler = SMTPHandler(("smtp.gmail.com", 465),
                      'diaper151@gmail.com',
                      ['diaper151@gmail.com'],
                      "Logging from PTT scraper",
                      credentials=('diaper151@gmail.com', 'morris050'),
                      )
err_log.addHandler(handler)


if __name__ == "__main__":
    s = Hardware()
    get = s.get_data(get_first=True, proxy=proxy)
    result = s.data_processing(
        get,
        rollback=rollback,
        proxy=proxy,
        words=search_key)

    try:
        # avoid duplicated notification
        with open('hardware.pickle', 'rb') as handle:
            previous = pickle.load(handle)
        consume = deque(maxlen=0).extend
        consume(result.pop(key, None) for key in previous)

    except IOError as e:
        print("Initial search record with dumping pickle...")
        with open('hardware.pickle', 'wb') as handle:
            pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)
        err_log.warning(f"Script failed: \n{e}", exc_info=True)

    if len(result) == 0:
        print("Empty Result")
        exit()
    else:
        text = u''.join('{} : {}\n'.format(key, val)
                        for key, val in result.items())
        message.attach(MIMEText(text, 'plain', 'utf-8'))
        print(text)
        context = ssl.create_default_context()
        # 587 = TLS ; 465 = SSL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        # Save new record
        with open('hardware.pickle', 'wb') as handle:
            pickle.dump(result.update(previous), handle,
                        protocol=pickle.HIGHEST_PROTOCOL)
