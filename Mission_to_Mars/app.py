from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_a

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"]="mongodb://localhost:27017/mars"
mongo = PyMongo(app)

# 3. Define what to do when a user hits the index route
@app.route("/")
def index():

    # Return template and data
    return render_template("index.html", mars=mars_data)


# 4. Define what to do when a user hits the /about route
@app.route("/scrape_mars_a")
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars_a.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)