# 1. import Flask
from flask import Flask

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Hello World")
    return "Hello"


# 4. Define what to do when a user hits the /about route
@app.route("/pg2")
def pg2():
    print("other page")
    return "other page"


if __name__ == "__main__":
    app.run(debug=True)