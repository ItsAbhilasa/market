from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask import flash
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://abhilasa:Yp7MrmnmOD6PqxyPRz4dnYsiQJXGDZJV@dpg-cqn4be5svqrc73fj6gtg-a.singapore-postgres.render.com/farm_market'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_farmer = db.Column(db.Boolean, nullable=False, default=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

class FarmerProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('farmer_products', lazy=True))
    user = db.relationship('User', backref=db.backref('farmer_products', lazy=True))



def create_sample_products():
    # Clear existing products and farmer products
    FarmerProduct.query.delete()
    Product.query.delete()
    db.session.commit()
    
    if Product.query.count() == 0:  # Check if there are no products
        products = [
            Product(name='Tomatoes', description='Fresh tomatoes from local farms.', price=20.0, image_url='https://th.bing.com/th/id/OIP.D6DpwoKh5XpTFczoQMufWgHaE8?rs=1&pid=ImgDetMain'),
            Product(name='Potatoes', description='High-quality potatoes.', price=30.0, image_url='https://cdn.britannica.com/89/170689-131-D20F8F0A/Potatoes.jpg'),
            # Product(name='Onions', description='Organic onions.', price=25.0, image_url='https://th.bing.com/th/id/R.33f6743d97e30e79c7ad0d3e48378b74?rik=0CH3oq6EUax4XA&riu=http%3a%2f%2fultimateguidetoeverything.com%2fwp-content%2fuploads%2f2020%2f12%2fmain-9.jpg&ehk=CK89idXFgn8UIn%2bLnCUUIYI7ZUkHFqUp2R0FG%2fut4cE%3d&risl=&pid=ImgRaw&r=0'),
            # Product(name='Carrots', description='Fresh carrots from local farms.', price=15.0, image_url='https://th.bing.com/th/id/R.a9ef0d119dabb519015a099f658ea478?rik=Auh3oo9N79OrWw&riu=http%3a%2f%2fupload.wikimedia.org%2fwikipedia%2fcommons%2fe%2fe6%2fCarrots.JPG&ehk=iZMbeeC9Jw%2fUVl2K94d6KtzP3SzKbGIXkR%2faamHTNgU%3d&risl=1&pid=ImgRaw&r=0'),
            Product(name='Cabbage', description='Organic cabbage.', price=10.0, image_url='https://www.thespruceeats.com/thmb/vh3pzGIKw5gzZPRXbOLdeX-4-cE=/2127x1409/filters:fill(auto,1)/Headsofgreencabbage-5bfda38346e0fb00264606e3.jpg'),
            Product(name='Cucumbers', description='High-quality cucumbers.', price=12.0, image_url='https://a-z-animals.com/media/2023/02/shutterstock_1161733981.jpg'),
            Product(name='Bell Peppers', description='Fresh bell peppers.', price=35.0, image_url='https://th.bing.com/th/id/OIP.4eOhUsPuDthMIfBWb1smyAAAAA?rs=1&pid=ImgDetMain'),
            Product(name='Lettuce', description='Organic lettuce.', price=20.0, image_url='https://images.heb.com/is/image/HEBGrocery/000319391'),
            Product(name='Spinach', description='Fresh spinach.', price=22.0, image_url='https://www.theharvestkitchen.com/wp-content/uploads/2023/05/what-is-spinach.jpg'),
            # Product(name='Broccoli', description='Organic broccoli.', price=28.0, image_url='https://th.bing.com/th/id/R.5341184da71ddce835721e48ad4f528a?rik=STn8glO4uSvarA&riu=http%3a%2f%2fwww.rivieraproduce.eu%2fwp-content%2fuploads%2f2011%2f08%2fimage_riviera_broccoli.jpg&ehk=OO9GhzV02R8pftBLm%2f%2be4CUh04Jh42iw3FSx%2fyspa3M%3d&risl=&pid=ImgRaw&r=0'),
            Product(name='Zucchini', description='High-quality zucchini.', price=18.0, image_url='https://th.bing.com/th/id/OIP.S2ikkIRqccdatSZ7b01jEwHaE8?rs=1&pid=ImgDetMain'),
            Product(name='Eggplant', description='Fresh eggplant.', price=25.0, image_url='https://cdn.shopify.com/s/files/1/0451/1101/7626/products/longbrinjalseeds.jpg?v=1603434934'),
            Product(name='Pumpkin', description='Organic pumpkin.', price=40.0, image_url='https://th.bing.com/th/id/OIP.by4flJvXzGwYCP1c2pwzwgHaEK?rs=1&pid=ImgDetMain'),
            # Product(name='Garlic', description='Fresh garlic.', price=45.0, image_url='https://th.bing.com/th/id/R.1c58ff5f0048505999ca4b541861bb21?rik=DLwoO7ZKTAVYaw&riu=http%3a%2f%2fcdn.shopify.com%2fs%2ffiles%2f1%2f2550%2f8730%2farticles%2fgarlic-bulbs_1200x1200.jpg%3fv%3d1628788048&ehk=bwa6rLxkMEL%2fL%2bJLVWY%2bwxYdsgBP4nzwCL0cUdZ7DQ8%3d&risl=&pid=ImgRaw&r=0'),
            Product(name='Ginger', description='High-quality ginger.', price=50.0, image_url='https://www.tastingtable.com/img/gallery/12-varieties-of-culinary-ginger-explained/l-intro-1673555215.jpg'),
            # Product(name='Coriander', description='Fresh coriander.', price=5.0, image_url='https://th.bing.com/th/id/R.6738d10e092a95e935269cbd6d1077b7?rik=%2fyb29jJP4M%2bNxg&riu=http%3a%2f%2fupload.wikimedia.org%2fwikipedia%2fcommons%2f5%2f51%2fA_scene_of_Coriander_leaves.JPG&ehk=W0NDHDbowCM1ZTazJxz55VP4MlfGL7FNTbIQTYJf6cc%3d&risl=1&pid=ImgRaw&r=0'),
            Product(name='Mint', description='Organic mint.', price=7.0, image_url='https://www.thespruce.com/thmb/okicoeSuE7_m0okpcVNDyKZvQIg=/4726x3151/filters:fill(auto,1)/types-of-mint-5120608-hero-7a3d6d0f70034bcc967080a6d7118967.jpg'),
            Product(name='Basil', description='Fresh basil.', price=10.0, image_url='https://www.tasteofhome.com/wp-content/uploads/2020/05/GettyImages-858087300.jpg'),
            Product(name='Parsley', description='Organic parsley.', price=6.0, image_url='https://th.bing.com/th/id/OIP._NAaYGD08sEJbTWR5X4GEgHaE5?rs=1&pid=ImgDetMain'),
            # Product(name='Dill', description='Fresh dill.', price=8.0, image_url='https://th.bing.com/th/id/R.5a94e30379e67302dcd5f9e9d4720b23?rik=aNwoH4Ys5fVIZA&riu=http%3a%2f%2fnashsorganicproduce.com%2frecipes%2fwp-content%2fuploads%2f2013%2f04%2fdill-2.jpg&ehk=O%2fFgVu5bbPHo5q%2fKztHQRWqnfi26xY6LqNvaDKepW%2fE%3d&risl=&pid=ImgRaw&r=0')
        ]
        db.session.bulk_save_objects(products)
        db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_farmer = 'is_farmer' in request.form
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return render_template('register.html')
        
        # Create new user
        new_user = User(username=username, password=password, is_farmer=is_farmer)
        db.session.add(new_user)
        
        try:
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'An unexpected error occurred: {str(e)}', 'error')
        
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        
        if user:
            session['user_id'] = user.id
            session['is_farmer'] = user.is_farmer 
            if user.is_farmer:
                return redirect(url_for('add_product'))
            return redirect(url_for('products'))
    return render_template('login.html')

@app.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    farmer_products = FarmerProduct.query.filter_by(product_id=product_id).all()
    return render_template('product_detail.html', product=product, farmer_products=farmer_products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    if not user.is_farmer:
        return redirect(url_for('products'))
    
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        
        new_farmer_product = FarmerProduct(product_id=product_id, quantity=quantity, user_id=user.id)
        db.session.add(new_farmer_product)
        db.session.commit()
        
        return redirect(url_for('products'))
    
    all_products = Product.query.all()
    return render_template('add_product.html', products=all_products)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# with app.app_context():
    # db.drop_all()
    # db.create_all()
    # create_sample_products()

if __name__ == '__main__':
    app.run(debug=True, port=8080)
