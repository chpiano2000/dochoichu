# dochoichu

## Usage
1. **-t, --title**: Required. Name to export csv file
2. **-n, --number**: Default is **3**. Number 3 correspond to 10 posts from the newest. after 3, for each plus 1, it corresponds to four posts
    for example: 3->10 posts, 4->14 posts, 5->18 posts, 6->24 posts, ......
4. **-u, --username**: Required. A username of a real facebook account
5. **-p, --password**: Required. A password of a real facebook account
```
python3 crawl_post.py -t "dochoichu.csv" -u "test@gmail.com" -p "matkhaumanh"
```
## get old data
- run get_data.py to get old data stored in my mongodb atlas
