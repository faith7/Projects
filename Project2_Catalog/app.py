from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   jsonify)

from flask import session as login_session
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Item, User, Base
from sqlalchemy import desc
import urllib.request
import json
import os
import requests
import random
import string
from flask import session as login_session
import random
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import string
from flask import make_response
import requests


# Setting the name of the Flask instance to app
app = Flask(__name__)

# Connect to database
engine = create_engine('sqlite:///itemcatalog.db',
                       connect_args={'check_same_thread': False}, echo=True)


# Bind engine with database session
DBSession = sessionmaker(bind=engine)
session = DBSession()


# To restart to cache again (to prevent loading the same picture twice)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1


###############################
# Show Category(ies)/Item(s)
###############################


# Create root route that directs to category url
# Shows every category and item available in the system
# with the top five latest list
@app.route('/')
@app.route('/catalog')
def showCatalog():
    # Get all categories
    categories = session.query(Category).all()
    # Retrieve five recently realeased movie/show titles
    item5 = session.query(Item).order_by(Item.release.desc()).limit(5)
    url = []
    title = []
    for item in item5:
        url.append(item.img)
        title.append(item.title)
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


# Show items within the specific category
@app.route('/catalog/<int:category_id>')
def showCategory(category_id):
    # Query all the categories
    categories = session.query(Category).all()
    # Query a specific category
    category = session.query(Category).filter_by(id=category_id).one()
    # Get name of category
    categoryName = category.genre
    # Get all the items within the specific category
    items = session.query(Item).filter_by(category_id=category.id).all()

    return render_template('category.html', categories=categories, items=items,
                           category=category, categoryName=categoryName,
                           category_id=category_id
                           )


# Show individual item within a category
@app.route('/catalog/<int:category_id>/<int:item_id>')
def showItem(category_id, item_id):

    # Select one category
    category = session.query(Category).filter_by(id=category_id).one()
    # Find the item in the category
    item = session.query(Item).filter_by(id=item_id).one()
    url = item.img

    with open('static/local', 'wb') as f:
        f.write(urllib.request.urlopen(url).read())

    # check if username is in login_session or user is creater
    if 'username' not in login_session or \
            item.user_id != login_session['user_id']:
        return render_template('publicItem.html', category=category, item=item,
                               category_id=category_id, item_id=item_id)
    else:
        return render_template('item.html', category=category, item=item,
                               category_id=category_id, item_id=item_id)


######################
# Manage a Category
######################


# Create new category
@app.route('/catalog/new', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))

    if request.method == 'POST':
        genre = request.form['genre']
        user_id = login_session['user_id']
        newCategory = Category(genre=genre, user_id=user_id)
        session.add(newCategory)
        session.commit()

        flash("You just created a new Category!")
        return redirect(url_for('showCategory', category_id=1))
    else:
        return render_template('newCategory.html')


# Edit a category
@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editCat = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')

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


# Delete a category
@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
def delCategory(category_id):
    delCategory = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(delCategory)
        session.commit()
        flash("You successfully deleted the category!")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('delCategory.html', delCategory=delCategory,
                               category_id=category_id)

###################
# Manage an Item
###################


# Create a new item
@app.route('/catalog/newItem', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        # request form data from brower
        show = request.form['show']
        category = request.form['category']
        category = int(category)
        title = request.form['title']
        description = request.form['description']
        release = request.form['release']
        img = request.form['img']
        user_id = login_session['user_id']
        if img == '':
            img = "https://upload.wikimedia.org/wikipedia/commons/4/4f/\
                   Black_hole_-_Messier_87_crop_max_res.jpg"
        # Create item from requested data
        newItem = Item(show=show, title=title, description=description,
                       release=release, img=img, category_id=category,
                       user_id=user_id)

        session.add(newItem)
        session.commit()

        flash("You just created a new Item!")
        return redirect(url_for('showCatalog'))
    else:
        categories = session.query(Category).all()
        return render_template('newItem.html', categories=categories)


# Edit an item
@app.route('/catalog/<int:category_id>/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    editItem = session.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['show'] == '':
            editItem.show = editItem.show
        else:
            editItem.show = request.form['show']

        if request.form['title'] == '':
            editItem.title = editItem.title
        else:
            editItem.title = request.form['title']

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
            editItem.category_id = editItem.category_id
        else:
            editItem.category_id = request.form['category']

        session.add(editItem)
        session.commit()
        flash("You just updated the Item!")
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('editItem.html',
                               editItem=editItem, categories=categories,
                               category=category, item_id=item_id,
                               category_id=category_id)


# Delete an item
@app.route('/catalog/<int:category_id>/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def delItem(category_id, item_id):
    delItem = session.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(delItem)
        session.commit()
        flash("You deleted the item successfully")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('delItem.html', category_id=category_id,
                               item_id=item_id, delItem=delItem)


####################
# JSON END POINT
####################


# Create JSON endpoint for the catalog
@app.route('/catalog/JSON')
def showCatalogJSON():
    # Get all categories
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize
                               for category in categories])


# Create JSON endpoint for all  items the within the specific category
@app.route('/catalog/<int:category_id>/JSON')
def showCategoryJSON(category_id):
    # Get all the items within the specific category
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(items=[item.serialize for item in items])


# Create JSON end point for individual item within a category
@app.route('/catalog/<int:category_id>/<int:item_id>/JSON')
def showItemJSON(category_id, item_id):
    # Find the item in the category
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=[item.serialize])

######################################
# Helper Functions for User
######################################

# id = Column(Integer, primary_key=True)
#     name = Column(String)
#     email = Column(String, nullable=False)
#     profile_pic = Column(String)


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

######################################
# LOG IN
######################################


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Netflix Recomendation Application"


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Connect to server
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response
        (json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if  user exists, if it doesn't make a new one.
    user_id = getUserID(data['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    flash("you are now logged in as %s" % login_session['username'])

    output = ''
    output += '<h1><br><br><br>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '''style = "margin-top:20%;
                 width: 100px;
                 height: 100px;
                 border-radius: 15px;
                -webkit-border-radius: 150px;
                -moz-border-radius: 150px;" ><br>'''
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/logout')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            output), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        # response=make_response(render_template('logout.html'),200)
        response.headers['Content-Type'] = 'application/json'
        return response
        # return render_template("logout.html")

    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
