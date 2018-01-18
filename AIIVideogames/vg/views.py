import os
import shelve

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template.context import RequestContext

from AIIVideogames.myWhoosh import inicia, buscar
from vg.models import Game, MediaList, Category, GamePage, Page, Valoration, \
    User
from vg.recommendations import transformPrefs, calculateSimilarItems, topMatches
from vg.scraping.scraping import full_scraping


def populate(request):
    full_scraping()
    return render_to_response('index.html')

def index(request):
    games = Game.objects.all()
    games_pages = Paginator(games, 16)
    games = games_pages.page(1)
    get_games_img(games)
    
    return render_to_response('index.html', {'games': games})

def list_category(request):
    items = []
    letter = ""
    count = 0
    for c in Category.objects.order_by('name'):
        if len(c.name) == 0:
            continue
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
    view = request.GET.get('view')
    name = request.GET.get('name')
    p = request.GET.get('p')
    if not p:
        p = 1
    if not view:
        view = 'list'
    p = int(p)
    
    cat = Category.objects.get(name=name)
    pages = Paginator(cat.games.all(), 12)
    
    max_p = pages.num_pages
    if p > max_p:
        p = max_p
    
    games = get_games_img(pages.page(p))
    get_games_price(games)
    
    model = {'title': 'Categoria: ' + name, 'games': games, 'view': view}
    model = render_with_pagination(model, p, max_p, '/category/explore?name='+name+"&p=")
    return render_to_response('list_games.html', model)
    
def search_game(request):
    text = request.GET.get('text')
    pmin = request.GET.get('min')
    pmax = request.GET.get('max')
    if not text:
        text = ''
    if not pmin:
        pmin = 0
    if not pmax:
        pmax = 999999
    
#     games = Game.objects.all()
#     games = GamePage.objects.filter(page=Page.objects.get(name="GOG.com"))
    a,b = inicia()
    games = get_game_by_title(buscar(text, pmin, pmax, a, b))
    get_games_img(games)
    get_games_price(games)
    
    if pmax > 100:
        pmax = "100+"
    
    model = {'games': games,
             'pages': Page.objects.all(), 
             'text': text, 
             'pmin': pmin, 
             'pmax': 100 if pmax > 100 else pmax}
    
    return render_to_response('base_games.html', model)


def view_game(request):
    game = Game.objects.filter(id=request.GET.get('game'))[0]
    shelf = shelve.open("dataRS.dat")
    ItemsPrefs = shelf['ItemsPrefs']
    shelf.close()
    recommended = topMatches(ItemsPrefs, int(request.GET.get('game')), n=5)
    items = []
    itemsMedia=[]
    for re in recommended:
        item = Game.objects.get(pk=int(re[1]))
        items.append(item)
        itemsMedia.append(MediaList.objects.filter(game=itemsMedia)[0])
    imgs = MediaList.objects.filter(game=game)
    gamePages = GamePage.objects.filter(game=game).order_by("-price")
    categories = Category.objects.filter(games__id=game.id)
    colors = ['default', 'primary', 'success', 'info', 'warning', 'danger']
    for i in range(len(categories)):
        categories[i].color = colors[i%len(colors)]
        
    num_pos = Valoration.objects.filter(game=game, isPositive=True).count()
    num_neg = Valoration.objects.filter(game=game, isPositive=False).count()
    
    return render_to_response('game.html', {'game': game,
                                            'imgs': imgs,
                                            'gamePages': gamePages,
                                            'categories': categories,
                                            'num_pos': num_pos,
                                            'num_neg': num_neg,
                                            'games': items,
                                            'games_images': itemsMedia})

def vote_game(request):
    game = Game.objects.filter(id=request.GET.get('game'))[0]
    val = Valoration.objects.filter(game=game)
    if not val:
        val = Valoration(isPositive=True, user=User.objects.all()[0], game=game)
     
    if request.GET.get('v') == 'pos':
        val.isPositive = True
    else:
        val.isPositive = False
         
    val.save()
        
    return view_game(request)


def log_in(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/perfil')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/perfil')
                else:
                    return render(request, 'noactivo.html')
            else:
                return render(request, 'nousuario.html')
    else:
        formulario = AuthenticationForm()
    context = {'formulario': formulario}
    return render(request, 'login.html', context)


@login_required(login_url='/login')
def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/login')
def perfil(request):
    games = Game.objects.all()
    games_pages = Paginator(games, 16)
    games = games_pages.page(1)
    get_games_img(games)
    
    p = request.GET.get('p')
    if not p:
        p = 1
        
    model = render_with_pagination({}, p, games_pages.num_pages, "/perfil?&p=")
    
    return render_to_response('perfil.html', model)

Prefs = {}  # matriz de usuarios y puntuaciones a cada a items
ItemsPrefs = {}  # matriz de items y puntuaciones de cada usuario. Inversa de Prefs
SimItems = []  # matriz de similitudes entre los items


def loadRS(request):
    loadDict()
    return render_to_response('loadRS.html')


def loadDict():
    shelf = shelve.open("dataRS.dat")
    users = User.objects.all()
    games = Game.objects.all()
    for u in users:
        for g in games:
            ratings = Valoration.objects.filter(user=u, game=g)
            user = int(u.id)
            itemid = int(g.id)
            if (ratings):
                for ra in ratings:
                    if (ra.isPositive):
                        rating = float(2)
                    else:
                        rating = float(0)
                    Prefs.setdefault(user, {})
                    Prefs[user][itemid] = rating
            else:
                rating = float(1)
                Prefs.setdefault(user, {})
                Prefs[user][itemid] = rating
    shelf['Prefs'] = Prefs
    shelf['ItemsPrefs'] = transformPrefs(Prefs)
    shelf['SimItems'] = calculateSimilarItems(Prefs, n=10)
    shelf.close()


def reccommendGame(request):
    game = None
    if request.method == 'GET':
        id = request.user.id
        shelf = shelve.open("dataRS.dat")
        ItemsPrefs = shelf['ItemsPrefs']
        shelf.close()
        recommended = topMatches(ItemsPrefs, int(id), n=4)
        items = []
        for re in recommended:
            item = Game.objects.get(pk=int(re[1]))
            items.append(item)
        return render_to_response('recommendedGames.html', {'games': items}, context_instance=RequestContext(request))


def get_games_img(games):
    for g in games:
        g.img = get_game_img(g)
    return games
    
def get_game_img(game):
    res = MediaList.objects.filter(game=game)
    if not res:
        return ""
    return res[0].value

def get_games_price(games):
    for g in games:
        g.price = get_game_price(g)
    return games

def get_game_price(game):
    res = GamePage.objects.filter(game=game)
    if not res:
        return ""
    
    _min = None
    for p in res:
        if not _min or p.price < _min:
            _min = p.price
            
    return str(_min)

def get_games_from_gamepage(gps):
    games = []
    for gp in gps:
        games.append(gp.game)
    return games

def get_game_by_title(titles):
    games = []
    for g in titles:
        games.append(Game.objects.filter(name=g[0])[0])
    return games

def render_with_pagination(model, p, max_p, requestURI):
    ran = []
    ran.append(1)
    
    temp = p-3
    if temp<=1:
        temp = 2
        
    if p-temp == 3:
        ran.append("...")
        
    for i in range(temp, p):
        ran.append(i)
        
    if p != 1:
        ran.append(p)
        
    temp = p+4
    if temp > max_p:
        temp = max_p+1
    
    for i in range(p+1, temp):
        ran.append(i)
    
    if temp-p == 4 and temp != max_p+1:
        ran.append("...")
        
    if temp != max_p+1:
        ran.append(max_p)
    
    modelPage = {'p': p, 
          'p_next': str(p+1),
          'p_prev': str(p-1),
          'max_p': max_p,
          'range': ran,
          'requestURI': requestURI}
          
    model.update(modelPage)
    return model
