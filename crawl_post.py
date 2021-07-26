from bs4 import BeautifulSoup
from facebook_scraper import get_posts
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import argparse
import pandas as pd
import time

ap = argparse.ArgumentParser()
ap.add_argument("--page", help="the unique profile name")
ap.add_argument("--group", type=int, help="provide a unique id of the group")
ap.add_argument("-t", "--title", required=True, help="title of csv file")
ap.add_argument("-n", "--number", type=int, default=3, help="number of post to crawl")
ap.add_argument("-u", "--username", required=True, help="Gmail or username of your facebook account")
ap.add_argument("-p", "--password", required=True, help="password of your facebook account")
args = vars(ap.parse_args())

fb_post = []

if args["page"]: # option if you want to crawl PAGES
    for post in get_posts(args['page'], pages=args["number"]):
        fb_post.append(post)
elif args["group"]: # option if you want to crawl GROUP
    for post in get_posts(args['group'], pages=args["number"], cookies="cookies.txt"):
        fb_post.append(post)

# Post process data
fb_post = pd.DataFrame(fb_post)
fb_post = fb_post.drop(['post_text', 'shared_text', 'shared_text', 'image', 'video', 'video_thumbnail', 'video_id', 'shares', 'link', 'user_id', 'username', 'is_live', 'factcheck', 'shared_post_id', 'shared_time', 'shared_user_id', 'shared_username', 'shared_post_url', 'images', 'available'], axis=1)
fb_post = fb_post.drop(['video_size_MB', 'video_watches', 'video_width', 'likes'], axis=1)
fb_post = fb_post.drop(['image_lowquality', 'images_description', 'images_lowquality', 'images_lowquality_description', 'video_duration_seconds', 'video_height', 'video_quality', 'image_ids', 'image_id', 'reaction_count', 'reactions', 'w3_fb_url', 'reactors', 'comments_full', 'user_url'], axis=1)
fb_post = fb_post.replace({'\n': ' '}, regex=True)
fb_post = fb_post.rename(columns={"post_id":"_id"})

# Get all of the posts' id to crawl reactions
fb_id = []
for i in fb_post['_id']:
    fb_id.append(i)

# Use selenium web driver with firefox's driver and headless option
options = Options()
options.headless = True
browser = webdriver.Firefox(executable_path="./geckodriver", options=options)

# Login to facebook
browser.get('https://m.facebook.com')
txtUser = browser.find_element_by_id("m_login_email")
txtUser.send_keys(args["username"])
txtPass = browser.find_element_by_id("m_login_password")
txtPass.send_keys(args["password"])
txtPass.send_keys(Keys.ENTER)
time.sleep(2)

# Crawl posts' reactions
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

# convert DataFrame to csv file
fb.to_csv(args["title"])