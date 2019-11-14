import discord
import os

from discord.ext.commands import has_permissions

from get_source import get_source_data
from dotenv import load_dotenv
from discord.ext import commands
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')
auto = True
# m = None
# bot_m = None

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


def add_image(em, data):
    """
    adds the current data (representing an image) to the embed message the bot will send to the channel
    :param em: the embed object being added to
    :param data: the data, a list of three lists and a string, containing the found information
    :return: the updated embed object
    """
    # creator, member, member pixiv link, author, author deviantart link
    creator = data[0]
    # material, google search, gelbooru search
    material = data[1]
    # pixiv link, gelbooru link, danbooru link, sankaku link, deviantart link
    images = data[2]
    saucenao = data[3]

    if creator[0] != '':
        em.add_field(name='creator', value=creator[0], inline=True)
    if creator[1] != '':
        if creator[2] != '':
            em.add_field(name='member', value='[{0}]({1})'.format(creator[1], creator[2]), inline=True)
        else:
            em.add_field(name='member', value=creator[1], inline=True)
    if creator[3] != '':
        if creator[4] != '':
            em.add_field(name='author', value='[{0}]({1})'.format(creator[3], creator[4]), inline=True)
        else:
            em.add_field(name='member', value=creator[3], inline=True)

    if material[0] != '':
        em.add_field(name='material', value='[{}]({})'.format(material[0], material[1]))
        # code for gelboru/google search of material
        '''
        if material[0] == 'Original':
            em.add_field(name='material', value=material[0], inline=False)
        else:
            em.add_field(name='material: '+material[0],
                        value='[google search]({}) | [gelbooru search]({})'.format(material[1], material[2]), inline=False)
        '''

    if images.count(images[0]) != len(images):
        image_source = ['Pixiv', 'Gelbooru', 'Danbooru', 'Sankaku', 'DeviantArt']
        img_string_list = []
        for i in range(len(images)):
            if images[i] != '':
                img_string_list.append('[{0}]({1})'.format(image_source[i], images[i]))

        img_string = ' | '.join(img_string_list)
        em.add_field(name='image sources', value=img_string, inline=True)

    # code for saucenao field
    em.add_field(name='SauceNao', value='[View full results]({})'.format(saucenao), inline=False)

    return em


def cook_sauce(em, image_url):
    """
    method to generate the sauce. first gets the source data from saucenao, and then builds a message based on this.
    :param em: the embed object being added to
    :param image_url: the url of the image being searched
    :return: an embed object that the bot will output
    """
    sauce = get_source_data(image_url)
    return em.add_field(name='\u200b', value="could not find sauce", inline=False) if not sauce else add_image(em, build_data(sauce))


def make_embed(message):


    """
    creates the embed object representing all photos in the message
    :param message: the message
    :return: the embed object representing the sauce
    """
    em = discord.Embed(title="The Sauce:")

    # if there are multiple files in the message
    if len(message.attachments) > 1:
        em.add_field(name='\u200b', value='====== Image #1 =======', inline=False)

    for i in range(len(message.attachments)):
        attachment = message.attachments[i]
        url = attachment.url

        if url.lower().endswith('.jpg') or url.lower().endswith('.jpeg') or url.lower().endswith('.png'):
            # if this is not the last item, add the next item's header
            em = cook_sauce(em, url)
            if i < len(message.attachments) - 1:
                em.add_field(name='\u200b', value='====== Image #'+str(i+2)+' =======', inline=False)

    # credits field
    '''
    em.add_field(name='\u200b', value='====== credits =======\nported by [avalc0](https://github.com/avalc0) | original reddit bot by'
                                       ' [u/Mistress_Mamiya](https://reddit.com/user/Mistress_Mamiya)'
                                       ' [(github)](https://github.com/MistressMamiya/hsauce_bot)', inline=False)
    '''
    return em


@bot.event
async def on_message(message):
    """
    action to take on a message - check if the message contains an attachment, and if so executes the sauce-finding
    methods and outputs the resulting embedded message to discord
    :param message: the message being parsed
    :return: break if the message author is the bot
    """

    await bot.process_commands(message)

    if message.author == bot.user:
        return
    if len(message.attachments) > 0 and 'ignore' not in message.content and (auto or (not auto and 'sauce' in message.content)):
            bot_message = make_embed(message)
            await message.channel.send(embed=bot_message)
    # print('message done')

'''
@bot.command()
async def sauce(ctx, r='all'):
    if len(m.attachments) > 0:
        global bot_m
        if r.lower() == 'all':
            print('here - all')
            bot_m = make_embed(m, 0, len(m.attachments))
        else:
            if re.search('\d+:|-\d+', r):
                l = r.split(':')
                if int(l[0]) < 1:
                    l[0] = 1
                if int(l[1]) > len(m.attachments):
                    l[1] = len(m.attachments)
                bot_m = make_embed(m, int(l[0])-1, int(l[1]))
        await m.channel.send(embed=bot_m)
'''

@bot.command()
async def sauce(ctx):
    pass

# async def can_post(user, need_admin, op, need_roles):
#     if op.lower() == 'and':
#         print('this is an and')
#         if (need_admin and user.administrator) and all(role in user.roles for role in need_roles):
#             print('can post--> returning true')
#             return True
#         else: return False
#     else:
#         print('this is not an and')
#         print('is admin: ', user.administrator)
#         print('user roles: ', user.roles)
#         print('need roles: ', need_roles)
#         if all(role in user.roles for role in need_roles):
#             print('has the roles--> returning true')
#             return True
#         if need_admin and user.administrator:
#             print('is admin--> returning true')
#             return True
#         return False
#     print('reached end--> returning false')
#     return False



@bot.command()
async def ignore(ctx):
    pass


@has_permissions(administrator=True)
@bot.command()
async def auto(ctx, state: str):
    global auto
    if state.lower() == 'on':
        auto = True
        await ctx.send('automatic response turned on')

    elif state.lower() == 'off':
        auto = False
        await ctx.send('automatic response turned off')

    elif state.lower() == 'toggle':
        auto = not auto
        await ctx.send('automatic response turned ' + str('on' if auto else 'off'))

    elif state.lower() == 'get':
        await ctx.send('automatic response is turned ' + str('on' if auto else 'off'))

    else:
        await ctx.send('invalid command - specify on, off or toggle')

@auto.error
async def auto_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('invalid command - specify on, off or toggle')


@bot.event
async def on_ready():
    """
    startup sequence. prints the bot and the server it is connected to
    """
    guild = discord.utils.get(bot.guilds, name=GUILD)
    global auto
    auto = True
    print(
        f'{bot.user} is connected to the following guild:\n',
        f'{guild.name}(id: {guild.id})\n'
    )
    # set the bot's activity
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="hentai"))


bot.run(TOKEN)
