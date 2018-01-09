from vg.scraping import steam_scraping
from vg.models import Page


def full_scraping():
    steam_page = new_page("Steam", "http://localhost")
    
    steam_scraping.get_all_game(steam_page)
    
    
    
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