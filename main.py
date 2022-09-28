import requests
from bs4 import BeautifulSoup
import json
from email.message import EmailMessage
import ssl
import smtplib
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen
url = 'https://www.pushsafer.com/api'
data_html = []
y = []
are_in = []
loginurl = "login to school site"
secure_url = "school site this week"
secure_url_1 = "school site next week"
payloud = {
        "username": "name",
        "password": "password"
}
def main():
    with requests.session() as s:
        s.post(loginurl,data=payloud)
        r = s.get(secure_url)
        r_1 = s.get(secure_url_1)
        soup = BeautifulSoup(r.content, "html.parser")
        soup_1 = BeautifulSoup(r_1.content, "html.parser")
    for i in soup.find_all(class_=["day-item-hover tooltip-bubble pink",
                                   "day-item day-item-hover tooltip-bubble pink"]):
        data_html.append(i)
    for i in soup_1.find_all(class_=["day-item-hover tooltip-bubble pink",
                                     "day-item day-item-hover tooltip-bubble pink"]):
        data_html.append(i)
    check(data_html)

def check(data_html):
    for i in data_html:
        z = json.loads(i.attrs["data-detail"])
        z["theme"] = ""
        z["notice"] = ""
        if z not in are_in:
            ucitel = z.get("teacher")
            print("----------ZMĚNA----------")
            if ucitel == None:
                message = z.get("removedinfo") + " " + z.get("subjecttext")
                print(message)
                send_noti(message)
            else:
                message = ucitel + " " + z.get("subjecttext")
                print(message)
                send_noti(message)
            are_in.append(z)

def send_email(sent_email):
    email_sender = ""
    email_password = ""
    email_receiver = [""]
    for i in email_receiver:
        email_receiver = i
        subject = "ROZVRH"
        body = sent_email
        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_receiver
        em["Subject"] = subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver, em.as_string())

def send_noti(z):
    post_fields = {
        "t": 'ZMENA',
        "m": z,
        "v": 3,
        "i": 33,
        "c": '#FF0000',
        "d": 'a',
        "k": 'token'
    }
    request = Request(url, urlencode(post_fields).encode())
    json = urlopen(request).read().decode()

while True:
    main()
    time.sleep(100)
