from IPython import display
from pprint import pprint
import pandas as pd
import seaborn as sns
sns.set(style='darkgrid', context='talk', palette='Dark2')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import praw

reddit = praw.Reddit(client_id='***',
                     client_secret='***',
                     user_agent='***',
                     username ='***',
                     password ='***')
reddit.read_only = True

#variables we need
comments = set()
results = []

#Select subreddits to scan in the array
subreddits = ['climate', 'politics','AskReddit','aww','worldnews','news','Showerthoughts','crypto','UpliftingNews','philosophy','todayilearned','AmItheAsshole','pics','videos','trees','conservative','antiwork','WorkReform','atheism','religion','CallOfDuty','mildlyinfuriating','jobs','funny','WatchPeopleDieInside']

#loop through each subreddit
for x in subreddits:
    print(x)

    #iterate through top 10 hot posts
    for topposts in reddit.subreddit(x).hot(limit=10):

        #clear variables
        comment = set()
        sia = SIA()

        #enter into each post
        url = 'https://www.reddit.com' + topposts.permalink
        print(topposts.permalink)
        toppost = reddit.submission(url=url)

        #get top 1000 comments in post
        toppost.comments.replace_more(limit = 1000)

        #create set of comments to analyze
        for comments in toppost.comments.list():
            comment.add(comments.body)
            
        #evaluate polarity and save to results
        for line in comment:     
            pol_score = sia.polarity_scores(line)
            pol_score['subreddit:'] = x
            pol_score['link:' ] = toppost.id
            pol_score['comment:'] = line
            results.append(pol_score)

#save results to csv file
df = pd.DataFrame.from_records(results)
df.to_csv('list.csv', index=False)
