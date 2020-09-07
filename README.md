# A Harry Potter Economy (on Reddit)

Last December, I created a bot that allows users on the Harry Potter Reddit community to give each other Galleons, Sickles, and Knuts (units of Harry Potter universe currency). It also keeps track of each user's total awards using SQLite. In 9 months, about 5 awards have been given per day on average (about 1500 total). It's fun to give the money to other users, but with nothing to do with the money it can become a little stale.

I'd like to extend the functionality of this bot to allow users to use their awarded currency to purchase a variety of items from the Harry Potter universe, which will be stored in their Gringotts vault (our database). I'd also like users to be able to give other users items they buy to reward high-quality content. This all takes place when users use any one of a set of commands within any comment on the subreddit. 

I'm very open to brainstorming more ideas of how to extend the bot's functionality, this is just a starting point. There's no business angle to this--it's just a fun tool for a community I belong to.

If you want to see the bot's current functionality, head over to [the Harry Potter subreddit](reddit.com/r/harrypotter), find a post or comment you like, and reply to it using !redditGalleon, !redditSickle, or !redditKnut somewhere in the reply's text. The bot scans new comments every minute on the minute and will reply to your comment when it performs its next scan.

## Team
I'm looking for one or (maybe) two others to join the team. 
It's probably best if you're a Harry Potter fan, but not necessary.

## SQL
Currently using SQLite.

## NoSQL
I'm thinking of going with DynamoDB, but I'm open to anything.

## Business
N/A

## Legal
N/A

## Technical
- Finalize SQL and NoSQL databases
- Finalize client-side and server-side languages (python running on my EC2 instance is the current setup)
