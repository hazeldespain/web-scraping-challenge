#import dependencies 
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "./chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars = {}
    space_images={}
    mars_twitter={}
    mars_weather={}
    hemisphere_images={}

    url_1="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"    
    url_2="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    mars_twitter_url="https://twitter.com/marswxreport?lang=en"
    mars_weather_url="https://space-facts.com/mars/"
    #mars hemispheres
    c_url="https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    sh_url="https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    sy_url="https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    v_url="https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    browser.visit(url_1)
    browser.visit(url_2)
    browser.visit(mars_twitter_url)
    browser.visit(mars_weather_url)
    browser.visit(c_url)
    browser.visit(sh_url)
    browser.visit(sy_url)
    browser.visit(v_url)
    html = browser.html
    soup = bs(html, "html.parser")

    response = requests.get(url_1)
    soup = bs(response.text, 'lxml')
    mars["news_title"] = soup.title.text
    mars["news_p"] = soup.body.p.text

    response = requests.get(url_2)
    soup = bs(response.text, 'lxml')
    space_images["featured_image_url"]= "https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA17838-1920x1200.jpg"
    
    mars_response = requests.get(mars_twitter_url)
    soup = bs(mars_response.text, 'lxml')
    mars_twitter["mars_tweet"]=soup.find("p", class_="tweet-text").text.replace('\n', '')
#   creating table
    table = pd.read_html(mars_weather_url)
    df = table[0]
    df.columns = ["Mars - Earth Comparison", "Mars", "Earth"]
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')
    mars_weather["weather_table"]=html_table
#   images
#1
    cereberus_response = requests.get(c_url)
    soup_c=bs(cereberus_response.text, 'lxml')
    cereberus_img = soup_c.find("img", class_="wide-image")["src"]
    cereberus_title = soup_c.find("h2", class_="title").text
#2
    sh_response= requests.get(sh_url)
    soup_sh=bs(sh_response.text,'lxml')
    sh_img = soup_sh.find("img",class_="wide-image")["src"]
    sh_title = soup_sh.find("h2", class_="title").text
#3
    sy_response=requests.get(sy_url)
    soup_sy = bs(sy_response.text,'lxml')
    sy_img=soup_sy.find("img", class_="wide-image")["src"]
    sy_title = soup_sy.find("h2", class_="title").text
#4
    v_response=requests.get(v_url)
    soup_v=bs(v_response.text, 'lxml')
    v_img=soup_v.find("img",class_="wide-image")["src"]
    v_title=soup_v.find("h2", class_="title").text
#dictionary with images  
    hemisphere_image_urls = [
    {"title": cereberus_title, "img_url": "https://astrogeology.usgs.gov"+cereberus_img},
    {"title": sh_title, "img_url": "https://astrogeology.usgs.gov"+sh_img},
    {"title": sy_title, "img_url": "https://astrogeology.usgs.gov"+sy_img},
    {"title": v_title, "img_url": "https://astrogeology.usgs.gov"+v_img},]   
    
    hemisphere_images["hemisphere"]=hemisphere_images_urls
    return mars
    return space_images
    return mars_twitter
    return mars_weather
    return hemisphere_images


if __name__ == "__main__":
    mars = scrape()
    print(mars)

