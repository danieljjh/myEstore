CURRENCY = '¥'
INE = IS_NOT_EMPTY()

session.cart = session.cart or {}

auth.settings.extra_fields['auth_user'] = [
    Field('is_manager','boolean',default=True)
]
auth.define_tables(username=False, signature=False)
if auth.user: auth.user.is_manager = True

db.define_table(
    'product',
    Field('category',label="分类"),
    Field('tags',label="标签"),
    Field('promo_type',requires=IS_IN_SET(('促销','赠品'))),
    Field('name',required=True,label="产品名称"),
    Field('description_short','text',label="产品概述"),
    Field('description_long','text',label="产品详情"),
    # Field('private_info','text'),
    # Field('unit_price','double',label="促销价"),
    # Field('list_price','double',label="原价"),
    Field('on_sale','boolean',default=True,label="在售"),
    # Field('rating','double'),
    # Field('clicks','integer'),
    Field('image','upload',label="产品主图片"),
    Field('delivery',requires=IS_IN_SET(('normal','free',)),label="送货方式"),
    # Field('media_file','upload'),
    # Field('rating','double'),
    # Field('in_stock','integer'),
    Field('discount_2x','double',default=0,label="2件折扣"),
    # Field('discount_3x','double',default=0),
    Field('discount_4x','double',default=0,label="4件折扣"),
    format='%(name)s')

db.define_table(
    'inventory',
    Field('product','reference product'),
    Field('detail',label="规格"),
    Field('code'),
    Field('description','text',label="详情"),
    Field('quantity','integer',label="库存量"),
    Field('image','upload',label="产品主图片"),
    Field('qty_on_book','integer'),
    Field('list_price','double'),
    Field('best_price','double'),
    # Field('fire_date','date',required=True),
    # Field('serial_codes','list:string')
    format='%(detail)s'
    )

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
        # if n and product.discount_4x:
        #     d += product.discount_4x*int(n/4)+(inventory.list_price-inventory.best_price)*int(n/4)
        #     n -= 4*int(n/4) 
        # if n and product.discount_2x:
        #     d += product.discount_2x*int(n/2)+(inventory.list_price-inventory.best_price)*int(n/2)
        #     n -= 2*int(n/2) 
        d += (inventory.list_price - inventory.best_price) *n
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
