import discord
import os
from get_source import get_source_data
from comment_builder import build_comment, build_footprint
from dotenv import load_dotenv

# # Setting up PRAW
# # You have to enter your own values here. If confused, refer to any PRAW guide.
# reddit = praw.Reddit(client_id="Found at reddit.com/prefs/apps/", client_secret="Found at reddit.com/prefs/apps/", password="password", user_agent="rHentai_Bot", username="rHentai_Bot")
# print('Logged in as '+str(reddit.user.me()))
# subreddit = reddit.subreddit('hentai')
#

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')


client = discord.Client()

def build_message(dic):
	# creator, member, member pixiv link, author, author deviantart link
	creator = ['']*5
	# material, google search, gelbooru search
	material = ['']*3
	# pixiv link, gelbooru link, danbooru link, sankaku link, deviantart link
	images = ['']*5

	if (dic.get('Creator') or dic.get('Member') or dic.get('Author')) is not None:
		if dic.get('Creator') is not None:
			creator[0] = dic.get('Creator').title()
		if dic.get('Member') is not None:
			creator[1] = dic.get('Member')
			if dic.get('Pixiv_art') is not None:
				creator[2]=dic.get('Pixiv_art')
		if dic.get('Author') is not None and dic.get('Member') is None:
			creator[3] = dic.get('Author')
			if dic.get('DeviantArt_art') is not None:
				creator[4] = dic.get('DeviantArt_art')
	if dic.get('Material') is not None:
		material[0] = dic.get('Material').title()
		if dic.get('Material') != 'original':
			material[1] = 'http://www.google.com/search?q={0}'.join(dic.get('Material').split(' '))
			material[2] = 'https://gelbooru.com/index.php?page=post&s=list&tags={0}'.join(dic.get('Material').split(' '))

	if (dic.get('Pixiv_src') or dic.get('Gelbooru') or dic.get('Danbooru') or dic.get('Sankaku') or dic.get(
			'DeviantArt_src')) is not None:
		if dic.get('Pixiv_src') is not None: images[0]= dic.get('Pixiv_src')
		if dic.get('Gelbooru') is not None: images[1]= dic.get('Gelbooru')
		if dic.get('Danbooru') is not None: images[2]= dic.get('Danbooru')
		if dic.get('Sankaku') is not None: images[3]= dic.get('Sankaku')
		if dic.get('DeviantArt_src') is not None: images[4]= dic.get('DeviantArt_src')

	# Handle no results
	if creator.count(creator[0]) == len(creator) and material.count(material[0]) == len(material) and \
			images.count(images[0]) == len(images):
		return False

	return [creator, material, images]

def make_embed(data):
	# creator, member, member pixiv link, author, author deviantart link
	creator = data[0]
	# material, google search, gelbooru search
	material = data[1]
	# pixiv link, gelbooru link, danbooru link, sankaku link, deviantart link
	images = data[2]

	#link = creator[2] + "/collection/" + str(field[1]) + "test"
	#embed.add_field(name=str(field[0]), value="![test]!({})".format(variable))
	em = discord.Embed(title="The Sauce:")

	if creator[0] != '':
		# add creator field
		pass
	if creator[1]!='':
		# add member
		pass
		if creator[2] != '':
			#add pixiv link
			pass
	if creator[3]!='':
		pass
		#add author
		if creator[4] != '':
			pass
			#add author devart link

	if material[0] != '':
		pass
		#add material and links

	if images.count(images[0]) != len(images):
		# pixiv link, gelbooru link, danbooru link, sankaku link, deviantart link

		if images[0] != '':
			pass
		if images[1] != '':
			pass
		if images[2] != '':
			pass
		if images[3] != '':
			pass
		if images[4] != '':
			pass

	#add web source(probably not in code yet)
	#em.add_field(name="Its mine now", value="Add DiscordBot to your server! [Click here](https://discordapp.com/oauth2/authorize?client_id=439778986050977792&scope=bot&permissions=8)")
	return em

def cook_sauce(image_url):
	sauce = get_source_data(image_url)
	bot_reply = build_message(sauce)

	print(bot_reply)
	return "could not find sauce" if not bot_reply else bot_reply

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	# if message.content.startswith("!hello"):
	# 	msg = 'Hello there'.format(message)
	# 	await message.channel.send(msg)

	if len(message.attachments)>0:
		for attachment in message.attachments:
			url = attachment.url
			if url.lower().endswith('.jpg')or url.lower().endswith('.jpeg') or url.lower().endswith('.png'):
				print('is image')
				bot_message= make_embed(cook_sauce(url))
				await message.channel.send(embed=bot_message)
@client.event
async def on_ready():
	guild = discord.utils.get(client.guilds, name=GUILD)

	print(
		f'{client.user} is connected to the following guild:\n',
		f'{guild.name}(id: {guild.id})\n'
	)


client.run(TOKEN)
'''
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
'''