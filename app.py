from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    env = os.getenv("APP_ENV", "Development")
    return f"Hello from {env} Environment!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
