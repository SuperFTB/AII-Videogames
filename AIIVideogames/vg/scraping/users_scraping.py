# -*- coding: utf-8 -*-

from django.contrib.auth.hashers import make_password

from vg.models import Game, MediaList, Category, GamePage, User, Valoration
from vg.scraping.common import open_link, open_link_cookies


def get_all_users():
	page_list = 1
	maxu = 1
	while True:
		soup = open_link('http://store.steampowered.com/search/?page=' + str(page_list))
		soup = soup.find('div', {'id' : 'search_result_container'})
		listA = soup.findAll('a')
		if not listA:
			break
		
		print '------------------ Page ' + str(page_list) + ' ------------------'
		for a in listA:
			if not a.parent.has_attr('class'):
				url = a['href']
				url = url[:url.find('?')]
				url = url.replace('http://store.steampowered.com/app/', '')
				url = url[:url.find('/')]
				url = 'http://steamcommunity.com/app/' + url + '/reviews/'
				rev = open_link(url)
				for user in rev.findAll('div', {'class': 'apphub_friend_block_container'}):
					user = user.find('a')['href']
					if get_one_user(user + 'recommended/', user.replace('http://steamcommunity.com/id/', '')
								.replace('http://steamcommunity.com/profiles/', '')[:-1]):
						maxu += 1
					if maxu >= 1000:
						return
				
		page_list += 1
			

def get_one_user(url, user):
	try:
		us = User(username=user, password=make_password(user))
		us.save()
		print user + ":"
	except:
		return False
	
	page = 1
	maxg = 1
	while True:
		end = True
		soup = open_link(url + u'?p=' + unicode(page))
		
		for r in soup.findAll('div', {'class': 'review_box_content'}):
			end = False
			game = r.find('a')['href'].replace('http://steamcommunity.com/app/', '')
			game = 'http://store.steampowered.com/app/' + game
			game = open_link_cookies(game, {'mature_content': '1', 
								'lastagecheckage': '1-January-1992',
								'birthtime': '694220401',
								'steamCountry': 'ES%7C89c6a3a2e0af7f45f261d7f43c3689c3'})
			title = game.find('div', {'class' : 'apphub_AppName'})
			if not title:
				title = ""
			else:
				title = title.text
				if not title:
					title = ""
			
			valoration = r.find('div', {'class': 'vote_header'}).find('img')['src'].endswith('Up.png')
			
			try:
				_g = Game.objects.get(name=title)
				Valoration(isPositive=valoration, user=us, game=_g).save()
				print "\t"+title + " (" + str(valoration) + ")"
			except:
				print "\tError"
			
			if maxg >= 20:
				end = True
				break
			maxg += 1
		
		if end:
			break
		page += 1
		
	return True
	
	