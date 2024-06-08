from twilio.rest import Client
from django.conf import settings


def send_sms(phn, data):
    sid = settings.SID
    auth = settings.AUTH
    phone = settings.PHONE
    client = Client(sid, auth)
    result = "Response received\n"
    for question in data["questions"]:
        answers = ", ".join(question["answers"])
        row = f"{question['question']}: {answers}\n"
        result += row

    print(result)
    try:
        client.messages.create(body=result, from_=phone, to=phn)
    except Exception as e:
        print(f"An error occurred while sending the SMS: {str(e)}")
