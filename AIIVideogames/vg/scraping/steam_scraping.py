# -*- coding: utf-8 -*-
from vg.models import Game, MediaList, Category, GamePage
from vg.scraping.common import open_link, open_link_cookies


def get_all_game(page):
	page_list = 1
	while True:
		soup = open_link('http://store.steampowered.com/search/?page=' + str(page_list) + "&sort_by=Name_ASC")
		soup = soup.find('div', {'id' : 'search_result_container'})
		listA = soup.findAll('a')
		if not listA:
			break
		
		print '------------------ Page ' + str(page_list) + ' ------------------'
		for a in listA:
			if not a.parent.has_attr('class'):
				url = a['href']
				url = url[:url.find('?')]
				get_one_game(url, page)
				
		page_list += 1
			

def get_one_game(url, page):
	soup = open_link_cookies(url, {'mature_content': '1', 
								'lastagecheckage': '1-January-1992',
								'birthtime': '694220401',
								'steamCountry': 'ES%7C89c6a3a2e0af7f45f261d7f43c3689c3'})
	
	# Title
	title = soup.find('div', {'class' : 'apphub_AppName'})
	if not title:
		return
	else:
		title = title.text
		if not title:
			return
		
	# Description
	desc = soup.find(id='game_area_description')
	if desc:
		desc = desc.contents
	else:
		desc = u''
	
	# Process description
	_desc = u''
	i = 0
	for s in desc:
		if i >= 2:
			_desc += unicode(s)
		i+=1
	desc = _desc
	
	# Save
	game = None
	try:
		game = Game.objects.get(name=title)
		game.description = desc
		game.save()
		print title
	except:
		try:
			game = Game(name=title, description=desc)
			game.save()
			print title
		except:
			pass
	
	get_media_of_game(game, soup)
	get_categories_of_game(game, soup)
	set_page(game, page, soup, url)
	
	
	
def get_media_of_game(game, soup):
	medias = soup.find('div', {'id' : 'highlight_strip_scroll'})
	for img in medias.findAll('img'):
		try:
			MediaList(value = img['src'], game = game).save()
		except:
			pass
	

def get_categories_of_game(game, soup):
	for a in soup.findAll('a', {'class' : 'app_tag'}):
		cat_name = a.text.strip()
		try:
			cat = Category.objects.get(name=cat_name)
			cat.games.add(game)
			cat.save()
		except:
			try:
				cat = Category(name=cat_name)
				cat.save()
				cat.games.add(game)
				cat.save()
			except:
				pass
	
	
def set_page(game, page, soup, url):
	price = soup.find('div', {'class' : 'price'})
	if not price:
		price = soup.find('div', {'class' : 'discount_original_price'})
		if not price:
			price = 0
		else:
			price = price.get_text(strip=True).replace(',', '.')
	else:
		price = price.get_text(strip=True).replace(',', '.')
	
	if price != 0:
		price = price[:len(price)-1]
		try:
			price = float(price)
		except:
			price = 0
		
	try:
		GamePage(pageURL=url, price=price, page=page, game=game).save()
	except Exception as e: 
		print(e)
		
	return price