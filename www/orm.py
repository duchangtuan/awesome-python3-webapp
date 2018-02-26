#!/usr/local/bin python3
# -*- coding: utf-8 -*-

import asyncio, logging
import aiomysql

def log(sql, args=()):
    logging.info('SQL: %s' % sql)

@asyncio.coroutine
def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = yield from aiomysql.create_pool(
            host=kw.get('host', 'localhost'),
            port=kw.get('port', 3306),
            user=kw['user'],
            password=kw['password'],
            db=kw['db'],
            charset=kw.get('charset', 'utf-8'),
            autocommit=kw.get('autocommit', True),
            maxsize=kw.get('maxsize', 10),
            minsize=kw.get('minsize', 1),
            loop=loop
            )

@asyncio.coroutine
def select(sql, args, size=None):
    log(sql, args)
    global __pool
    with (yield from __pool) as conn:
        cur = yield from conn.cursor(aiomysql.DictCuros)
        yield from cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            rs = yield from cur.fetchmany(size)
        else:
            rs = yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows returned: %s' %len(rs))
        return rs

@asyncio.coroutine
def execute(sql, args):
    # the coroutine encapsulate the operation for insert, update and delete
    log(sql, args)
    with (yield from __pool) as conn:
        try:
            cur = yield from conn.cursor()
            yield from cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount
            yield from cur.close()
        except BaseException as e:
            raise
        return affected

def create_args_string(num):
    # create a string that have some placeholders
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)

class Field(object):
    # the base class that used to store database column name and type
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        # the function used to print the object of the class elegantly
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)


