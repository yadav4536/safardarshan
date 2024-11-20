import os
from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app
from flask_login import login_required
from . import db
from .models import City, Hotel, Places, Restaurant
from werkzeug.utils import secure_filename
from PIL import Image

admin = Blueprint('admin', __name__)

# Utility function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


@admin.route('/add_place', methods=['GET', 'POST'])
@login_required
def add_place():
    if request.method == 'POST':
        # Get form data
        category = request.form.get('category')
        destination = request.form.get('destination')
        description = request.form.get('description')
        location = request.form.get('location')

        # Get the state if the category is city, otherwise get the city
        state = request.form.get('state') if category == 'city' else None
        city = request.form.get('city') if category != 'city' else None

        # Handle image upload
        if 'pictures' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['pictures']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Open the image to check its dimensions
            img = Image.open(file)
            width, height = img.size

            # Determine the max dimensions and minimum dimension message based on category
            if category == 'city':
                min_dimensions = (600, 600)
                max_dimensions = (1500, 1994)
                dimension_message = 'For cities, the image dimensions should be at least 600x600 and a maximum of 1500x1994.'
            else:
                min_dimensions = (600, 600)
                max_dimensions = (1500, 1994)
                dimension_message = 'For other categories, the image dimension should be exactly 600x600.'

            # Check if the image is smaller than the minimum dimensions
            if width < min_dimensions[0] or height < min_dimensions[1]:
                flash(f"Image is too small. {dimension_message}")
                return redirect(request.url)

            # Resize the image if it exceeds the max dimensions
            if width > max_dimensions[0] or height > max_dimensions[1]:
                img.thumbnail(max_dimensions)  # Resize while maintaining aspect ratio

            # Save the image (resized or original)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            img.save(file_path)

            # Save the place data to the appropriate table based on the category
            if category == 'place':
                new_place = Places(destination=destination, description=description, pictures=filename, location=location, city=city)
                db.session.add(new_place)
            elif category == 'city':
                new_city = City(destination=destination, description=description, pictures=filename, location=location, state=state)
                db.session.add(new_city)
            elif category == 'restaurant':
                new_restaurant = Restaurant(destination=destination, description=description, pictures=filename, location=location, city=city)
                db.session.add(new_restaurant)
            elif category == 'hotel':
                new_hotel = Hotel(destination=destination, description=description, pictures=filename, location=location, city=city)
                db.session.add(new_hotel)

            # Commit to database
            db.session.commit()

            # Flash success message and redirect
            flash('New place added successfully!')
            return redirect(url_for('admin.add_place'))

    return render_template('add.html')  # Render the form again if not POST.
