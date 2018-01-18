# -*- coding: utf-8 -*-
import os, os.path, sqlite3

from whoosh.fields import *
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser, FuzzyTermPlugin, MultifieldParser
from whoosh.query import *


def inicia():
    pth = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/indiceJuego")
    if not os.path.exists(pth):
        os.mkdir(pth)
        esquemaJuego = Schema(titulo=KEYWORD(stored=True), descripcion=TEXT,
                              categorias=KEYWORD(stored=True), plataformas=KEYWORD(stored=True),
                              precio=NUMERIC(stored=True))
        indiceJuego = create_in("indiceJuego",esquemaJuego)
    else:
        indiceJuego = open_dir(pth)
 
    parser = MultifieldParser(["titulo"], schema=indiceJuego.schema)
    parser.add_plugin(FuzzyTermPlugin())
 
    return indiceJuego,parser


def insertaJuego(titulo, descripcion, categorias, plataformas, precio, indiceJuego):
    writerJuego = indiceJuego.writer()
    writerJuego.add_document(titulo=titulo, descripcion=descripcion, categorias=categorias,
                             plataformas=plataformas, precio=precio)
    writerJuego.commit()


def buscaPorTituloDesc(keyword, indiceJuego, parser):
    keyword = keyword + "~2"
    res = []
    with indiceJuego.searcher() as searcher:
        myquery = parser.parse(keyword)
        for hit in searcher.search(myquery, limit=None):
            res.append(hit.values())
    return res


def buscaPorCategoria(keyword, indiceJuego):
    res = []
    with indiceJuego.searcher() as searcher:
        myquery = QueryParser("categorias", indiceJuego.schema).parse("*:*")
        for hit in searcher.search(myquery, limit=None):
            for cat in hit["categorias"].split(","):
                if (cat == u(keyword)):
                    res.append(hit.values())
                    break
    return res


def buscaPorPlataforma(keyword, indiceJuego):
    res = []
    with indiceJuego.searcher() as searcher:
        myquery = QueryParser("plataformas", indiceJuego.schema).parse("*:*")
        for hit in searcher.search(myquery, limit=None):
            for plat in hit["plataformas"].split(","):
                if (plat == u(keyword)):
                    res.append(hit.values())
                    break
    return res


def buscaPrecioMayorQue(min, indiceJuego):
    res = []
    with indiceJuego.searcher() as searcher:
        myquery = NumericRange("precio", min, 99999999)
        for hit in searcher.search(myquery, limit=None):
            res.append(hit.values())
    return res


def buscaPrecioMenorQue(max, indiceJuego):
    res = []
    with indiceJuego.searcher() as searcher:
        myquery = NumericRange("precio", -1, max)
        for hit in searcher.search(myquery, limit=None):
            res.append(hit.values())
    return res


def buscaPrecioRango(min, max, indiceJuego):
    res = []
    with indiceJuego.searcher() as searcher:
        myquery = NumericRange("precio", min, max)
        for hit in searcher.search(myquery, limit=None):
            res.append(hit.values())
    return res


def buscaPorTituloDescPrecioMayorQue(keyword, min, indiceJuego, parser):
    keyword = keyword + "~2"
    res = []
    with indiceJuego.searcher() as searcher:
        myquery = And([parser.parse(keyword), TermRange("precio", min, 99999999)])
        for hit in searcher.search(myquery, limit=None):
            res.append(hit.values())
    return res


def buscaPorTituloDescPrecioMenorQue(keyword, max, indiceJuego, parser):
    keyword = keyword + "~2"
    res = []
    with indiceJuego.searcher() as searcher:
        myquery = And([parser.parse(keyword), TermRange("precio", -1, max)])
        for hit in searcher.search(myquery, limit=None):
            res.append(hit.values())
    return res


def buscar(keyword, min, max, indiceJuego, parser):
    keyword = keyword + "~2"
    res = []
    with indiceJuego.searcher() as searcher:
        myquery = And([parser.parse(keyword), TermRange("precio", min, max)])
        for hit in searcher.search_page(myquery, 1, pagelen=10):
            res.append(hit.values())
        
    return res


def db(indiceJuego):
    con = None
    try:
        con = sqlite3.connect('vg.db')
        cur1 = con.cursor()
        cur1.execute("SELECT * FROM 'vg_game'")
        juegos = cur1.fetchall()
        cur2 = con.cursor()
        cur2.execute("SELECT * FROM 'vg_page'")
        paginas = cur2.fetchall()
        cur3 = con.cursor()
        cur3.execute("SELECT * FROM 'vg_category'")
        categorias = cur3.fetchall()

        for juego in juegos:
            cats=""
            precio=0.0
            plats=""
            cur4 = con.cursor()
            cur4.execute("SELECT * FROM 'vg_category_games' WHERE game_id={jid}".format(jid=juego.__getitem__(0)))
            relacion_categoriasJuego = cur4.fetchall()
            for rel in relacion_categoriasJuego:
                if cats=="":
                    cats=categorias[rel.__getitem__(1)-1].__getitem__(1)
                else:
                    cats+=","+categorias[rel.__getitem__(1) - 1].__getitem__(1)
            cur5 = con.cursor()
            cur5.execute("SELECT * FROM 'vg_gamepage' WHERE game_id={jid}".format(jid=juego.__getitem__(0)))
            relacion_paginaJuego = cur5.fetchall()
            for rel in relacion_paginaJuego:
                if precio==0.0 or precio>rel.__getitem__(2):
                    precio=rel.__getitem__(2)
                if plats=="":
                    plats=paginas[rel.__getitem__(3)-1].__getitem__(1)
                else:
                    plats =","+paginas[rel.__getitem__(3) - 1].__getitem__(1)
            if cats=="":
                cats=u"None"
            if plats=="":
                plats=u"None"
            insertaJuego(juego.__getitem__(1),juego.__getitem__(2), cats, plats, precio, indiceJuego)

    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if con:
            con.close()


