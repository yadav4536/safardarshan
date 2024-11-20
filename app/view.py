from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from . import db 
from flask_mail import Message
from . import mail  # Import mail from your app
from .models import  Budget, City, Hotel, Places, Restaurant

views = Blueprint('views', __name__)

@views.route('/')
def home():
    # Query all cities from the database
    cities = City.query.all()  
    city_data = [
        {
            'destination': city.destination,
            'description': city.description,
            'pictures': city.pictures.split(','),  # Split comma-separated pictures
            'location': city.location,
            'total_destinations': city.total_destinations,
        } for city in cities
    ]

    # Get all places for featured destinations
    featured_places = Places.query.all()  
    places_data = [
        {
            'destination': place.destination,
            'city': place.city,
            'description': place.description,
            'pictures': place.pictures.split(','),  # Split comma-separated pictures
            'location': place.location,
        } for place in featured_places
    ]

    # Get all restaurants
    featured_restaurants = Restaurant.query.all()  
    restaurant_data = [
        {
            'destination': restaurant.destination,
            'city': restaurant.city,
            'description': restaurant.description,
            'pictures': restaurant.pictures.split(','),  # Split comma-separated pictures
            'location': restaurant.location,
        } for restaurant in featured_restaurants
    ]

    # Get all hotels
    featured_hotels = Hotel.query.all()  
    hotel_data = [
        {
            'destination': hotel.destination,
            'city': hotel.city,
            'description': hotel.description,
            'pictures': hotel.pictures.split(','),  # Split comma-separated pictures
            'location': hotel.location,
        } for hotel in featured_hotels
    ]

    # Define categories
    categories = [
        {'id': 'restaurants', 'name': 'Restaurants'},
        {'id': 'hotels', 'name': 'Hotels'},
        {'id': 'places', 'name': 'Destinations'}
    ]

    city_count = City.query.count()  # Count the number of cities
    destination_count = Places.query.count()  # Count the number of destinations
    hotel_count = Hotel.query.count()  # Count the number of hotels
    restaurant_count = Restaurant.query.count()  # Count the number of restaurants



    user_budget = Budget.query.filter_by(user_id=current_user.id).first() if current_user.is_authenticated else None
    
   

   
    
    # Return all data to the template
    return render_template('index.html', 
                           cities=city_data, 
                           places=places_data, 
                           restaurants=restaurant_data, 
                           hotels=hotel_data, 
                           categories=categories, city_count=city_count, destination_count=destination_count, hotel_count=hotel_count, restaurant_count=restaurant_count, user_budget=user_budget)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@views.route('/about')
def about():
    city_count = City.query.count()  # Count the number of cities
    destination_count = Places.query.count()  # Count the number of destinations
    hotel_count = Hotel.query.count()  # Count the number of hotels
    restaurant_count = Restaurant.query.count()  # Count the number of restaurants
    team_members = ["Himanshu Yadav", "Kshitij Srivastva", "Adrija Maurya", "Khushbu Verma"]
    linkedin_urls=["https://www.linkedin.com/in/himanshu-yadav-400a38256/","https://www.linkedin.com/in/kshitij-srivastava-071617216/","https://www.linkedin.com/in/adrija-maurya-4180a7294","https://www.linkedin.com/in/khushbu-verma-500872293/"]
    return render_template('about.html' ,city_count=city_count, destination_count=destination_count, hotel_count=hotel_count, restaurant_count=restaurant_count,team_members=team_members,linkedin_urls=linkedin_urls)


@views.route('/contact')
@login_required
def contact():
    return render_template('contact.html')


# Route for handling form submission
@views.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Compose the email
        msg = Message(subject=subject,
                      sender=email,
                      recipients=['deepuyadav8276@gmail.com'])  # Your email to receive the contact form details
        msg.body = f"Message from {name} ({email}):\n\n{message}"

        try:
            mail.send(msg)  # Send the email using Flask-Mail
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send message. Error: {str(e)}', 'danger')

        return redirect(url_for('views.contact'))

    return render_template('contact.html')


@views.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query', '')
    results = {
        'cities': [],
        'restaurants': [],
        'hotels': [],
        'places': [],
    }

    if query:
        # Normalize the query to handle case-insensitive matching
        query_lower = query.lower()

        # Check if the query matches a city name first
        cities = City.query.filter(City.destination.ilike(f'%{query_lower}%')).all()
        if cities:
            results['cities'] = cities
            # If a specific city is found, also fetch related hotels, restaurants, and places
            city_names = [city.destination for city in cities]
            results['restaurants'] = Restaurant.query.filter(Restaurant.city.in_(city_names)).all()
            results['hotels'] = Hotel.query.filter(Hotel.city.in_(city_names)).all()
            results['places'] = Places.query.filter(Places.city.in_(city_names)).all()
        else:
            # If no specific city is found, perform general searches
            results['restaurants'] = Restaurant.query.filter(Restaurant.destination.ilike(f'%{query_lower}%')).all()
            results['hotels'] = Hotel.query.filter(Hotel.destination.ilike(f'%{query_lower}%')).all()
            results['places'] = Places.query.filter(Places.destination.ilike(f'%{query_lower}%')).all()
            results['cities'] = City.query.filter(City.destination.ilike(f'%{query_lower}%')).all()  # To search cities too

    return render_template('search_results.html', **results, query=query)



@views.route('/suggestions', methods=['GET'])
def suggestions():
    query = request.args.get('query', '').lower()  # Get the query from the URL
    results = {
        "cities": City.query.filter(City.destination.ilike(f'%{query}%')).all(),
        "restaurants": Restaurant.query.filter(Restaurant.destination.ilike(f'%{query}%')).all(),
        "hotels": Hotel.query.filter(Hotel.destination.ilike(f'%{query}%')).all(),
        "places": Places.query.filter(Places.destination.ilike(f'%{query}%')).all()
    }

    # Format the results to send back as JSON
    suggestions = {
        "cities": [city.destination for city in results["cities"]],
        "restaurants": [restaurant.destination for restaurant in results["restaurants"]],
        "hotels": [hotel.destination for hotel in results["hotels"]],
        "places": [place.destination for place in results["places"]],
    }

    return jsonify(suggestions)




@views.route('/search_advanced', methods=['GET'])
def search_advanced():
    selected_city = request.args.get('city', '').strip()
    selected_category = request.args.get('category', '').strip()

    results = []
    title = "Search Results"

    # Filter based on the selected city and category
    if selected_city and selected_category:
        if selected_category == 'restaurants':
            results = Restaurant.query.filter_by(city=selected_city).all()
            title += f" - Restaurants in {selected_city}"
        elif selected_category == 'hotels':
            results = Hotel.query.filter_by(city=selected_city).all()
            title += f" - Hotels in {selected_city}"
        elif selected_category == 'places':
            results = Places.query.filter_by(city=selected_city).all()
            title += f" - Destinations in {selected_city}"
    elif selected_city:
        # Filter by city only
        results = Restaurant.query.filter_by(city=selected_city).all() + \
                  Hotel.query.filter_by(city=selected_city).all() + \
                  Places.query.filter_by(city=selected_city).all()
        title += f" - All Categories in {selected_city}"
    elif selected_category:
        # Filter by category only
        if selected_category == 'restaurants':
            results = Restaurant.query.all()
            title += " - All Restaurants"
        elif selected_category == 'hotels':
            results = Hotel.query.all()
            title += " - All Hotels"
        elif selected_category == 'places':
            results = Places.query.all()
            title += " - All Destinations"

    return render_template('search_advance.html', results=results, title=title)









@views.route('/explore/<category>')
@login_required
def explore(category):
    if category == 'destinations':
        places = get_destinations()  # Function to retrieve destinations data
        title = 'Featured Destinations'
    elif category == 'hotels':
        places = get_hotels()  # Function to retrieve hotels data
        title = 'Featured Hotels'
    elif category == 'restaurants':
        places = get_restaurants()  # Function to retrieve restaurants data
        title = 'Featured Restaurants'
    else:
        places = []  # Empty list if no valid category
        title = 'Explore'
    
    # Check if places are empty and handle it (optional)
    if not places:
        flash(f'No {category} found.', 'warning')

    return render_template('explore.html', places=places, title=title, category=category)



def get_destinations():
    # Get all places for featured destinations
    featured_places = Places.query.all()  
    places_data = []
    
    for place in featured_places:
        places_data.append({
            'destination': place.destination,
            'city': place.city,
            'description': place.description,
            'pictures': place.pictures.split(','),  # Split comma-separated pictures
            'location': place.location,
        })

    return places_data  # Return the data


def get_hotels():
    # Get all hotels
    featured_hotels = Hotel.query.all()  # Query all hotels
    hotel_data = []

    for hotel in featured_hotels:
        hotel_data.append({
            'destination': hotel.destination,
            'city': hotel.city,
            'description': hotel.description,
            'pictures': hotel.pictures.split(','),  # Split comma-separated pictures
            'location': hotel.location,
        })

    return hotel_data  # Return the data


def get_restaurants():
    # Get all restaurants
    featured_restaurants = Restaurant.query.all()  # Query all restaurants
    restaurant_data = []

    for restaurant in featured_restaurants:
        restaurant_data.append({
            'destination': restaurant.destination,
            'city': restaurant.city,
            'description': restaurant.description,
            'pictures': restaurant.pictures.split(','),  # Split comma-separated pictures
            'location': restaurant.location,
        })

    return restaurant_data  # Return the data




