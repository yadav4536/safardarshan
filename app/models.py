from . import db
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def get_id(self):
        return str(self.id)
    
    def check_password(self, password):
        return self.password == password
    
    def set_password(self, password):
        self.password = password




class Places(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(400), nullable=False, unique=True)
    city = db.Column(db.String(400), nullable=False)
    description = db.Column(db.String(900))
    pictures = db.Column(db.String(1000), nullable=False)  # Store comma-separated URLs
    location = db.Column(db.String(1000))  # Store the location URL (e.g., Google Maps link)
    category = db.Column(db.String(400), default="place")  # Automatically set category to "place"
    added_at = db.Column(db.DateTime, default=db.func.now())


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(400), nullable=False, unique=True)
    state = db.Column(db.String(400), nullable=False)  # State field added
    description = db.Column(db.String(900))
    pictures = db.Column(db.String(1000), nullable=False)  # Store comma-separated URLs
    location = db.Column(db.String(1000))  # Store the location URL (e.g., Google Maps link)
    category = db.Column(db.String(400), default="city")  # Automatically set category to "city"
    added_at = db.Column(db.DateTime, default=db.func.now())

    @hybrid_property
    def total_destinations(self):
        """
        This property calculates the total number of matching destinations
        across the Restaurant, Hotel, and Places tables based on the 'destination' column.
        """
        restaurant_count = db.session.query(Restaurant).filter_by(city=self.destination).count()
        hotel_count = db.session.query(Hotel).filter_by(city=self.destination).count()
        places_count = db.session.query(Places).filter_by(city=self.destination).count()

        # Return the sum of all destinations
        return restaurant_count + hotel_count + places_count


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(400), nullable=False)
    description = db.Column(db.String(900))
    city = db.Column(db.String(400), nullable=False)
    pictures = db.Column(db.String(1000), nullable=False)  # Store comma-separated URLs
    location = db.Column(db.String(1000))  # Store the location URL (e.g., Google Maps link)
    category = db.Column(db.String(400), default="restaurant")  # Automatically set category to "restaurant"
    added_at = db.Column(db.DateTime, default=db.func.now())


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(400), nullable=False)
    city = db.Column(db.String(400), nullable=False)
    description = db.Column(db.String(900))
    pictures = db.Column(db.String(1000), nullable=False)  # Store comma-separated URLs
    location = db.Column(db.String(1000))  # Store the location URL (e.g., Google Maps link)
    category = db.Column(db.String(400), default="hotel")  # Automatically set category to "hotel"
    added_at = db.Column(db.DateTime, default=db.func.now())


class Favorite(db.Model):
    

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # This should match categories in your items
    added_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, user_id, item_id, category):
        self.user_id = user_id
        self.item_id = item_id
        self.category = category

    __table_args__ = (
        db.UniqueConstraint('user_id', 'item_id', 'category', name='unique_favorite_constraint'),  # Renamed for clarity
    )

    def __repr__(self):
        return f'<Favorite(user_id={self.user_id}, item_id={self.item_id}, category={self.category})>'
    




class Budget(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trip_name = db.Column(db.String(255), nullable=False)
    total_budget = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # Relationship with Expense
    expenses = db.relationship('Expense', backref='budget', lazy=True, cascade="all, delete-orphan")

    @hybrid_property
    def total_expenses(self):
        return sum(expense.amount for expense in self.expenses)

    @hybrid_property
    def remaining_budget(self):
        return self.total_budget - self.total_expenses

    def add_expense(self, expense_name, amount):
        new_expense = Expense(budget_id=self.id, name=expense_name, amount=amount)
        db.session.add(new_expense)
        db.session.commit()


class Expense(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    added_at = db.Column(db.DateTime, default=db.func.now())