import praw
from get_source import get_source_data
from comment_builder import build_comment, build_footprint

# Setting up PRAW
# You have to enter your own values here. If confused, refer to any PRAW guide.
reddit = praw.Reddit(client_id="Found at reddit.com/prefs/apps/", client_secret="Found at reddit.com/prefs/apps/", password="password", user_agent="rHentai_Bot", username="rHentai_Bot")
print('Logged in as '+str(reddit.user.me()))
subreddit = reddit.subreddit('hentai')

def cook_sauce(image_url):
		sauce = get_source_data(image_url)
		bot_reply = build_comment(sauce)
		if type(bot_reply) == str:
			i_submission.reply(bot_reply).mod.distinguish(sticky=True)
			print("	Replied: Sauce has been processed [Comment stickied]")
		else:
			i_submission.reply(build_footprint()).mod.remove()
			print("	Replied: Sauce not found [Comment removed]")

for i_submission in subreddit.stream.submissions():
	print("Found {}".format(i_submission.id))
	replied = False
	for i_comment in i_submission.comments:
		if "View full results" in i_comment.body:
			replied = True
			print("	Ignored: Already replied in this thread")
			break
	if replied == False:
			image_url = i_submission.url
			if image_url[-4:] == '.jpg' or image_url[-4:] == '.png':
				cook_sauce(image_url)
			# Handle non-direct imgur links https://imgur.com/... or https://i.imgur.com/...
			elif (image_url[8:14] == 'imgur.' and image_url[17:20] != '/a/') or (image_url[8:16] == 'i.imgur.' and image_url[19:22] != '/a/'):
				cook_sauce(image_url+'.jpg')
			else:
				i_submission.reply(build_footprint()).mod.remove()
				print("	Replied: Unsupported submission type [Comment removed]")