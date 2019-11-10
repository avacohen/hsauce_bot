from bs4 import BeautifulSoup
import requests, re

def create_link_dictionary(soup):
	"""
	parses the soup to create a dictionary of sauce data
	:param soup: the soup of the saucenao page
	:return: the dictionary
	"""
	dic = {}

	# Creator - boorus; Material - boorus; Author - DeviantArt; Member - Pixiv

	creator = re.search(r"Creator: </strong>([\w\d\s\-_.*()\[\]]*)<br/>", str(soup))
	if creator and dic.get('Creator') is None:
		dic.update({'Creator': creator.group(1)})
	material = re.search(r"Material: </strong>([\w\d\s\-_.*()\[\]]*)<br/>", str(soup))
	if material and dic.get('Material') is None:
		dic.update({'Material': material.group(1)})
	author = re.search(r'Author: </strong><[\w\s\d="\-_./?:]*>([\w\d\s\-_.*()\[\]]*)</a>', str(soup))
	if author and dic.get('Author') is None:
		dic.update({'Author': author.group(1)})
	member = re.search(r'Member: </strong><[\w\s\d="\-_./?:]*>([\w\d\s\-_.*()\[\]]*)</a>', str(soup))
	if member and dic.get('Member') is None:
		dic.update({'Member': member.group(1)})

	for link in soup.find_all('a'):
		pg = link.get('href')
		if re.search(r"[\w]+\.deviantart\.com", pg) and dic.get('DeviantArt_art') is None:
			dic.update({'DeviantArt_art': pg})
		if re.search(r"deviantart\.com/view/", pg) and dic.get('DeviantArt_src') is None:
			dic.update({'DeviantArt_src': pg})
		if re.search(r"pixiv\.net/member\.", pg) and dic.get('Pixiv_art') is None:
			dic.update({'Pixiv_art': pg})
		if re.search(r"pixiv\.net/member_illust", pg) and dic.get('Pixiv_src') is None:
			dic.update({'Pixiv_src': pg})
		if re.search(r"gelbooru\.com/index\.php\?page", pg) and dic.get('Gelbooru') is None:
			dic.update({'Gelbooru': pg})
		if re.search(r"danbooru\.donmai\.us/post/", pg) and dic.get('Danbooru') is None:
			dic.update({'Danbooru': pg})
		if re.search(r"chan\.sankakucomplex\.com/post", pg) and dic.get('Sankaku') is None:
			dic.update({'Sankaku': pg})
	return dic


def get_source_data(picture_url):
	"""
	searches saucenao for an image
	:param picture_url: the image being searched for
	:return: the dictionary of data, or false if the image is not found on saucenao
	"""
	resp = requests.get('http://saucenao.com/search.php?db=999&url='+picture_url)
	txt = resp.text.split('Low similarity results')[0]  # Get rid of the low similarity results
	soup = BeautifulSoup(txt, 'html.parser')
	dic = create_link_dictionary(soup)
	if len(dic) == 0:
		return False
	dic.update({'SauceNAO': 'http://saucenao.com/search.php?db=999&url='+picture_url})
	return dic


if __name__ == "__main__":
	print("This is also a standalone program. You can put the image url in the line below.")
	sauce = get_source_data('https://i.imgur.com/5iWlGz2.png')
	
	# with open('comm', 'w') as ot:
	# 	for line in build_comment(sauce):
	# 		ot.write(line)

	# print("\n\n")
	# print("Overwiev:\n")
	# print("Creator: "+sauce.get('Creator', ''))
	# print("Material: "+sauce.get('Material', ''))
	# print("Author: "+sauce.get('Author', ''))
	# print("Member: "+sauce.get('Member', ''))
	# print("\nLinks:\n")
	# print("DeviantArt_art: "+sauce.get('DeviantArt_art', ''))
	# print("DeviantArt_src: "+sauce.get('DeviantArt_src', ''))
	# print("Pixiv_art: "+sauce.get('Pixiv_art', ''))
	# print("Pixiv_src: "+sauce.get('Pixiv_src', ''))
	# print("Gelbooru: "+sauce.get('Gelbooru', ''))
	# print("Danbooru: "+sauce.get('Danbooru', ''))
	# print("Sankaku: "+sauce.get('Sankaku', ''))
	# print("\n\n")
