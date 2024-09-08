import random
import requests


def send_simple_message(email):
    pin = generate_pin()  # Correctly call the function to generate the PIN
    response = requests.post(
        "https://api.mailgun.net/v3/sandbox3ceaa358036244608f598cba5865bf95.mailgun.org/messages",
        auth=("api", "f6e3c37753e8e6edbe1e8361cb6e4338-777a617d-59c24f7e"),
        data={
            "from": "verification@gmail.com",
            "to": [f"{email}"],
            "subject": "Your Verification Code",
            "text": f"Here is your verification code: {pin}",
        },  # Include the PIN in the email body
    )

    status_code = response.status_code
    response_text = response.text

    if status_code == 200:
        print(f"Email sent successfully! with pin: {pin}")
        return pin

    elif status_code == 401:
        print("401 Unauthorized: Check if your API key is correct and not expired.")
    elif status_code == 403:
        print(
            "403 Forbidden: Verify that the recipient email addresses are authorized for your sandbox domain."
        )
    else:
        print(f"Error {status_code}: {response_text}")


def generate_pin():
    return str(random.randint(1000, 9999))  # Generate a 4-digit PIN


send_simple_message()
