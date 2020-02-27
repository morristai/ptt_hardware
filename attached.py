import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from hardware import Hardware
from email.mime.text import MIMEText

search_key = ["itx", "Z390-I", "z390-I", "Z390-i", "ITX"]
rollback = 4
proxy = False
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
    "sec-fetch-user": "?1",
    "dnt": "1",
    "accept-encoding": "gzip, deflate",  # 不能放br，不然就是要裝額外的解碼器
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "cookie": "__cfduid=d5bf85bc78cd75c30beabfc2c14e52e5f1567955601; _ga=GA1.2.410818996.1567955602; _gid=GA1.2.1223439128.1582700194; _gat=1",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "upgrade-insecure-requests": "1",
}

subject = "Hardware List"
body = "This is an email with attachment sent from Python"
sender_email = "diaper151@gmail.com"
receiver_email = "diaper151@gmail.com"
password = "Your password"

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

    text = u''.join('{} : {}'.format(key, val) for key, val in result.items())
    message.attach(MIMEText(text, 'plain', 'utf-8'))
    print(text)
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
