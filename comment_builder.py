def build_comment(dic):
    output_comment = ''

    if (dic.get('Creator') or dic.get('Member') or dic.get('Author')) is not None:
        output_comment += '**Creator:** '
        if dic.get('Creator') is not None: output_comment += dic.get('Creator').title()+' | '
        if dic.get('Member') is not None:
            output_comment += dic.get('Member')
            if dic.get('Pixiv_art') is not None: output_comment += ' [^({{on Pixiv}})]({0})'.format(dic.get('Pixiv_art'))
            output_comment += ' | '
        if dic.get('Author') is not None and dic.get('Member') is None:
            output_comment += dic.get('Author')
            if dic.get('DeviantArt_art') is not None: output_comment +=' [^({{on DeviantArt}})]({0})'.format(dic.get('DeviantArt_art'))
            output_comment += ' | '
        output_comment += '\n\n'

    if dic.get('Material') is not None:
        output_comment += '**Material:** '+dic.get('Material').title()
        if dic.get('Material') != 'original':
            output_comment += ' [^({{Google it!}})](http://www.google.com/search?q={0}) [^({{Hentify it!}})](https://gelbooru.com/index.php?page=post&s=list&tags={1})'.format('+'.join(dic.get('Material').split(' ')), '_'.join(dic.get('Material').split(' ')))
        output_comment += '\n\n'

    if (dic.get('Pixiv_src') or dic.get('Gelbooru') or dic.get('Danbooru') or dic.get('Sankaku') or dic.get('DeviantArt_src')) is not None:
        output_comment += '**Image links:** '
        if dic.get('Pixiv_src') is not None: output_comment += '[Pixiv]({0}) | '.format(dic.get('Pixiv_src'))
        if dic.get('Gelbooru') is not None: output_comment += '[Gelbooru]({0}) | '.format(dic.get('Gelbooru'))
        if dic.get('Danbooru') is not None: output_comment += '[Danbooru]({0}) | '.format(dic.get('Danbooru'))
        if dic.get('Sankaku') is not None: output_comment += '[Sankaku]({0}) | '.format(dic.get('Sankaku'))
        if dic.get('DeviantArt_src') is not None: output_comment += '[DeviantArt]({0}) | '.format(dic.get('DeviantArt_src'))
        output_comment += '\n\n'

    # Handle no results
    if output_comment == '':
        return False

    output_comment += "---\n[^(View full results)]({0}) ^| [^(Message creator)](https://reddit.com/user/Mistress_Mamiya) ^| [^(GitHub)](https://github.com/MistressMamiya/hsauce_bot) ^| ^(Bad sauce? Reply with '!rm')".format(dic.get('SauceNAO'))

    return output_comment

def build_footprint():
    return 'Submission is not an image or sauce could not be found!\n\n---\n^(View full results) ^| [^(Message creator)](https://reddit.com/user/Mistress_Mamiya)'