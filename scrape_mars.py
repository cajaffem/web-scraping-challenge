from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)
    

def scrape():
    browser = init_browser()
    
    # mars hemisphere images
    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemispheres)
    time.sleep(2)
    browser.links.find_by_partial_text("Cerberus Hemisphere Enhanced").click()
    html_cerb = browser.html
    soup_cerb = bs(html_cerb, "html.parser")
    browser.back()
    browser.links.find_by_partial_text("Schiaparelli Hemisphere Enhanced").click()
    html_schia = browser.html
    soup_schia = bs(html_schia, "html.parser")
    browser.back()
    browser.links.find_by_partial_text("Syrtis Major Hemisphere Enhanced").click()
    html_syrt = browser.html
    soup_syrt = bs(html_syrt, "html.parser")
    browser.back()
    browser.links.find_by_partial_text("Valles Marineris Hemisphere Enhanced").click()
    html_vall = browser.html
    soup_vall = bs(html_vall, "html.parser")
    browser.quit()


    url_image_cerb = soup_cerb.find("a", text="Sample")["href"]
    url_image_schia = soup_schia.find("a", text="Sample")["href"]
    url_image_syrt = soup_syrt.find("a", text="Sample")["href"]
    url_image_vall = soup_vall.find("a", text="Sample")["href"]

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": url_image_vall},
        {"title": "Cerberus Hemisphere", "img_url": url_image_cerb},
        {"title": "Schiaparelli Hemisphere", "img_url": url_image_schia},
        {"title": "Syrtis Major Hemisphere", "img_url": url_image_syrt},
    ]

    # latest title and paragraph
    url_NASA_mars = "https://mars.nasa.gov/#"
    response = requests.get(url_NASA_mars, headers={'Cache-Control': 'no-cache'})
    soup = bs(response.text, features="lxml")

    news_latest_title = soup.body.find("h1", class_="media_feature_title").text
    news_title_stripped = news_latest_title.strip()
    news_latest_para = soup.body.find("div", class_="description").text
    news_para_stripped = news_latest_para.strip("\nMORE")

    # featured image jpg
    # make browser a newly named variable
    browser2 = init_browser()

    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser2.visit(url_image)
    browser2.find_by_id("full_image").first.click()
    time.sleep(2)
    html = browser2.html
    soup = bs(html, "html.parser")
    browser2.quit()

    image_div = soup.find('div', id="fancybox-lock")
    image_anchor = image_div.find("a", class_="button")
    image_href = image_anchor["href"]

    image_id = image_href.strip("/spaceimages/details.php?id=")
    image_id_final = image_id.strip()

    url_image_fullsize = f"https://www.jpl.nasa.gov/spaceimages/images/largesize/{image_id_final}_hires.jpg"
    
    # mars weather
    url_twitter_mars = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url_twitter_mars)
    soup = bs(response.text, features="lxml")

    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_weather_split = mars_weather.partition("hPapic")
    mars_weather_final = mars_weather_split[0]

    # mars facts table
    url_table = "https://space-facts.com/mars/"
    table = pd.read_html(url_table)
    df = table[0]
    html_table = df.to_html()
    html_table_final = html_table.replace('\n', '')
    html_table_final

    all_scrapes_dict = {"news_title": news_title_stripped,
        "news_para": news_para_stripped,
        "featured_image": url_image_fullsize,
        "mars_weather": mars_weather_final,
        "mars_facts": html_table_final,
        "hemisphere_urls": hemisphere_image_urls
    }
    return all_scrapes_dict