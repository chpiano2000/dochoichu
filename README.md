# dochoichu

## Introduction
- YOu have to use a real facebook account to run this code
- I use a pakage facebook-scaper kevinzg to get contents and posts' id
- Then I use selenium to get reactions 

## Packages
- Use [facebook-scrawper](https://github.com/kevinzg/facebook-scraper) package to get contents and posts'id
- Use [Selenium Web Driver](https://pythonspot.com/selenium-webdriver/) to login to a facebook account to get all reactions of a post
- Use [Pandas' DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) to process data
- Use [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/) to extract data out of html file

## Installation
```
python3 -m  pip install -U -r requirement.txt
```

## Arguments
1. **--page**: Use this argument when you want to crawl facebook page. Provide the enpoint of the page
2. **--group**: Use this argument when you want to crawl facebook gropup. Provide the id of the group
3. **-t, --title**: Name to export csv file
4. **-n, --number**: Default is **3**. Number 3 correspond to 10 posts from the newest. after 3, for each plus 1, it corresponds to four posts
    for example: 3->10 posts, 4->14 posts, 5->18 posts, 6->24 posts, ......
4. **-u, --username**: Required. A username of a real facebook account
5. **-p, --password**: Required. A password of a real facebook account

## Usages
### Crawl pages
Get the last element of the pages' url. 
For example: Link to dochoichu's page is https://www.facebook.com/dochoichu/, so you need the "dochoichu" for the **-page** argument
```
python3 crawl_post.py --page "dochoichu" -t "dochoichu.csv" -u "test@gmail.com" -p "matkhaumanh"
```
### Crawl groups
- Crawl group is harder because there are private group
- [Export the cookie when you successfully login to a facebook account here](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg) and save it to **cookies.txt**
- [Go to this link to get the groiup's id](https://lookup-id.com/)
- run the **--group** with the group's id
```
python3 crawl_post.py --group 154819686702568 -n 3 -t "thacauthinhchu.csv" -u "test@gmail.com" -p "matkhaumanh"
```
## Common isues
1. Facebook will detect bot and you have to verify to login -> you should use another real facebook account or wait untill the next day 
2. There will be some warning of the facebook-scraper -> ignore them and wait untill your code finishes runing
## get old data
- run get_data.py to get old data stored in my mongodb atlas
