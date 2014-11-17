@auth.requires_membership('manager')
def products():
    grid = SQLFORM.smartgrid(db.product)
    return locals()