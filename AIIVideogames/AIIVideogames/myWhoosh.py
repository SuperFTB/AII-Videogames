import os, os.path
from whoosh.fields import *
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.filedb.filestore import FileStorage
from whoosh.query import *
from whoosh.qparser import FuzzyTermPlugin, MultifieldParser
import sqlite3 as lite
import sys


def inicia():
    if not os.path.exists("indiceJuego"):
        os.mkdir("indiceJuego")
        esquemaJuego = Schema(titulo=KEYWORD(stored=True), descripcion=TEXT(stored=True), links=KEYWORD(stored=True),
                              categorias=KEYWORD(stored=True), plataformas=KEYWORD(stored=True),
                              precio=NUMERIC(stored=True))
        indiceJuego = create_in("indiceJuego",esquemaJuego)
    else:
        indiceJuego = open_dir("indiceJuego")

    parser = MultifieldParser(["titulo", "descripcion"], schema=indiceJuego.schema)
    parser.add_plugin(FuzzyTermPlugin())

    return indiceJuego,parser


def insertaJuego(titulo, descripcion, links, categorias, plataformas, precio, indiceJuego):
    writerJuego = indiceJuego.writer()
    writerJuego.add_document(titulo=titulo, descripcion=descripcion, links=links, categorias=categorias,
                             plataformas=plataformas, precio=precio)
    writerJuego.commit()


def buscaPorTituloDesc(keyword, indiceJuego, parser):
    keyword = keyword + "~4"
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
    keyword = keyword + "~4"
    res = []
    with indiceJuego.searcher() as searcher:
        myquery = And([parser.parse(keyword), TermRange("precio", min, 99999999)])
        for hit in searcher.search(myquery, limit=None):
            res.append(hit.values())
    return res


def buscaPorTituloDescPrecioMenorQue(keyword, max, indiceJuego, parser):
    keyword = keyword + "~4"
    res = []
    with indiceJuego.searcher() as searcher:
        myquery = And([parser.parse(keyword), TermRange("precio", -1, max)])
        for hit in searcher.search(myquery, limit=None):
            res.append(hit.values())
    return res


def buscaPorTituloDescPrecioRango(keyword, min, max, indiceJuego, parser):
    keyword = keyword + "~4"
    res = []
    with indiceJuego.searcher() as searcher:
        myquery = And([parser.parse(keyword), TermRange("precio", min, max)])
        for hit in searcher.search(myquery, limit=None):
            res.append(hit.values())
    return res


def db(indiceJuego):
    con = None

    try:
        con = lite.connect('vg.db')

        cur = con.cursor()
        cur.execute('SELECT SQLITE_VERSION()')

        data = cur.fetchone()

        print "SQLite version: %s" % data

    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if con:
            con.close()


if __name__ == "__main__":
    # INICIO
    indiceJuego,parser=inicia()

    # INSERTAR DATOS PRUEBA
    #insertaJuego(u"titulo1", u"desc1", u"url1,url2",u"cat1,cat2,cat3",u"plat1,plat2,plat3",50,indiceJuego)
    #insertaJuego(u"titulo2", u"desc2", u"url3,url4",u"cat2",u"plat3",20,indiceJuego)

    # INSERTAR DATOS DB
    db(indiceJuego)

    # TESTEO QUERIES
    pro1 = buscaPorTituloDesc("desc",indiceJuego,parser)
    print(pro1)
    print("-------------------------------")
    pro2 = buscaPorCategoria("cat2",indiceJuego)
    print(pro2)
    print("-------------------------------")
    pro3 = buscaPorPlataforma("plat3",indiceJuego)
    print(pro3)
    print("-------------------------------")
    pro4 = buscaPrecioMayorQue(10,indiceJuego)
    print(pro4)
    print("-------------------------------")
    pro5 = buscaPrecioMenorQue(40,indiceJuego)
    print(pro5)
    print("-------------------------------")
    pro6 = buscaPrecioRango(40, 60,indiceJuego)
    print(pro6)
    print("-------------------------------")
    pro7 = buscaPorTituloDescPrecioMayorQue("titulo", 10,indiceJuego,parser)
    print(pro7)
    print("-------------------------------")
    pro8 = buscaPorTituloDescPrecioMenorQue("desc1", 30,indiceJuego,parser)
    print(pro8)
    print("-------------------------------")
    pro9 = buscaPorTituloDescPrecioRango("desc1", 40, 50,indiceJuego,parser)
    print(pro9)
    print("-------------------------------")
