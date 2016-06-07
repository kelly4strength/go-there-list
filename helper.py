from model import connect_to_db, db, User, List, Location, Category, Item

#  categories, item_name, item_address, item_comments = get_item_choices(request)

def get_item_choices(category_names):
    """pass categories into copied items"""
    categories = []

    for category_name in category_names:
        if category_name:
            category = Category.query.filter_by(category_name=category_name).one()
            category_id = category.category_id   
            categories.append(category_id)
    return categories

   

def flash_copied_item_names(item_name):
    """add 'and' between copied item names in flash"""
    
    name =""
    for num in range(len(item_name)):
        name += ' and ' + item_name[num]
    return str(name[5:])


def flash_added_item_names(item_name):
    """add 'and' between copied item names in flash"""
    
    name =""
    for num in range(len(item_name)):
        name += ' ' + item_name[num]
    return str(name[1:])

#from the copy_items route....
# def get_item_choices(item_ids):

