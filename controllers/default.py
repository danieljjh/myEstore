# -*- coding: utf-8 -*-

def index():
    # redirect(URL('showroom'))
    query = db(db.product.on_sale==True)
    category =make_tree()
    promo = query.select(db.product.promo_type,distinct=True)
    rows = query.select()
    response.title = "欢迎惠顾 众赢商城 ！"
    t = make_tree()
    return dict(rows=rows,category=category,promo=promo,tree=t)


def vendors():
    pass

def promotions():
    query = db((db.product.on_sale==True)
        & (db.product.promo_type=="促销"))
    category =make_tree()
    rows = query.select()
    response.title = "特价促销 ！"
    return dict(rows=rows,category=category)


def aboutus():
    response.title="上海众赢"
    return locals()

def freeware():
    query = db((db.product.on_sale==True)
        & (db.product.promo_type=="赠品"))
    category =make_tree()
    # promo = query.select(db.product.promo_type,distinct=True)
    rows = query.select()
    response.title = "厂家赠品大派送 ！"
    return dict(rows=rows,category=category)



def productdetails():
    if request.args:
        q = db((db.product.id == request.args[0])
            & (db.inventory.product == db.product.id)
            & (db.product.on_sale == True)
            )
        rows = q.select()
        if rows:
            response.title = rows[0].product.name
            return dict(rows=rows,d=rows)
        else:
            redirect(URL('default','index'))
    else:
        redirect(URL('default','index'))

def showroom():
    category = '/'.join(request.vars['c']) if request.vars else None
    rr = request.vars['c']
    rc = rr.split('-')
    # response.subtitle = '/'.join(x.replace('-',' ').title() for x in request.args)    
    cat = '/'.join(x.replace('-',' ').title() for x in rc)    
    response.subtitle = '/'.join(x.replace('-',' ').title() for x in rc)
    query = db.product.on_sale==True
    query &= db.product.id==db.inventory.product
    page = int(request.vars.get('page',1))-1
    if request.vars.id:
        query &= db.product.id == request.vars.id
    else:
        if cat:
            query &= db.product.category.startswith(cat)
        if request.vars.q:
            query &= reduce(lambda a,b:a&b,[db.product.name.contains(k) for k in request.vars.q])
    rows = db(query).select(orderby=db.product.id|db.inventory.id,limitby=(20*page,20*page+20))
    rows = group_rows(rows,'product','inventory')
    response.title = ""
    return locals()


def showroom2():
    category = '/'.join(request.args) if request.args else None
    rr = request.raw_args
    rc = rr.split('/')
    # response.subtitle = '/'.join(x.replace('-',' ').title() for x in request.args)    
    cat = '/'.join(x.replace('-',' ').title() for x in rc)    
    response.subtitle = '/'.join(x.replace('-',' ').title() for x in rc)
    query = db.product.on_sale==True
    query &= db.product.id==db.inventory.product
    page = int(request.vars.get('page',1))-1
    if request.vars.id:
        query &= db.product.id == request.vars.id
    else:
        if cat:
            query &= db.product.category.startswith(cat)
        if request.vars.q:
            query &= reduce(lambda a,b:a&b,[db.product.name.contains(k) for k in request.vars.q])
    rows = db(query).select(orderby=db.product.id|db.inventory.id,limitby=(20*page,20*page+20))
    rows = group_rows(rows,'product','inventory')
    response.title = ""
    return locals()

# def show_cart(editable=True):
#     if not session.cart: return T('Cart empty')
#     rows = [TR(qty,
#                A(product.name+ ' '+inventory.detail + ': ',inventory.best_price,
#                  _href=URL('showroom',vars=dict(id=product.id))),TD(
#                 A(I(_class='icon-plus-sign'),
#                   callback=URL('cart/add',
#                                vars=dict(id=inventory.id,editable=editable)),
#                   target='cart'),
#                 A(I(_class='icon-minus-sign'),
#                   callback=URL('cart/del',
#                                vars=dict(id=inventory.id,editable=editable)),
#                   target='cart'),
#                 A(I(_class='icon-remove-sign'),
#                   callback=URL('cart/clear',
#                                vars=dict(id=inventory.id,editable=editable)),
#                   target='cart'))
#                if editable else '')
#             for (qty,product,inventory) in session.cart.itervalues()]
#     results = price_cart()
#     rows.append(TR('',T('Total'),CURRENCY+'%.2f' % results['total']))
#     rows.append(TR('',T('Discount'),
#                    CURRENCY+'%.2f' % results['total_discount']))
#     # rows.append(TR('',T('Tax'),CURRENCY+'%.2f' % results['total_tax']))
#     return TABLE(*rows)


def show_cart(editable=True):
    if not session.cart: return '抢购中'
    rows = [  DIV(  
                    DIV(
                        A(
                        product.name + ' '+inventory.detail , BR(),' 单价：¥ ',inventory.best_price , ' 数量: ' , qty,
                        _href=URL('productdetails',args=(product.id)
                                ),
                        ),_class="col-md-8"
                    ),
                   DIV(
                        A('+',_class='btn btn-info btn-xs',
                                callback=URL('cart/add',
                                   vars=dict(id=inventory.id,editable=editable)
                                   ),target='cart'
                        ),_class="col-md-1"
                    ),
                    DIV(
                        A('-', _class="btn btn-warning btn-xs",
                                callback=URL('cart/del',
                                   vars=dict(id=inventory.id,editable=editable)
                                            ),target='cart'
                        ),_class="col-md-1"
                    ),
                    DIV(
                            A('清除',_class="btn btn-danger btn-xs",
                      callback=URL('cart/clear',
                                   vars=dict(id=inventory.id,editable=editable)),target='cart'
                            ),_class="col-md-1"
                    )
                     if editable else ''
                , _class="col-md-10 h5")
                    for (qty,product,inventory) in session.cart.itervalues()
            ]
    results = price_cart()
    rows.append(DIV(
                    T('总金额'),CURRENCY+'%.2f' % results['total'],_class=" col-md-10 h4"
                ))
    rows.append(DIV(
                T('折扣'),CURRENCY+'%.2f' % results['total_discount'],_class=" col-md-10 h4"
                ))
    # rows.append(TR('',T('Tax'),CURRENCY+'%.2f' % results['total_tax']))
    return DIV(*rows,_class="row")

def cart():
    if request.vars.id and request.vars.id.isdigit():
        inventory_id = int(request.vars.id)
        qty, _, _ = session.cart.get(inventory_id,(0,None,None))
        command = request.args(0)
        if command=='clear': qty = 0
        elif command=='del': qty = max(0,qty - 1)
        elif command=='add': qty = max(0,qty + 1)
        if command!='show':
            inventory = db.inventory(inventory_id)
            if inventory:
                product = db.product(inventory.product)
                if qty:
                    session.cart[inventory_id] = [qty, product, inventory]
                else:
                    del session.cart[inventory_id]
    return show_cart(request.vars.get('editable','true').lower()!='false')

def cartlist():
    # if not session.cart: return '抢购中...'
    return dict(t=price_cart())

def myorders():
    return locals()

def myorder():
    return locals()

# @auth.requires_login()
def checkout():
    if price_cart()['total'] > 0:
        response.title="谢谢惠顾，请填写收货信息"
        if session.checkout_form and not request.post_vars:
            for key in session.checkout_form:
                db.cart_order[key].default = session.checkout_form[key]
        form = SQLFORM(db.cart_order,
            formstyle='table3cols',
            ).process(dbio=False)
        if form.accepted:
            session.checkout_form = form.vars
            redirect(URL('pay'))
        return locals()
    else:
        redirect(URL('default','index'))

# def pay():
#     from gluon.contrib.stripe import StripeForm
#     results = price_cart()
#     stripe_form = StripeForm(
#         pk=STRIPE_PUBLIC_KEY,
#         sk=STRIPE_SECRET_KEY,
#         amount=int(100*results['total_with_shipping']),
#         description="Nothing")
#     stripe_form.process()
#     if stripe_form.accepted:
#         payment_id = stripe_form.response['id']            
#         d = dict(session.checkout_form)
#         d.update({'total':results['total'],
#                   'total_discount':results['total_discount'],
#                   'total_tax':results['total_tax'],
#                   'total_after_tax':results['total_after_tax'],
#                   'total_with_sipping':results['total_with_shipping'],
#                   'amount_due':results['total_with_shipping'],
#                   'amount_paid':results['total_with_shipping'],
#                   })
#         order_id = db.cart_order.insert(**d)
#         db.payment.insert(payment_id=payment_id,cart_order=order_id)
#         for id,(qty, product, invoice) in session.cart.items():
#             d = dict(                
#                 invoice=invoice_id,
#                 product=id,
#                 quantity=qty)
#             d.update(product)
#             d.update(invoice)
#             db.invoice_item.insert(**db.invoice_item._filter_fields(d))
#         session.cart.clear()
#         session.checkout_form = None
#         session.order_id = order_id
#         redirect(URL('thank_you'))
#     elif stripe_form.errors:
#         redirect(URL('pay_error'))
#     return dict(stripe_form=stripe_form)


def pay():
    # from gluon.contrib.stripe import StripeForm
    import random
    results = price_cart()
    form = FORM(
        INPUT(_name="check",_type="checkbox",_id="confirmorder"),
        LABEL('订单已核对无误'),BR(),
        INPUT(_type="submit",_value="去支付宝付款",_class="btn btn-success",_id="topay")
        )
    form.process()
    if form.accepted:
    # payment_id = stripe_form.response['id']    
        payment_id = random.randrange(1,90801) 
        d = dict(session.checkout_form)
        d.update({'total':results['total'],
                  'total_discount':results['total_discount'],
                  'deli_cost':results['total'],
                  # 'amount_paid':results['total'],
                  })
        order_id = db.cart_order.insert(**d)
        db.payment.insert(payment_id=payment_id,cart_order=order_id)
        invoice_id=db.invoice.insert(description="none",order_id = order_id,payment_id=payment_id,amount=results['total'])
        # invoice_id = random.randrange(1,9900)
        for id,(qty, product, inventory) in session.cart.items():
            d = dict(                
                invoice=invoice_id,
                inventory=inventory,
                quantity=qty,
                product=product)
            d.update(product)
            d.update(inventory)
            db.invoice_item.insert(**db.invoice_item._filter_fields(d))
            # db.invoice_item.insert(invoice=d['invoice'],quantity=d['quantity'],)
            db.commit()
        session.cart.clear()
        session.checkout_form = None
        session.order_id = order_id
        redirect(URL('thank_you'))
    # elif stripe_form.errors:
        # redirect(URL('pay_error'))
    return dict(form=form,c=session.cart,results=results,d=session.checkout_form)


def ship():
    return locals()

def thank_you():
    o = db((db.invoice.order_id == session.order_id) & (db.invoice_item.invoice == db.invoice.id)).select(
            db.invoice.id,db.invoice_item.invoice,db.invoice_item.quantity
        )
    s= session
    return locals()

def pay_error():
    return locals()

def user():
    return dict(form=auth())

@cache.action()
def download():
    return response.download(request, db)

def call():
    return service()
