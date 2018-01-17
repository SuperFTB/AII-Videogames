from vg.models import Page
from vg.scraping import steam_scraping, ingles_scraping, gog_scraping,\
    users_scraping


def full_scraping():
    steam_page = new_page("Steam", "/static/steam.png")
    ingles_page = new_page("ElCorteIngles", "/static/ingles.png")
    gog_page = new_page("GOG.com", "/static/gog.png")
    
#     steam_scraping.get_all_game(steam_page)
#     ingles_scraping.get_all_game(ingles_page)
#     gog_scraping.get_all_game(gog_page)
    users_scraping.get_all_users()
    
    
    
def new_page(name, url):
    res = None
    try:
        res = Page.objects.get(name=name)
    except:
        try:
            res = Page(name=name, image=url)
            res.save()
        except:
            pass
    return res