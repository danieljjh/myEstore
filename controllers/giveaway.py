#
def index():
    if request.args:
        q = db((db.product.id == request.args[0])
            & (db.product_image.product_id == db.product.id)
            & (db.product.on_sale == True)
            )
        rows = q.select()
        if rows:
            response.title = rows[0].product.name
            return dict(rows=rows,d=rows)
        else:
            redirect(URL('giveaway','index'))
    else:
        redirect(URL('default','freeware'))

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
            redirect(URL('giveaway','index'))
    else:
        redirect(URL('default','freeware'))



def checkout():
    # if price_cart()['total'] > 0:
    if request.args and request.args[0].isdigit():
        inventory_id = int(request.args[0])
        inventory = db.inventory(inventory_id)
        total = inventory.best_price
        if inventory:
            product = db.product(inventory.product)
            response.title="谢谢惠顾，请填写收货信息"
            form = SQLFORM(db.cart_order,
		        formstyle='table3cols',submit_button="免费申领"
		        ).process(dbio=False)
            if form.accepted:
		        session.checkout_form = form.vars
		        session.checkout_form.g_inventory=inventory_id
		        session.checkout_form.g_product=product.id
		        session.checkout_form.total=total
		        redirect(URL('pay'))
	return locals()
    else:
        redirect(URL('default','index'))


def cart():
    if request.vars.id and request.vars.id.isdigit():
        inventory_id = int(request.vars.id)
        qty, _, _ = session.cart.get(inventory_id,(0,None,None))
    	qty = max(0,qty + 1)
        inventory = db.inventory(inventory_id)
        if inventory:
            product = db.product(inventory.product)
            session.cart[inventory_id] = [qty, product, inventory]
            redirect(URL('checkout'))    	
    else:
    	redirect(URL('giveaway','index')) 
     




@cache.action()
def download():
    return response.download(request, db)

def pay():
    # from gluon.contrib.stripe import StripeForm
    import random
    form = FORM(
        # INPUT(_name="check",_type="checkbox",_id="confirmorder"),
        LABEL('订单已核对无误'),BR(),
        INPUT(_type="submit",_value="去支付宝付款",_class="btn btn-success",_id="topay")
        )
    dd = (session.checkout_form)
    total = dd.total
    form.process()
    if form.accepted:
        payment_id = random.randrange(1,90801) 
        order_id = db.cart_order.insert(**dd)
        db.payment.insert(payment_id=payment_id,cart_order=order_id)
        invoice_id=db.invoice.insert(description="none",order_id = order_id,payment_id=payment_id,amount=total)
        # invoice_id = random.randrange(1,9900)
        d = dict(                
            invoice=invoice_id,
            inventory=dd.g_inventory,
            quantity=1,
            product=dd.g_product
            )
        # db.invoice_item.insert(**db.invoice_item._filter_fields(d))
        # db.invoice_item.insert(invoice=d['invoice'],quantity=d['quantity'],)
        db.commit()
        session.checkout_form.clear()
        session.order_id = order_id
        redirect(URL('thank_you'))
    # elif stripe_form.errors:
        # redirect(URL('pay_error'))
    return dict(form=form,dd=session.checkout_form)

def thank_you():
    o = db((db.invoice.order_id == session.order_id) & (db.invoice_item.invoice == db.invoice.id)).select(
            db.invoice.id,db.invoice_item.invoice,db.invoice_item.quantity
        )
    s= session
    return locals()

