@auth.requires_membership('manager')
def index():
	pass


@auth.requires_membership('manager')
def products():
    grid = SQLFORM.smartgrid(db.product,field_id=None)
    return locals()