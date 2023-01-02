import uuid
from datetime import datetime
from twilio.rest import Client
from msgConfig import account_sid, auth_token

def generate_uuid() -> str:
    return str(uuid.uuid4())

def format_date_time(date_time) -> str:
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    date_time = date_time.split("T")
    date = date_time[0]
    time = date_time[1].split(".")[0]
    date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
    date = date.split("-")
    date[1] = months[int(date[1]) - 1]
    date = "-".join(date)
    time = datetime.strptime(time, "%H:%M:%S").strftime("%I:%M %p")
    return date + " " + time

def customStyle() -> str:
    return """
        QWidget{
            background-image: url(../resources/bg.png);
        }
        QLabel{
            font-family: Poppins;
            font-size: 30px;
            font-weight: 600;
            color: #fff;
        }
        QPushButton{
            background: #00FFE6;
            border: 1px solid #000;
            color: #000;
            font-size: 18px;
            font-weight: bold;
            border-radius: 17px;
            outline: none;
        }
        QPushButton:hover{
            background: #000;
            color: #00FFE6;
        }
        QLineEdit {
            padding: 5px 10px;
            font-size: 18px;
            border: 3px solid #000;
            background: #fff;
            font-family: Poppins;
            border-radius: 25px;
        }
        QMessageBox{
            background: #fff;
            font-family: Poppins;
        }
        QMessageBox QLabel{
            color: #000;
            background: #fff;
            font-size: 18px;
            font-weight: normal;
        }
        QMessageBox QPushButton{
            background: rgba(0, 0, 0, 0);
            padding: 5px;
            border: none;
            outline: none;
        }
        QListView{
            background: rgba(255, 255, 255, 0.5);
            border: 3px solid #000;
            border-radius: 25px;
        }
    """

def convert_to_international_format(number) -> str:
    if number[0] == "0":
        number = number[1:]
    return "+92" + number

def send_message_to_guardian(number, message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=convert_to_international_format(number),
        from_="+18655099495",
        body=message
    )