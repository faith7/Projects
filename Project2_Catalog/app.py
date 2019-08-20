from flask import Flask, render_template, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Item
# base, user


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


# create root route that directs to category url
# showCatlog shows every category and item available
@app.route('/')
@app.route('/category')
def showCatalog():
    # get all categories
    categories = session.query(Category).all()
    # get all items
    items = session.query(Item).all()
    return render_template('catalog.html',
                           categories=categories, items=items)


# show category
@app.route('/category/<int:category_id>')
@app.route('/category/<int:category_id>/items')
def showCategory(category_id):
    # query all the categories
    categories = session.query(Category).all()
    # query specific category inquired by browser user
    category = session.query(Category).filter_by(id=category_id).first()
    # get name of category
    categoryName = category.genre
    # get all the items in the specific category
    items = session.query(Item).order_by(Item.id.desc())

    return render_template('category.html', categories=categories, items=item,
                           category=category,
                           category_id=category_id,
                           categoryName=categoryName,
                           )


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=8080)
