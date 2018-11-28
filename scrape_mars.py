
# coding: utf-8

# In[59]:


from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests as req
import time

# function to initiate browser
def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

# function to scrape Mars data
def scrape():
    browser = init_browser()
    mars_dict = {}

# In[60]:

# NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    response = req.get(url)
    news_soup = bs(response.text, 'html.parser')

# In[61]:

    news_title = news_soup.find('div', class_='content_title').get_text()
    news_p = news_soup.find('div', class_='rollover_description_inner').get_text()

    mars_dict["data_title"] = news_title
    mars_dict["data_p"] = news_p

# In[62]:

# JPL Mars Space Images - Featured Image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

# In[63]:

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    browser.click_link_by_partial_text('.jpg')

# In[64]:

    html = browser.html
    jpl_soup = bs(html, 'html.parser')

    featured_img_url = jpl_soup.find('img').get('src')
    mars_dict["feat_image"] = featured_img_url

# In[65]:

# Mars Weather

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    response = req.get(twitter_url)
    weather_soup = bs(response.text, 'html.parser')
    mars_weather = weather_soup.find('p', class_='tweet-text').text
    mars_dict["weather"] = mars_weather

# In[66]:

# Mars Facts

    facts_url = 'https://space-facts.com/mars/'
    table_df = pd.read_html(facts_url)[0]
    table_df.columns = ['description', 'value']
    table_df = table_df.set_index('description', drop=True)
    mars_dict["table"] = table_df.to_html()

# In[67]:
# In[68]:

# Mars Hemispheres

    base_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(base_url)

    html = browser.html
    hem_soup = bs(html, 'html.parser')

# In[69]:

    hem_img_urls = []
    hem_dict = {'title': [], 'img_url': [],}

    x = hem_soup.find_all('h3')
# print(x)

    for i in x:
        t = i.get_text()
        title = t.strip('Enhanced')
        browser.click_link_by_partial_text(t)
        url = browser.find_link_by_partial_href('download')['href']
        hem_dict = {'title': title, 'img_url': url}
        hem_img_urls.append(hem_dict)
        browser.visit(base_url)

    mars_dict["hemispheres"] = hem_img_urls

    return mars_dict

