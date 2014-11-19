@auth.requires_membership('manager')
def index():
	pass


@auth.requires_membership('manager')
def products():
    grid = SQLFORM.smartgrid(db.product,linked_tables=['inventory'],field_id=None,exportclasses=None,csv=False,)
    return locals()

@cache.action()
def download():
    return response.download(request, db)
