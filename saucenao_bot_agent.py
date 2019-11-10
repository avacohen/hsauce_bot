import discord
import os
from get_source import get_source_data
from dotenv import load_dotenv

from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')

# client = discord.Client()

bot = commands.Bot(command_prefix='!')


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

	em = discord.Embed(title="The Sauce:")

	if creator[0] != '':
		em.add_field(name='creator', value=creator[0])
	if creator[1] != '':
		if creator[2] != '':
			em.add_field(name='member',value='[{0}]({1})'.format(creator[1],creator[2]))
		else:
			em.add_field(name='member', value=creator[1])
	if creator[3] != '':
		if creator[4] != '':
			em.add_field(name='author', value='[{0}]({1})'.format(creator[3], creator[4]))
		else:
			em.add_field(name='member', value=creator[3])

	if material[0] != '':
		em.add_field(name='material', value='[google search]({0})|[gelbooru search]({1})'.format(material[1], material[2]))

	if images.count(images[0]) != len(images):
		image_source = ['Pixiv', 'Gelbooru', 'Danbooru', 'Sankaku', 'DeviantArt']
		img_string_list = []
		for i in range(len(images)):
			if images[i] != '':
				img_string_list.append('[{0}]({1})'.format(image_source[i], images[i]))

		img_string = ' | '.join(img_string_list)
		em.add_field(name='image sources', value=img_string)
	return em

def cook_sauce(image_url):
	sauce = get_source_data(image_url)
	bot_reply = build_message(sauce)

	print(bot_reply)
	return "could not find sauce" if not bot_reply else bot_reply

@bot.event
async def on_message(message):
	if message.author == bot.user:
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
@bot.event
async def on_ready():
	guild = discord.utils.get(bot.guilds, name=GUILD)

	print(
		f'{bot.user} is connected to the following guild:\n',
		f'{guild.name}(id: {guild.id})\n'
	)


bot.run(TOKEN)
