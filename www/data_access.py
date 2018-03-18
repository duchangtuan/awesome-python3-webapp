#!/usr/bin/env python
# -*- coding:utf-8 -*-

# this is an example to access function of orm


import asyncio
import sys

import orm
from models import User
from models import Blog
from models import Comment

async def test(loop):
    await orm.create_pool(loop=loop, user='www-data', password='www-data', db='awesome')

    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')

    await u.save()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(loop))
    loop.close()
    if loop.is_closed():
        sys.exit(0)
