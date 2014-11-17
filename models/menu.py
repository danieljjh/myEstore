# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B(COMPANY_NAME),XML('&trade;&nbsp;'),
                  _class="brand",_href="#")
response.title = COMPANY_NAME
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = '众赢商城'
response.meta.description = '众赢商城'
response.meta.keywords = '众赢商城'
response.meta.generator = '众赢商城'

## your http://google.com/analytics id
response.google_analytics_id = None

def make_tree():
    categories = db().select(db.product.category,distinct=True)
    tree = {'':[]}
    for c in categories:
        keys = c.category.split('/')
        last = tree['']
        for i in range(0,len(keys)):            
            key = '/'.join(keys[:i]) 
            last = tree[key]
            newkey = '/'.join(keys[:i+1])
            if not newkey in tree:
                tree[newkey] = subtree = []
                last.append((keys[i].replace('-',' ').title(),False,URL('showroom',args=keys[:i+1]),subtree))
    return tree['']

response.menu = cache.ram('categories',lambda:make_tree(),0 if auth.user and auth.user.is_manager else None)

