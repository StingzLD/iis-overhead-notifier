import requests
import smtplib
import time
from datetime import datetime


def get_sun_data(latitude, longitude):
    parameters = {
        "lat": latitude,
        "lng": longitude,
        "formatted": 0
    }
    sun_response = requests.get(url="https://api.sunrise-sunset.org/json",
                                params=parameters)
    sun_response.raise_for_status()
    sun_data = sun_response.json()["results"]
    return sun_data["sunrise"], sun_data["sunset"]


def is_dark(latitude, longitude):
    current_hour = datetime.utcnow().hour
    sunrise, sunset = get_sun_data(latitude=latitude, longitude=longitude)
    sunrise_hour = int(sunrise.split("T")[1].split("+")[0].split(":")[0])
    sunset_hour = int(sunset.split("T")[1].split("+")[0].split(":")[0])

    if sunset_hour >= 0:
        if sunrise_hour >= current_hour >= sunset_hour:
            return True
    elif current_hour <= sunrise_hour or current_hour >= sunset_hour:
        return True


def iss_is_overhead(my_latitude, my_longitude):
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()["iss_position"]
    iss_latitude = float(iss_data["latitude"])
    iss_longitude = float(iss_data["longitude"])

    if my_latitude - 5 <= iss_latitude <= my_latitude + 5 and \
       my_longitude - 5 <= iss_longitude <= my_longitude + 5:
        return True


def send_email(email):
    email_sender = "stingzld.test.email@gmail.com"
    password = "aaeddmspdtbyixxw"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=email_sender, password=password)
        connection.sendmail(from_addr=email_sender,
                            to_addrs=email,
                            msg="Subject:ISS is Overhead!!!\n\n"
                                "LOOK UP!\n"
                                "The ISS is overhead RIGHT NOW!!!")


# -------------------------------- MAIN CODE --------------------------------- #
MY_COORDINATES = (42.359837288868796, -71.09420291711368)

while True:
    if iss_is_overhead(MY_COORDINATES[0], MY_COORDINATES[1]) and \
       is_dark(MY_COORDINATES[0], MY_COORDINATES[1]):
        send_email("stingzld.other.test.email@gmail.com")
    time.sleep(60)
