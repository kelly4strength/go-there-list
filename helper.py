
#     item_name, item_address, item_contents = get_item_choices(request)
def get_item_choices(request):

    # category = Category.query.filter_by(category_name=category_name).first()
    # category_id = Category.query.filter_by(category_id=old_item.category_id).first()
    # category_name = request.form.get("category_name")
    # item_name = request.form.get("item_name")
    # item_address = request.form.get("item_address")
    # item_comments = request.form.get("item_comments")
    item_name = request.form.get("item_name")
    item_address = request.form.get("item_address")
    item_comments = request.form.get("item_comments")
    
    return (item_name, item_address, item_comments)


# def login_first(current_user):

#     if session.get('current_user') == None:
#         flash ("please login first")
#         return render_template("login.html") 

