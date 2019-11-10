import discord
import os
from get_source import get_source_data
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')

bot = commands.Bot(command_prefix='!')


def build_data(dic):
    """
    organizes the information found so that the make_embed() method can use it
    :param dic: the dictionary of information
    :return: a list of the creator list, the material list, the image list, and the saucenao string. data that is not
    found is represented by an empty string
    """

    # creator, member, member pixiv link, author, author deviantart link
    creator = [''] * 5
    # material, google search, gelbooru search
    material = [''] * 3
    # pixiv link, gelbooru link, danbooru link, sankaku link, deviantart link
    images = [''] * 5
    saucenao = dic.get('SauceNAO')

    if (dic.get('Creator') or dic.get('Member') or dic.get('Author')) is not None:
        if dic.get('Creator') is not None:
            creator[0] = dic.get('Creator').title()
        if dic.get('Member') is not None:
            creator[1] = dic.get('Member')
            if dic.get('Pixiv_art') is not None:
                creator[2] = dic.get('Pixiv_art')
        if dic.get('Author') is not None and dic.get('Member') is None:
            creator[3] = dic.get('Author')
            if dic.get('DeviantArt_art') is not None:
                creator[4] = dic.get('DeviantArt_art')
    if dic.get('Material') is not None:
        material[0] = dic.get('Material').title()
        if dic.get('Material') != 'original':
            material[1] = 'http://www.google.com/search?q={}'.format('+'.join(dic.get('Material').split(' ')))
            material[2] = 'https://gelbooru.com/index.php?page=post&s=list&tags={}'.format(
                '_'.join(dic.get('Material').split(' ')))

    if (dic.get('Pixiv_src') or dic.get('Gelbooru') or dic.get('Danbooru') or dic.get('Sankaku') or dic.get(
            'DeviantArt_src')) is not None:
        if dic.get('Pixiv_src') is not None: images[0] = dic.get('Pixiv_src')
        if dic.get('Gelbooru') is not None: images[1] = dic.get('Gelbooru')
        if dic.get('Danbooru') is not None: images[2] = dic.get('Danbooru')
        if dic.get('Sankaku') is not None: images[3] = dic.get('Sankaku')
        if dic.get('DeviantArt_src') is not None: images[4] = dic.get('DeviantArt_src')

    # Handle no results (probably won't get here)
    if creator.count(creator[0]) == len(creator) and material.count(material[0]) == len(material) and \
            images.count(images[0]) == len(images):
        return False

    return [creator, material, images, saucenao]


def make_embed(data):
    """
    creates the embed message the bot will send to the channel
    :param data: the data, a list of three lists and a string, containing the found information
    :return: an embed object representing the message
    """
    # creator, member, member pixiv link, author, author deviantart link
    creator = data[0]
    # material, google search, gelbooru search
    material = data[1]
    # pixiv link, gelbooru link, danbooru link, sankaku link, deviantart link
    images = data[2]
    saucenao = data[3]

    em = discord.Embed(title="The Sauce:")

    if creator[0] != '':
        em.add_field(name='creator', value=creator[0])
    if creator[1] != '':
        if creator[2] != '':
            em.add_field(name='member', value='[{0}]({1})'.format(creator[1], creator[2]))
        else:
            em.add_field(name='member', value=creator[1])
    if creator[3] != '':
        if creator[4] != '':
            em.add_field(name='author', value='[{0}]({1})'.format(creator[3], creator[4]))
        else:
            em.add_field(name='member', value=creator[3])

    if material[0] != '':
        em.add_field(name='material',
                     value='[google search]({}) | [gelbooru search]({})'.format(material[1], material[2]))

    if images.count(images[0]) != len(images):
        image_source = ['Pixiv', 'Gelbooru', 'Danbooru', 'Sankaku', 'DeviantArt']
        img_string_list = []
        for i in range(len(images)):
            if images[i] != '':
                img_string_list.append('[{0}]({1})'.format(image_source[i], images[i]))

        img_string = ' | '.join(img_string_list)
        em.add_field(name='image sources', value=img_string)

    em.add_field(name='credits', value='[View full results]({}) | ported by [avalc0](https://github.com/avalc0) '
                                       '| original reddit bot by [u/Mistress_Mamiya](https://reddit.com/user/Mistress_Mamiya)'
                                       ' [(github)](https://github.com/MistressMamiya/hsauce_bot)'.format(saucenao))
    return em


def cook_sauce(image_url):
    """
    method to generate the sauce. first gets the source data from saucenao, and then builds a message based on this
    :param image_url: the url of the image being searched
    :return: an embed object that the bot will output
    """
    sauce = get_source_data(image_url)
    return discord.Embed(title="could not find sauce") if not sauce else make_embed(build_data(sauce))


@bot.event
async def on_message(message):
    """
    action to take on a message - check if the message contains an image, and if so finds the sauce and sends the
    sauce output message to discord
    :param message: the message being parsed
    :return: break if the message author is the bot
    """
    if message.author == bot.user:
        return

    if len(message.attachments) > 0:
        for attachment in message.attachments:
            url = attachment.url
            if url.lower().endswith('.jpg') or url.lower().endswith('.jpeg') or url.lower().endswith('.png'):
                bot_message = cook_sauce(url)
                await message.channel.send(embed=bot_message)


@bot.event
async def on_ready():
    """
    startup sequence. prints the bot and the server it is connected to
    """
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n',
        f'{guild.name}(id: {guild.id})\n'
    )
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="hentai"))


bot.run(TOKEN)
