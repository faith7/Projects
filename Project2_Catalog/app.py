from flask import Flask, render_template, url_for, request, redirect, flash, jsonify  # noqa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Item, User, Base
# base, user
from sqlalchemy import desc
import urllib.request
# import io
import requests
# from PIL import Image
import json
import os

# setting the name of the Flask instance to app
app = Flask(__name__)

# connect to database
engine = create_engine('sqlite:///itemcatalog.db',
                       connect_args={'check_same_thread': False}, echo=True)

# bind engine with database session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# create user function
# def createUser(login_session)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
# change to "redis" and restart to cache again

# # some time later
# cache.init_app(app)

''' create root route that directs to category url
 shows every category and item available in the system
 with the top five latest list
 '''


@app.route('/')
@app.route('/catalog')
def showCatalog():
    # get all categories
    categories = session.query(Category).all()
    # retrieve five recently realeased movie/show titles
    item5 = session.query(Item).order_by(Item.release.desc()).limit(5)
    url = []
    title = []
    for item in item5:
        url.append(item.img)
        title = item.title
    with open('static/recent0', 'wb') as f:
        f.write(urllib.request.urlopen(url[0]).read())
    with open('static/recent1', 'wb') as f:
        f.write(urllib.request.urlopen(url[1]).read())
    with open('static/recent2', 'wb') as f:
        f.write(urllib.request.urlopen(url[2]).read())
    with open('static/recent3', 'wb') as f:
        f.write(urllib.request.urlopen(url[3]).read())
    with open('static/recent4', 'wb') as f:
        f.write(urllib.request.urlopen(url[4]).read())
    return render_template('catalog.html', categories=categories,
                           item5=item5, title=title)


# show items within the specific category
@app.route('/catalog/<int:category_id>')
def showCategory(category_id):
    # query all the categories
    categories = session.query(Category).all()
    # query a specific category
    category = session.query(Category).filter_by(id=category_id).one()
    # get name of category
    categoryName = category.genre
    # get all the items within the specific category
    items = session.query(Item).filter_by(category_id=category.id).all()

    return render_template('category.html', categories=categories, items=items,
                           category=category, categoryName=categoryName,
                           category_id=category_id
                           )


# show individual item within a category
@app.route('/catalog/<int:category_id>/<int:item_id>')
def showItem(category_id, item_id):

    # select one category
    category = session.query(Category).filter_by(id=category_id).one()
    #  find the item in the category
    item = session.query(Item).filter_by(id=item_id).one()
    url = item.img

    with open('static/local', 'wb') as f:
        f.write(urllib.request.urlopen(url).read())

    return render_template('item.html', category=category, item=item,
                           category_id=category_id, item_id=item_id)


# create new category
@app.route('/catalog/new', methods=['GET', 'POST'])
def newCategory():

    if request.method == 'POST':
        genre = request.form['genre']
        newCategory = Category(genre=genre)
        session.add(newCategory)
        session.commit()

        flash("You just created a new Category!")
        return redirect(url_for('showCategory', category_id=1))
    else:
        return render_template('newCategory.html')


# create a new item
@app.route('/catalog/newItem', methods=['GET', 'POST'])
def newItem():

    if request.method == 'POST':
        # request form data from brower
        show = request.form['show']
        category = request.form['category']
        category = int(category)
        title = request.form['title']
        description = request.form['description']
        release = request.form['release']
        img = request.form['img']
        if img == '':
            img = "https://upload.wikimedia.org/wikipedia/commons/4/4f/Black_hole_-_Messier_87_crop_max_res.jpg"  # noqa
        # create item from requested data
        newItem = Item(show=show, title=title, description=description,
                       release=release, img=img, category_id=category)

        session.add(newItem)
        session.commit()

        flash("You just created a new Item!")
        return redirect(url_for('showCatalog'))
    else:
        categories = session.query(Category).all()
        return render_template('newItem.html', categories=categories)


# edit a category
@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editCat = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['genre'] == '':
            editCat.genre = editCat.genre
        else:
            editCat.genre = request.form['genre']
        session.add(editCat)
        session.commit()
        flash("You just updated a category!")
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('editCategory.html',
                               editCat=editCat, category_id=category_id)


# delete a category
@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
def delCategory(category_id):
    delCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(delCategory)
        session.commit()
        flash("You successfully deleted the category!")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('delCategory.html', delCategory=delCategory,
                               category_id=category_id)


# delete an item
@app.route('/catalog/<int:category_id>/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def delItem(category_id, item_id):
    delItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(delItem)
        session.commit()
        flash("You deleted the item successfully")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('delItem.html', category_id=category_id,
                               item_id=item_id, delItem=delItem)


# edit an item
@app.route('/catalog/<int:category_id>/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    editItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['show'] == '':
            editItem.show = editItem.show
        else:
            editItem.show = request.form['show']

        if request.form['title'] == '':
            editItem.title = editItem.title
        else:
            editItem.title = editItem.form['title']

        if request.form['description'] == '':
            editItem.description = editItem.description
        else:
            editItem.description = request.form['description']

        if request.form['release'] == '':
            editItem.release = editItem.release
        else:
            editItem.release = request.form['release']

        if request.form['img'] == '':
            editItem.img = editItem.img
        else:
            editItem.img = request.form['img']

        if request.form['category'] == '':
            editItem.category = editItem.category
        else:
            editItem.category = request.form['category']

        session.add(editItem)
        session.commit()
        flash("You just updated the Item!")
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('editItem.html',
                               editItem=editItem, categories=categories,
                               category=category, item_id=item_id,
                               category_id=category_id)

####################################
# JSON END POINT
####################################

# create JSON endpoint for the catalog
@app.route('/catalog/JSON')
def showCatalogJSON():
    # get all categories
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize
                               for category in categories])

# create JSON endpoint for all  items the within the specific category
@app.route('/catalog/<int:category_id>/JSON')
def showCategoryJSON(category_id):
    # get all the items within the specific category
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(items=[item.serialize for item in items])


# create JSON end point for individual item within a category
@app.route('/catalog/<int:category_id>/<int:item_id>/JSON')
def showItemJSON(category_id, item_id):
    #  find the item in the category
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=[item.serialize])


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=8080)
