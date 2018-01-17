# -*- coding: utf-8 -*-
from vg.models import Game, MediaList, Category, GamePage
from vg.scraping.common import open_link_json, open_link


def get_all_game(page):
	page_list = 1
	page_max = 2
	while page_list <= page_max:
		json = open_link_json('https://www.gog.com/games/ajax/filtered?mediaType=game&page='+str(page_list)+'&sort=title')
		page_max = int(json['totalPages'])
		
		print '------------------ Page ' + str(page_list) + ' ------------------'
		for g in json['products']:
			get_one_game(g, page)
		
		page_list += 1
			

def get_one_game(json, page):
	title = json['title']
	
	soup = open_link('https://www.gog.com' + json['url'])
	desc = u""
	for d in soup.find('div', {'class': 'description__text'}).contents:
		desc += unicode(d)
	
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
		
	get_media_of_game(game, soup, json)
	get_categories_of_game(game, soup)
	set_page(game, page, json)
	
	
	
def get_media_of_game(game, soup, json):
	imgs = []
	imgs.append("https:" + json['image'] + ".jpg")
	for img in soup.findAll('img', {'class': 'screen-tmb__img'}):
		i = img['src'].replace('112.jpg', '320.jpg')
		if not i.startswith('https:'):
			i = "https:" + i
			
		imgs.append(i)
		
	for img in imgs:
		try:
			MediaList(value = img, game = game).save()
		except:
			pass
	

def get_categories_of_game(game, soup):
	soup = soup.find('div', {'class': 'product-details-row'})
	for c in soup.findAll('a', {'class': 'un'}):
		cat_name = c.text
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
	
	
def set_page(game, page, json):
	price = json['price']['baseAmount']
	if not price:
		price = "0.0"
	else:
		price = float(price)
		
	try:
		GamePage(pageURL='https://www.gog.com' + json['url'], price=price, page=page, game=game).save()
	except Exception as e: 
		print(e)