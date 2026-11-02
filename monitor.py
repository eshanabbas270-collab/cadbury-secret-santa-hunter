
import os
import re
import smtplib
import hashlib
from email.message import EmailMessage
from urllib.request import Request, urlopen

URL = "https://secretsanta.cadbury.co.uk/missed-out"

EMAIL_TO = os.environ["EMAIL_TO"]
EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

def send_alert(subject, body):
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = EMAIL_FROM
    message["To"] = EMAIL_TO
    message.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
        smtp.send_message(message)

request = Request(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

try:
    with urlopen(request, timeout=20) as response:
        page = response.read().decode("utf-8", errors="ignore")

    text = re.sub(r"<[^>]+>", " ", page).lower()
    blocked = any(word in text for word in [
        "access denied",
        "too many requests",
        "captcha"
    ])

    if blocked:
        print("Cadbury may be limiting access. Stopping.")
        raise SystemExit

    if "missed-out" not in URL:
        send_alert(
            "Cadbury Hunter: Page changed",
            "The Cadbury page has changed. Check it manually."
        )

    print("Cadbury page checked successfully.")
    print("No confirmed claim opportunity detected.")

except Exception as error:
    print("Monitoring error:", error)
