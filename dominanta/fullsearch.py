# coding: utf-8

import glob
import os
import os.path
import psycopg2
import sys
import subprocess
import re

def get_cursor():
    conn = psycopg2.connect("dbname='dominanta' user='dominanta' host='localhost' password='dominanta'")
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    conn.set_client_encoding('utf-8')
    return conn.cursor()

def get_words(query):
    word = re.compile(r'(\w+)', re.U)
    words = word.findall(query)
    return words

def get_db_query(query):
    return " | ".join(get_words(query))

def search_articles(query):
    cur = get_cursor()
    db_query = get_db_query(query)
    SQL = u"SELECT id, ts_headline(name, to_tsquery('%s')), ts_headline(text, to_tsquery('%s')), ts_rank(tsv, to_tsquery('%s')) as rank from blog_article where tsv @@ to_tsquery('pg_catalog.russian', '%s') ORDER BY rank DESC;" % (db_query, db_query, db_query, db_query)
    cur.execute(SQL)
    
    res = []
    for resp in cur.fetchall():
        res.append({'id': resp[0],
                    'name': resp[1],
                    'text': resp[2]})

    return res

def search_archive(query):
    cur = get_cursor()
    db_query = get_db_query(query)
    
    # if archive
    SQL = u"SELECT id, ts_headline(name, to_tsquery('%s')), ts_headline(text, to_tsquery('%s')), ts_rank(tsv, to_tsquery('%s')) as rank from archive_archivefile where tsv @@ to_tsquery('pg_catalog.russian', '%s') ORDER BY rank DESC;" % (db_query, db_query, db_query, db_query)
    cur.execute(SQL)
    
    res = []
    for resp in cur.fetchall():
        res.append({'id': resp[0],
                    'name': resp[1],
                    'text': resp[2]})
    
    return res