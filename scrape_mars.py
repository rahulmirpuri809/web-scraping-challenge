#!/usr/bin/env python
# coding: utf-8


# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser as browser
import pandas as pd


def init_browser():
    # Set Executable Path with Chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return browser('chrome', **executable_path, headless=False)

def web_scrape():

    browser = init_browser()

    # Visit the NASA Mars News Site
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)


    # HTML Parser
    html1 = browser.html
    news_soup = BeautifulSoup(html1, "html.parser")
    slide_element = news_soup.select_one("ul.item_list li.slide")


    # Find the first paragraph with newss
    news_title = slide_element.find("div",class_="content_title").text.strip()
    news_paragraph = slide_element.find("div",class_="article_teaser_body").text.strip()
   

    # Visit the jpl url
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # Click Full Image
    browser.click_link_by_partial_text('FULL IMAGE')


    # Click More Info Element
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()


    # HTML Parser 
    html2 = browser.html
    image_soup = BeautifulSoup(html2, 'html.parser')


    # Get Image URL
    feat_img_url = image_soup.find('figure', class_='lede').a['href']
    feat_img_full_url = f'https://www.jpl.nasa.gov{feat_img_url}'




    # Visit Mars Twitter Page
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)



    #HTML Parser 
    html3 = browser.html
    tweet_soup = BeautifulSoup(html3, 'html.parser')


    # Get Mars Weather
    mars_weather = tweet_soup.find('p', class_='TweetTextSize').text.strip().replace("\n"," ").split("pic.twitter")
    mars_weather = mars_weather[0]


    dictionary1= {"news_title": news_title,
                "news_paragraph": news_paragraph,
                "featured_image_url": feat_img_full_url,
                "mars_weather": mars_weather}



    # Get DataFrame of Facts 
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = ['Property', 'Value']
    df = df.set_index('Property')
    

    # Convert DataFrame to HTML
    df.to_html()
    dictionary2 = df.to_dict()["Value"]



    # Mars Hemispheres URL
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)



    # HTML Parser
    html4 = browser.html
    hemi_soup = BeautifulSoup(html4, 'html.parser')



    # Get Strings of Title Names by finding H3 Elemement
    hemi_strings = []
    links = hemi_soup.find_all('h3')

    for hemi in links:
        hemi_strings.append(hemi.text)
        



    # Blank List to Insert Hemisphere URLs
    hemisphere_image_urls = []

    # Use String Element to obtain Image URLs
    for hemi in hemi_strings:
        # Dictionary for the hemispheres
        hemi_dict = {}
        
        # Click on the link with the hemisphere strings
        browser.click_link_by_partial_text(hemi)
        
        # Scrape the image url string and store into the dictionary
        hemi_dict["img_url"] = browser.find_by_text('Sample')['href']
        
        # Store Hemisphere Title in Dict
        hemi_dict["title"] = hemi
        
        # Add the dictionary to hemisphere_image_urls kust
        hemisphere_image_urls.append(hemi_dict)
        

        
        # Click the 'Back' button
        browser.back()



    dictionary3= {"image_titles":[hemisphere_image_urls[0]["title"],hemisphere_image_urls[1]["title"],
                                hemisphere_image_urls[2]["title"],hemisphere_image_urls[3]["title"]],
                "image_urls":[hemisphere_image_urls[0]["img_url"],hemisphere_image_urls[1]["img_url"],
                                hemisphere_image_urls[2]["img_url"],hemisphere_image_urls[3]["img_url"]]}
  





    total_data = {**dictionary1,**dictionary2, **dictionary3}
    
    browser.quit()

    return total_data





