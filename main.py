from flask import Flask, render_template, request, redirect, session
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.secret_key = "gsavdVsagdvdfgj"

@app.route("/")
def main():
    return redirect("login")


@app.route("/login", methods=["GET", "POST"])
def login():
    name = request.form.get("username")
    roll = request.form.get("roll")
    password = request.form.get("password")

    try:
        name.title()

        # Checking user in database 
        data_file = Path(__file__).resolve().parent / "Data.txt"

        with open(data_file, "r") as file:
            data = file.read().split("\n")[1:-1]
        for i in range(len(data)):
            if f"{name.title()} {roll} {password}" == data[i]:
                session["username"] = name.title()
                return redirect("home")
    except Exception as e:
        print("LOGIN ERROR:", e)
    return render_template("login.html")


@app.route("/home", methods=["GET", "POST"])
def home():
    message = request.form.get("message")
    name = session.get("username")
    timestamp = str(datetime.now()).split()
    print(timestamp)
    print(message)
    if message != None:
        with open("chat.csv", "a") as file:
            ts = str(timestamp).replace(",","")
            print(ts)
            chats = file.write(f"{name},{message},{ts}\n")
    with open("chat.csv", "r") as file:
        chats = file.read().splitlines()
    for i in range(len(chats)):
        chats[i] = chats[i].split(",")
    print(chats)
    
    chats.sort(key=get_time)
    print(chats)
    return render_template("main.html", lenght=range(len(chats)), chats=chats, name=name)

@app.route("/get_messages")
def get_messages():
    with open("chat.csv", "r") as file:
        chats = file.read().splitlines()

    for i in range(len(chats)):
        chats[i] = chats[i].split(",")

    chats.sort(key=get_time)

    return {"chats": chats}

def get_time(msg):
    return datetime.strptime(
        msg[2], "['%Y-%m-%d' '%H:%M:%S.%f']"
    )

if __name__ == "__main__":
    app.run(debug=True, port=8080)