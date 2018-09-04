#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Base, Item, User

engine = create_engine('sqlite:///catalogWithOAuth.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Items for Milk substitutes
category1 = Category(name="Milk Substitutes")

session.add(category1)
session.commit()

item1 = Item(user_id=1, title="Hemp Milk", description="Hemp milk is a complete protein that contains all of the amino acids necessary for optimal health.",
                     category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, title="Soy Milk", description="Soy milk has a nutrition profile most similar to dairy milk.",
                     category=category1)

session.add(item2)
session.commit()

item3 = Item(user_id=1, title="Almond Milk", description="Almond milk tends to be lower in calories and sugar than most non-dairy milk. It also contains monounsaturated fats, which are heart healthy fats. Almond milk tends to separate when heated so it may separate in coffee.",
                     category=category1)

session.add(item3)
session.commit()

item4 = Item(user_id=1, title="Cashew Milk", description="Cashew milk is the new kid on the block. It is creamy and sweet but can be high in sugar. Make sure you go for unsweetened.",
                     category=category1)

session.add(item4)
session.commit()

item5 = Item(user_id=1, title="Rice Milk", description="Rice milk is non-allergenic. However, it is the lowest in protein and tends to be higher in sugar and calories. Always use unsweetened.",
                     category=category1)

session.add(item5)
session.commit()

item6 = Item(user_id=1, title="Oat Milk", description="Oat milk provides fiber as well as protein about 4 grams per serving. However, it is on the higher end in terms of sugar and calories.",
                     category=category1)

session.add(item6)
session.commit()

# Items for Butter substitutes
category2 = Category(name="Butter Substitutes")

session.add(category2)
session.commit()

item1 = Item(user_id=1, title="Earth Balance", description="Earth Balance is popular and makes lots of vegan butter options.",
                     category=category2)

session.add(item1)
session.commit()

item2 = Item(user_id=1, title="It's Vegan", description="With an irresistibly creamy taste you'll love, it's 100% non-dairy, Vegan Action Certified and made from the goodness of plants.",
                     category=category2)

session.add(item2)
session.commit()

item3 = Item(user_id=1, title="Miyokos Creamery", description="Cultured vegan butter made with organic coconut oil, this culinary game-changer brings plant-based buttery goodness to your morning toast & beyond.",
                     category=category2)

session.add(item3)
session.commit()

# Items for Cheese substitutes
category3 = Category(name="Cheese Substitutes")

session.add(category3)
session.commit()

item1 = Item(user_id=1, title="Daiya Mozzarella Shreds", description="Dairy-free Mozzarella Style Shreds melt, ooze, bubble and stretch - just like regular mozzarella cheese.",
                     category=category3)

session.add(item1)
session.commit()

item2 = Item(user_id=1, title="Daiya Cheddar Slices", description="Dairy-free Cheddar Style Slices can better any burger, sandwich or afternoon snack. ",
                     category=category3)

session.add(item2)
session.commit()

# Items for Egg substitutes
category4 = Category(name="Egg Substitutes")

session.add(category4)
session.commit()

item1 = Item(user_id=1, title="Ground Flax Seed", description="Makes two eggs - Whisk two tablespoons of ground flax seed with six tablespoons of water until fluffy - put the mixture in the refrigerator for 10 minutes to thicken.",
                     category=category4)

session.add(item1)
session.commit()

item2 = Item(user_id=1, title="Aquafaba", description="Aquafaba is the liquid from cooked chickpeas. Three tablespoons equals 1 egg white. Two tablespoons of aquafaba equals one egg as a binder.",
                     category=category4)

session.add(item2)
session.commit()

item3 = Item(user_id=1, title="Chickpea Flour", description="Makes one egg - Whisk three tablespoons of Chickpea flour with three tablespoons of water.",
                     category=category4)

session.add(item3)
session.commit()

item4 = Item(user_id=1, title="Tofu", description="For two eggs - blend 1/4 cup silken tofu until tofu is smooth and creamy.",
                     category=category4)

session.add(item4)
session.commit()

item5 = Item(user_id=1, title="Arrowroot", description="Makes one egg - Combine two tablespoons of Arrowroot with three tablespoons of water.",
                     category=category4)

session.add(item5)
session.commit()

# Items for Meat substitutes
category5 = Category(name="Meat Substitutes")

session.add(category5)
session.commit()

item1 = Item(user_id=1, title="Gardein chick'n strips", description="There's no guilt with these easy, delicious, and crispy chick'n strips. Everyone likes to skinny dip!",
                     category=category5)

session.add(item1)
session.commit()

item2 = Item(user_id=1, title="Gardein turk'y cutlet", description="Tender cutlets wrapped in crunchy breading is the start of a delicious meal!",
                     category=category5)

session.add(item2)
session.commit()

item3 = Item(user_id=1, title="Gardein beefless tips", description="Dine in and keep the tip...just saute and add to anything you've got going!",
                     category=category5)

session.add(item3)
session.commit()

item4 = Item(user_id=1, title="Gardein szechuan beefless strips", description="Add these easily to any meal - and they'll be asking for more.",
                     category=category5)

session.add(item4)
session.commit()

item5 = Item(user_id=1, title="Beyond Meat Burger", description="The Beyond Burger is the world's first plant-based burger that looks, cooks, and tastes like a fresh beef burger. It has all the juicy, meat deliciousness of a traditional burger, but comes with the upsides of a plant-based meal.",
                     category=category5)

session.add(item5)
session.commit()

item6 = Item(user_id=1, title="Tofurky Italian Sausage", description="A Tofurky fan favorite, our Italian sausages stand out with flavors of fragrant basil and sweet sun-dried tomatoes. They bring a smile to spaghetti, soups and sautes.",
                     category=category5)

session.add(item6)
session.commit()

item7 = Item(user_id=1, title="Tofurky Feast", description="Tailgate partiers, trick-or-treaters and the Tooth Fairy are all in agreement: if you do something twice in a row, it's officially a tradition. We've been serving up Tofurky Roasts since 1995, so we're well-versed in the fine art of the meat-free main dish. If this is your first Tofurky Roast dinner, congratulations - you're halfway to a brand new tradition.",
                     category=category5)

session.add(item7)
session.commit()

item8 = Item(user_id=1, title="Tofurky Oven Roasted Deli Slices", description="Keep the day-after-Thanksgiving refrigerator raid going all year round. These deli slices are made from the same delicious recipe as the Holiday Tofurky Roast.",
                     category=category5)

session.add(item8)
session.commit()

item9 = Item(user_id=1, title="Tofurky Thai Basil Slow Roasted Chick'n", description="This bright, vibrant and aromatic Thai-basil chick'n can be seared, steamed, or tossed cold with your favorite crisp veggies.",
                     category=category5)

session.add(item9)
session.commit()

# Items for Desserts & Ice Cream
category6 = Category(name="Desserts & Ice Cream")

session.add(category6)
session.commit()

item1 = Item(user_id=1, title="Ben & Jerry's Coconut Seven Layer Bar", description="Coconut non-dairy ice cream with fudge chunks, walnuts & swirls of graham cracker & caramel.",
                     category=category6)

session.add(item1)
session.commit()

item2 = Item(user_id=1, title="Haagen-Dazs Chocolate Salted Fudge Truffle", description="Rich Belgian chocolate is blended with swirls of sweet salted fudge and chunks of fudge truffles to create an incredible non-dairy indulgence that isn't missing a thing.",
                     category=category6)

session.add(item2)
session.commit()

item3 = Item(user_id=1, title="Trader Joe's Organic Soy Creamy", description="Trader Joe's lineup of vanilla frozen treat options is this flavor that's great for vegans and those with dairy sensitivities. The 'creamy' in the name is no misnomer. Despite the lack of dairy, this flavor will blow you away in the texture department.",
                     category=category6)

session.add(item3)
session.commit()

item4 = Item(user_id=1, title="So Delicious Chocolate Drizzled Bananas Foster", description="Inspired by the classic, enjoy this banana-vanilla-chocolate chip sensation that's making a comeback. Or did it ever go away? Perfectly paired with our cashewmilk frozen dessert.",
                     category=category6)

session.add(item4)
session.commit()

item5 = Item(user_id=1, title="So Delicious Very Vanilla", description="Rich, creamy & totally indulgent!",
                     category=category6)

session.add(item5)
session.commit()

item6 = Item(user_id=1, title="So Delicious Salted Caramel Cluster", description="A sweet and salty delight featuring chocolate covered cashews and a ribbon of salted caramel.",
                     category=category6)

session.add(item6)
session.commit()

item7 = Item(user_id=1, title="So Delicious Snickerdoodle", description="A cinnamon delight loaded with chunks of gluten-free snickerdoodle cookie dough!",
                     category=category6)

session.add(item7)
session.commit()

item8 = Item(user_id=1, title="So Delicious Peachy Maple Pecan", description="Get ready for the flavor experience of Non-GMO Project Verified peaches, pecans and maple syrup, matched with our cashewmilk frozen dessert. Peach out, everybody.",
                     category=category6)

session.add(item8)
session.commit()

item9 = Item(user_id=1, title="Breyers Vanilla Peanut Butter", description="Real Vanilla and luscious peanut butter collide to create this completely non-dairy dessert from Breyers. Made with real almond milk. Try it today!",
                     category=category6)

session.add(item9)
session.commit()

item10 = Item(user_id=1, title="Breyers Oreo", description="Non-Dairy OREO cookies and cream flavor frozen dessert from Breyers is made with creamy vanilla almond milk and filled with delicious OREO cookies.",
                     category=category6)

session.add(item10)
session.commit()

item11 = Item(user_id=1, title="Tofutti", description="Tofutti has been offering us vegan ice creams, and ice cream treats for decades. Their cutie ice cream sandwiches are a favorite. Their ice cream comes in vanilla, chocolate, and vanilla almond bark.",
                     category=category6)

session.add(item11)
session.commit()

item12 = Item(user_id=1, title="Dream", description="The soy based ice cream has Butter Pecan, Vanilla Fudge Swirl, and French Vanilla. Their Almond milk ice cream includes cappuccino swirl, chocolate, praline crunch, vanilla, strawberry, mint chocolate chip, and toffee almond fudge.",
                     category=category6)

session.add(item12)
session.commit()

# Items for Condiments
category7 = Category(name="Condiments")

session.add(category7)
session.commit()

item1 = Item(user_id=1, title="Vegenaise", description="Made with non-GMO, expeller-pressed Canola oil, low in saturated fats and high in essential omega-3 fatty acids!",
                     category=category7)

session.add(item1)
session.commit()

item2 = Item(user_id=1, title="Hellmann's Vegan Dressing", description="Hellmann's Vegan Dressing and Sandwich Spread is an excellent source of good fats, like Omega 3-ALA (contains 771mg of Omega-3 per serving, which is 44% of the 1.6g Daily Value for ALA), and is also gluten-free and certified kosher. It's the ideal condiment for spreading on sandwiches and wraps, grilling juicy burgers, baking flavorful fish, mixing creamy dips, and preparing fresh salads.",
                     category=category7)

session.add(item2)
session.commit()

item3 = Item(user_id=1, title="Just Mayo", description="Just Mayo is an egg-free mayonnaise substitute produced by JUST, Inc, formerly known as Hampton Creek. Just Mayo was first released in Northern California Whole Foods Markets on September 19, 2013.",
                     category=category7)

session.add(item3)
session.commit()

# Items for Sweeteners
category8 = Category(name="Sweeteners")

session.add(category8)
session.commit()

# Done
print "Added category items!"
