# -*- coding: utf-8 -*
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from hardware import Hardware
from config import search_key, proxy
from email.mime.text import MIMEText
import pickle
from collections import deque

subject = "Hardware List"
body = "This is an email with attachment sent from Python"
sender_email = "diaper151@gmail.com"
receiver_email = "diaper151@gmail.com"
password = "your_password"

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email


if __name__ == "__main__":
    s = Hardware()
    origin = s.get_data(
        url="https://www.ptt.cc/bbs/HardwareSale/index.html",
        proxy=proxy)
    index = Hardware.get_index(origin)
    print(f"index: {index}")
    result = s.data_processing(index=index, proxy=proxy, words=search_key)

    # avoid duplicated notification
    try:
        with open('hardware.pkl', 'rb') as handle:
            previous = pickle.load(handle)
        print(f"previous:{previous}")
        consume = deque(maxlen=0).extend
        consume(result.pop(key, None) for key in previous)
    except (TypeError, EOFError):
        print("there's no previous record.")
        previous = {}

    except IOError as e:
        print("Initial search record with dumping pickle...")
        with open('hardware.pkl', 'wb') as handle:
            pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

    if len(result) == 0:
        print("Empty Result")
        exit()
    else:
        text = u''.join('{} : {}\n'.format(key, val)
                        for key, val in result.items())
        message.attach(MIMEText(text, 'plain', 'utf-8'))
        print(text)
        # Send G-mail
        if proxy:
            with open('hardware.pkl', 'wb') as handle:
                result.update(previous)
                pickle.dump(result, handle,
                            protocol=pickle.HIGHEST_PROTOCOL)
            exit()
        else:
            context = ssl.create_default_context()
            # 587 = TLS ; 465 = SSL
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email,
                    receiver_email,
                    message.as_string())
            # Save new record TODO: prevent mail fail?
            with open('hardware.pkl', 'wb') as handle:
                result.update(previous)
                pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)
