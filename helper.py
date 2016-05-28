# @app.route('/copy_items_to_list', methods=["POST"])
# def copy_items_to_list():
#     """save copied item(s) to list"""

    user_id = session['current_user']

    users_lists = List.list_name.query.filter_by(user_id = user_id).all()
    # want users existing lists (to populate dropdown to be made on form)

    list_name = request.form.get("list_name")
    location_name = request.form.get("location_name")

    location = Location.query.filter_by(location_name=location_name).first()

    if location == None:
        new_location = Location(location_name=location_name)
        db.session.add(new_location)
        db.session.commit()

        location = Location.query.filter_by(location_name=location_name).first()

    location_id = session['current_location'] = location.location_id

    new_list = List(user_id=user_id,
                    location_id=location_id,
                    list_name=list_name)

# try flush again for multiples

    db.session.add(new_list)
    db.session.commit()

    list_id = session['current_list'] = new_list.list_id

    # item_name, item_address, item_contents = get_item_choices(request)

    # def get_item_choices(request):

    #     category = Category.query.filter_by(category_name=category_name).first()
    #     category_name = request.form.get("category_name")
    #     item_name = request.form.get("item_name")
    #     item_address = request.form.get("item_address")
    #     item_comments = request.form.get("item_comments")
        
        # return (item_name, item_address, item_contents)

    final_item = Item(list_id=list_id,
                    category_id=category.category_id,
                    item_name=item_name,
                    item_address=item_address,
                    item_comments=item_comments)

    db.session.add(final_item)
    db.session.commit()

    flash ("%s has been copied" % item_name )

    return render_template("list_detail.html", 
                            lists=List.query.filter_by(list_id=list_id).first(), 
                            items=Item.query.filter_by(list_id=list_id).all())