from bs4 import BeautifulSoup
from facebook_scraper import get_posts
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from decouple import config
import pandas as pd
import time
import pymongo
import sys, os

if getattr(sys, 'frozen', False):
    # if you are running in a |PyInstaller| bundle
    extDataDir = sys._MEIPASS
    extDataDir  = os.path.join(extDataDir, '.env') 
    #you should use extDataDir as the path to your file Store_Codes.csv file
else:
    # we are running in a normal Python environment
    extDataDir = os.getcwd()
    extDataDir = os.path.join(extDataDir, '.env') 
    #you should use extDataDir as the path to your file Store_Codes.csv file


url = config('URL')
client = pymongo.MongoClient(url)
db = client.crawl

fb_post = []

for post in get_posts('dochoichu', pages=int(config('POST'))):
    fb_post.append(post)

fb_post = pd.DataFrame(fb_post)
fb_post = fb_post.drop(['post_text', 'shared_text', 'shared_text', 'image', 'video', 'video_thumbnail', 'video_id', 'shares', 'link', 'user_id', 'username', 'is_live', 'factcheck', 'shared_post_id', 'shared_time', 'shared_user_id', 'shared_username', 'shared_post_url', 'images', 'available'], axis=1)
fb_post = fb_post.drop(['video_size_MB', 'video_watches', 'video_width', 'likes'], axis=1)
fb_post = fb_post.drop(['image_lowquality', 'images_description', 'images_lowquality', 'images_lowquality_description', 'video_duration_seconds', 'video_height', 'video_quality', 'image_ids', 'image_id', 'reaction_count', 'reactions', 'w3_fb_url', 'reactors', 'comments_full', 'user_url'], axis=1)
fb_post = fb_post.replace({'\n': ' '}, regex=True)
fb_post = fb_post.rename(columns={"post_id":"_id"})

fb_id = []
for i in fb_post['_id']:
    fb_id.append(i)

print(fb_id)

options = Options()
options.headless = True
browser = webdriver.Firefox(executable_path="./geckodriver", options=options)
browser.get('https://m.facebook.com')
txtUser = browser.find_element_by_id("m_login_email")
txtUser.send_keys(config('GMAIL'))
txtPass = browser.find_element_by_id("m_login_password")
txtPass.send_keys(config('PASSWORD'))
txtPass.send_keys(Keys.ENTER)
time.sleep(2)
reactions = []
for i in fb_id:
    browser.get('https://m.facebook.com/ufi/reaction/profile/browser/?ft_ent_identifier={}'.format(i))
    soup = BeautifulSoup(browser.page_source, "html.parser")
    
    likes = soup.find_all('span', {'data-store': '{"reactionType":1}'})
    loves = soup.find_all('span', {'data-store': '{"reactionType":2}'})
    wows = soup.find_all('span', {'data-store': '{"reactionType":3}'})
    hahas = soup.find_all('span', {'data-store': '{"reactionType":4}'})
    sads = soup.find_all('span', {'data-store': '{"reactionType":7}'})
    cares = soup.find_all('span', {'data-store': '{"reactionType":16}'})
    
    
    if likes:
        for like in likes:
            like_list = like.text
    else:
        like_list = 0
    if loves:
        for love in loves:
            love_list = love.text
    else:
        love_list = 0
        
    if wows:
        for wow in wows:
            wow_list = wow.text
    else:
        wow_list = 0
        
    if hahas:
        for haha in hahas:
            haha_list = haha.text
    else:
        haha_list = 0
    if sads:
        for sad in sads:
            sad_list = sad.text
    else:
        sad_list = 0
    if cares:
        for care in cares:
            care_list = care.text
    else:
        care_list = 0

        
    reactions.append({'like': like_list, 'love': love_list, 'wow': wow_list, 'haha': haha_list, 'sad': sad_list, 'care': care_list})
    time.sleep(2)

reactions = pd.DataFrame(reactions)
fb = pd.concat([fb_post, reactions], axis=1, join='inner')

for post in fb.values.tolist():
    try:
        insert = {
            "_id": post[0],
            "text": post[1],
            "time": post[2],
            "comments": post[3],
            "post_url": post[4],
            "like": post[5],
            "love": post[6],
            "wow": post[7],
            "haha": post[8],
            "sad": post[9],
            "care": post[10]
        }
        db.dochoichu.insert_one(insert)
    except:
        if list(db.dochoichu.find({"_id": post[0]})) != []:
            pass