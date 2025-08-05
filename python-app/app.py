from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    env_var = os.getenv('MY_ENV_VAR', 'Not Set')
    return f'MY_ENV_VAR is: {env_var}', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)