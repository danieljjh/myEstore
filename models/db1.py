CURRENCY = '$'
INE = IS_NOT_EMPTY()

session.cart = session.cart or {}

auth.settings.extra_fields['auth_user'] = [
    Field('is_manager','boolean',default=True)
]
auth.define_tables(username=False, signature=False)
if auth.user: auth.user.is_manager = True

db.define_table(
    'product',
    Field('category'),
    Field('name',required=True),
    Field('description_short','text'),
    Field('description_long','text'),
    Field('private_info','text'),
    Field('unit_price','double'),
    Field('list_price','double'),
    Field('on_sale','boolean'),
    Field('rating','double'),
    Field('clicks','integer'),
    Field('image','upload'),
    Field('delivery',requires=IS_IN_SET(('normal','free','digital'))),
    Field('media_file','upload'),
    Field('rating','double'),
    Field('in_stock','integer'),
    Field('discount_2x','double',default=0),
    Field('discount_3x','double',default=0),
    Field('discount_4x','double',default=0),
    format='%(name)s')

db.define_table(
    'inventory',
    Field('product','reference product'),
    Field('detail'),
    Field('code'),
    Field('description','text'),
    Field('quantity','integer'),
    Field('qty_on_book','integer'),
    Field('list_price','double'),
    Field('best_price','double'),
    Field('fire_date','date',required=True),
    Field('serial_codes','list:string'))

db.define_table(
    'cart_order',
    Field('guest_name',requires=INE),
    Field('shipping_address',requires=INE),
    Field('leaving_city',requires=INE),
    # Field('shipping_zip',requires=INE),
    # Field('shipping_country',requires=INE),
    Field('guest_phone'),
    Field('booking_instructions','text'),
    Field('total','double',readable=False,writable=False),
    Field('total_discount','double',readable=False,writable=False),
    Field('amount_due','double',readable=False,writable=False),
    Field('amount_paid','double',readable=False,writable=False,default=0.0),
    auth.signature)

db.define_table(
    'payment',
    Field('cart_order','reference cart_order'),
    Field('payment_id'))

db.define_table(
    'shipping',
    Field('shipped_date','date'),
    Field('tracking_info'),
    Field('shipping_label'),
    Field('notes'))

db.define_table('invoice',
    Field('description','string'),
    Field('order_id','reference cart_order'),
    Field('amount','double'),
    Field('payment_id')
    )

db.define_table(
    'invoice_item',
    Field('invoice','reference invoice'),
    Field('quantity','integer',default=1),
    # Field('inventory','reference inventory'),
    # Field('shipping','reference shipping'),
    db.product,
    db.inventory
    ) # copy the prodoct, in case changes

def price_cart():    
    total_pretax = 0.0
    discount = 0.0
    for qty, product, inventory in session.cart.itervalues():
        # price = product.unit_price*qty
        price = inventory.best_price*qty
        n, d = qty, 0.0
        if n and product.discount_4x:
            d += product.discount_4x*int(n/4)
            n -= 4*int(n/4) 
        if n and product.discount_3x:
            d += product.discount_3x*int(n/3)
            n -= 3*int(n/3) 
        if n and product.discount_2x:
            d += product.discount_2x*int(n/2)
            n -= 2*int(n/2) 
        product.price = price
        total_pretax += price
        discount += d
    return dict(
        total = total_pretax,
        total_discount = discount)

def group_rows(rows,table1,*tables):
    last = None
    new_rows = []
    for row in rows:
        row_table1 = row[table1]
        if not last or row_table1.id!=last.id:
            last = row_table1
            new_rows.append(last)
            for t in tables:
                last[t] = []
        for t in tables:
            last[t].append(row[t])
    return new_rows
