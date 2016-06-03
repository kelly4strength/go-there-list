from model import connect_to_db, db, User, List, Location, Category, Item

#  categories, item_name, item_address, item_comments = get_item_choices(request)

def get_item_choices(request):

    category_names = request.form.getlist("category_name")  
    
    categories = []

    for category_name in category_names:
        if category_name:
            category = Category.query.filter_by(category_name=category_name).one()
            category_id = category.category_id   
            categories.append(category_id)
       
    item_name = request.form.getlist("item_name")
    item_address = request.form.getlist("item_address")
    item_comments = request.form.getlist("item_comments")

    return (categories, item_name, item_address, item_comments)

   




