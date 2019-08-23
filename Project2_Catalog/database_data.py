# pep8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

# create engine
engine = create_engine('sqlite:///itemcatalog.db',
                       connect_args={'check_same_thread': False}, echo=True)

# drop & create database
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# bind the engine to the metadata of Base Class
Base.metadata.bind = engine

'''DBSession creates a staging zone for all objects loaded into the DBsession.
Session will not be persistent unitl session.commit() is called.
To revert back, use session.rollback()
'''
DBsession = sessionmaker(bind=engine)
session = DBsession()

# create random user
user1 = User(name="Robert Jr.", email="robert@udacity.com",
             profile_pic="https://randomuser.me/")
session.add(user1)
session.commit()

# create categories for the catalog
cat1 = Category(genre="Action")
session.add(cat1)
session.commit()

cat2 = Category(genre="Comedy")
session.add(cat2)
session.commit()

cat3 = Category(genre="Crime")
session.add(cat3)
session.commit()

cat4 = Category(genre="Horror")
session.add(cat4)
session.commit()

cat5 = Category(genre="Thriller")
session.add(cat5)
session.commit()

'''create items for the catalog
For current show, release year is set to current year
For finished show, relase year is set to season finished year'''
item1 = Item(show="movie", title="Avengers:End game",
             description='''part of avengers series. Hero movies.
             Check other Marvel's movies''',
             release="2019",
             category=cat1,
             # noqa
             img='''https://upload.wikimedia.org/wikipedia/en/0/0d/Avengers_Endgame_poster.jpg''')  # noqa

session.add(item1)
session.commit()

item2 = Item(show="movie", title="Batman begins",
             description="Background of batman. Recommend all series..",
             release="2015",
             category=cat1,
             img="https://upload.wikimedia.org/wikipedia/en/a/af/Batman_Begins_Poster.jpg")  # noqa

session.add(item2)
session.commit()

item3 = Item(show="show", title="Park and recreation",
             description="Sitcome..American politcal satire",
             release="2015",
             category=cat2,
             img="https://upload.wikimedia.org/wikipedia/en/2/24/Parks_and_recreation_season_1_cast.jpg")  # noqa
session.add(item3)
session.commit()

item4 = Item(show="movie", title="Luck-key",
             description="South Korean action comedy film ",
             release="2016",
             category=cat2,
             img="https://upload.wikimedia.org/wikipedia/en/b/b7/Luck_Key-poster.jpg")  # noqa

session.add(item4)
session.commit()

item5 = Item(show="show", title="Kim's Convenience",
             description="A sitcome on Canadian Korean convenience story",
             release="2016",
             category=cat2,
             img="https://upload.wikimedia.org/wikipedia/en/b/b7/Luck_Key-poster.jpg")  # noqa

session.add(item5)
session.commit()

item6 = Item(show="show", title="Breaking bad",
             description="drug trafficking",
             release="2013",
             category=cat3,
             img="https://upload.wikimedia.org/wikipedia/en/6/61/Breaking_Bad_title_card.png")  # noqa

session.add(item6)
session.commit()

item7 = Item(show="show",
             title="Dead to me",
             description='''A widow whose husband died of hit-and-run accident
             and her friend''',
             release="2019",
             category=cat3,
             img="https://upload.wikimedia.org/wikipedia/en/0/0d/Title_screen_for_Netflix%27s_Dead_to_Me.png")  # noqa

session.add(item7)
session.commit()

item8 = Item(show="show", title="The Haunting of Hill House",
             description="supernational horror drama",
             release="2018",
             category=cat4,
             img="https://upload.wikimedia.org/wikipedia/en/9/92/The_Haunting_of_Hill_House.jpg")  # noqa

session.add(item8)
session.commit()

item9 = Item(show="show", title="Walking dead",
             description="zombie & human drama",
             release="2019",
             category=cat4,
             img="http://www.pngmart.com/files/4/TWD-PNG-Clipart.png")  # noqa

session.add(item9)
session.commit()

item10 = Item(show="show", title="Stranger things",
              description='''supernatural events occurring
              around fictional town in Indiana''',
              release="2019",
              category=cat5,
              img="https://upload.wikimedia.org/wikipedia/commons/3/38/Stranger_Things_logo.png")  # noqa
session.add(item10)
session.commit()

item11 = Item(show="movie", title="Snowpiercer",
              description="Story about survivors of Earth's second Ice Age",
              release="2013",
              category=cat5,
              img="https://upload.wikimedia.org/wikipedia/en/b/b4/Snowpiercer_poster.jpg")  # noqa

session.add(item11)
session.commit()
