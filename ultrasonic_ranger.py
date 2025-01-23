import time
import requests
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os

THINGSPEAK_URL = "https://api.thingspeak.com/update"
API_KEY = "ZR2R4O910OA8SA61"

D5 = 5  
sensor = GroveUltrasonicRanger(D5)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "fifaboy963@gmail.com"
EMAIL_PASSWORD = "kmld ymme ammk tvvj"
RECIPIENT_EMAIL = "fifaboy963@gmail.com"

def send_email(distance, timestamp):
    subject = "New Mail Delivered!"
    body = (
        f"Hello!\n\n"
        f"Your Smart Letterbox has detected new mail.\n\n"
        f"Distance: {distance:.2f} cm\n"
        f"Time: {timestamp}\n\n"
        f"Best regards,\n"
        f"Smart Letterbox System"
    )
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_to_thingspeak(distance, timestamp, change_flag):
    params = {
        "api_key": API_KEY,
        "field1": distance,
        "field2": timestamp,
        "field3": change_flag
    }
    try:
        response = requests.get(THINGSPEAK_URL, params=params)
        print("ThingSpeak response:", response.text)
    except Exception as e:
        print(f"Failed to send data to ThingSpeak: {e}")
def main():
    print("Measuring Distance and sending to ThingSpeak if change > 2cm...")
    last_distance = sensor.get_distance()
    print(f"Initial Distance: {last_distance:.2f} cm")
    alert_sent = False

    while True:
        distance = sensor.get_distance()
        print(f"Distance: {distance:.2f} cm")

        if abs(distance - last_distance) > 2.0 and not alert_sent:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            send_to_thingspeak(distance, timestamp, 1)
            send_email(distance, timestamp)
            last_distance = distance
            alert_sent = True
            print("Significant change detected! Alert sent.")
        elif abs(distance - last_distance) <= 2.0 and alert_sent:
            alert_sent = False
            print("Distance back to normal. Ready to send next alert.")
        time.sleep(15)

if __name__ == "__main__":
    main()

