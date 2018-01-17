# -*- coding: utf-8 -*-
from common import open_link
from vg.models import Game, MediaList, Category, GamePage


def get_all_game(page):
    page_num = 1

    while True:
        soup = open_link("https://www.elcorteingles.es/videojuegos/pc/juegos/"+str(page_num)+"?sorting=nameAsc")
        
        if soup.find('div', {'class': 'no-results'}):
            break
        
        soup = soup.find('div', {'class': 'c9 c12-xxs c12-xs c12-s c12-m'}) #todos los juegos

        print '--------------------------Page' + str(page_num) + '----------------------'

        for a in soup.findAll('div',{'class':'product-image'}):
            url = "https://www.elcorteingles.es"+a.a['href']
            get_one_game(url,page)

        page_num +=1



def get_one_game(url, page):
    soup = open_link(url)

    #Title
    title = soup.find('h2', {'class': 'title'})
    if not title:
        return
    else:
        title = title.text
        if not title:
            return
        if title.endswith(" PC"):
            title = title[:-3]

    #Description
    desc = soup.find('div', {'id': 'description'})
    description = desc.contents[0]
    
    # Save
    game = None
    try:
        game = Game.objects.get(name=title)
        game.description = description
        game.save()
        print title
    except:
        try:
            game = Game(name=title, description=description)
            game.save()
            print title
        except:
            pass

    if not game:
        game = Game.objects.get(name=title)
        set_page(game, page, soup, url)
    else:
        get_media_of_game(game, soup)
        get_categories_of_game(game, soup)
        set_page(game, page, soup, url)


def get_media_of_game(game, soup):
    medias = soup.find('ul',{'class':'alternate-images'})
    medias = medias.findAll('img')

    for img in medias:
        if img.has_attr('data-zoom-src'):
            media = u'https:' + img['data-zoom-src']
        else:
            media = u'https:' + img['src']
            
        try:
            MediaList(value = media, game = game).save()
        except:
            pass
            
            
def get_categories_of_game(game, soup):
    info = soup.find('div',{'class':'product-features c12'})
    lista = info.contents[0].encode('utf-8')
    num = lista.find("Género")
    i = 0
    cat_name = ""
    mitad = lista[num:]
    for l in mitad:  #recorro desde la G de género y salgo en cuanto supera los 5 < o >
        if i == 4 and l!="<":
            cat_name = cat_name+l

        if l==">" or l=="<":
            i+=1
            if i > 4: break

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
    if soup.findAll('span', {'class':'former stroked'}): #hay rebajas entonces el precio real se mete aqui
        price = soup.findAll('span', {'class': 'former stroked'})
        price1 = price[0].get_text().replace(',','.')
        price1 = price1[:-1]
    elif soup.findAll('span', {'class': 'current'}):  #precio de un juego sin rebajas
        price = soup.findAll('span', {'class': 'current'})
        price1 = price[0].get_text().replace(',', '.')
        price1 = price1[:-1]
    else:
        price1 = "0.0"
    
    try:
        GamePage(pageURL=url, price=float(price1), page=page, game=game).save()
    except Exception as e: 
        print(e)







