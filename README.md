# dochoichu

## In general
- Collecting facebook's content, link of each post, post_id via facebook_scraper library
- Collecting number of reactions via selenium with geckodriver (firefox)
- Using pandas to process data
- Using mongodb to store data

## .env file
- POST: number of array of posts (at least 2, 1 integer number = 4 posts)
- URL: link connecting to mongodb
- GMAIL: gmail of your facebook account
- PASSWORD: password of your facebook account

## How to use?

**Facebook Page Crawler** requires **five** arguments:

1. **app_id**: app_id of your Facebook app, the will used to access Facebook Graph API.
2. **app_secret**: app_secret of your Facebook app, the will used to access Facebook Graph API.
3. **targets**: The page name you want to crawl.
4. **since**: The date you want to start the crawling.
5. **until**: The date you want to finish the crawling.

