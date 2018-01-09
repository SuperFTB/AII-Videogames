from django.core.paginator import Paginator
from django.shortcuts import render_to_response

from vg.models import Game, MediaList, Category
from vg.scraping.scraping import full_scraping


def populate(request):
    full_scraping()
    return render_to_response('index.html')

def index(request):
    games = Game.objects.all()
    games_pages = Paginator(games, 20)
    games = games_pages.page(466)
    get_games_img(games)
    
    return render_to_response('index.html', {'games': games})

def list_category(request):
    items = []
    letter = ""
    count = 0
    for c in Category.objects.order_by('name'):
        if(c.name[0] != letter):
            items.append("L:" + c.name[0])
            letter = c.name[0]
            count += 1
        items.append("N:" + c.name)
        count += 1
        
    _items = items
    items = []
    count /= 7
    i = 0
    it = []
    for item in _items:
        it.append(item)
        i += 1
        if(i >= count):
            i = 0
            items.append(it)
            it = []
        
    return render_to_response('list_category.html', {'items': items})

def explore_category(request):
    name = request.GET.get('name')
    p = request.GET.get('p')
    if not p:
        p = 1
    p = int(p)
    
    cat = Category.objects.get(name=name)
    pages = Paginator(cat.games.all(), 12)
    games = get_games_img(pages.page(p))
    
    return render_with_pagination('base_games.html', {'title': 'Categoria: ' + name, 'games': games},
                                                    p, pages.num_pages, '/category/explore?name='+name)
    


def get_games_img(games):
    for g in games:
        g.img = get_game_img(g)
    return games
    
def get_game_img(game):
    res = MediaList.objects.filter(game=game)
    if not res:
        return ""
    return res[0].value

def render_with_pagination(template, model, p, max_p, requestURI):
    ran = []
    ran.append("1")
    
    temp = p-3
    if temp<=1:
        temp = 2
        
    if p-temp == 3:
        ran.append("...")
        
    for i in range(temp, p):
        ran.append(str(i))
        
    if p != 1:
        ran.append(p)
        
    temp = p+4
    if temp > max_p:
        temp = max_p
    
    for i in range(p+1, p+4):
        ran.append(str(i))
    
    if temp-p == 4 and temp != max_p:
        ran.append("...")
    
    if temp != max_p:
        ran.append(max_p)
    
    modelPage = {'p': p, 
          'p_next': str(p+1),
          'p_prev': str(p-1),
          'max_p': max_p,
          'range': ran,
          'requestURI': requestURI}
          
    model.update(modelPage)
    return render_to_response(template, model)
