from flask import Blueprint, render_template, redirect, flash, request, session, url_for
from . import db
from .models import Budget, Expense, Users
from .forms import ForgotForm, LoginForm, SignUpForm
from flask_login import current_user, login_user,login_required,logout_user

auth = Blueprint('auth', __name__)

@auth.route('/signin', methods=['GET', 'POST'])
def login():
    signin_form = LoginForm()
    signup_form = SignUpForm()
    if signin_form.validate_on_submit():
        email = signin_form.email.data
        password = signin_form.password.data
        user = Users.query.filter_by(email=email).first()  
        if user and user.password == password:  # Directly check password
            session['id'] = user.id  # Store user ID in session
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('views.home'))  # Ensure this matches your home route
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', signin_form=signin_form, signup_form=signup_form)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    signin_form = LoginForm()
    signup_form = SignUpForm()
    if signup_form.validate_on_submit():
        email = signup_form.email.data
        name = signup_form.name.data
        password = signup_form.password.data
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please choose a different one.', 'danger')
            return render_template('login.html', signin_form=signin_form)

        new_user = Users(email=email, name=name, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect('/signin')
    return render_template('login.html', signin_form=signin_form, signup_form=signup_form)

@auth.route('/logout', methods=['POST'])
@login_required
def log_out():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/forgot', methods=['GET', 'POST'])
def forgot():
    forgot_form = ForgotForm()
    
    if forgot_form.validate_on_submit():
        email = forgot_form.email.data
        new_password = forgot_form.password.data
        confirm_password = forgot_form.confirmPassword.data
        
        # Check if both password fields match
        if new_password != confirm_password:
            flash("Passwords do not match. Please try again.", "danger")
            return render_template('forgot.html', forgot_form=forgot_form)

        # Logic to handle password reset (find user by email and update password in the database)
        user = Users.query.filter_by(email=email).first()
        if user:
            user.password = new_password  # Assuming no password hashing
            db.session.commit()  # Commit the password update
            flash("Your password has been reset successfully!", "success")
            return redirect(url_for('auth.signin'))
        else:
            flash("No account found with that email address.", "danger")
            return render_template('forgot.html', forgot_form=forgot_form)

    return render_template('forgot.html', forgot_form=forgot_form)




@auth.route('/change_password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not current_user.check_password(current_password):
        flash("Current password is incorrect", "danger")
        return redirect(url_for('views.profile'))

    if new_password != confirm_password:
        flash("New passwords do not match", "danger")
        return redirect(url_for('views.profile'))

    current_user.set_password(new_password)
    db.session.commit()

    flash("Password successfully updated", "success")
    return redirect(url_for('views.profile'))


@auth.route('/add_expense/<int:budget_id>', methods=['POST'])
@login_required
def add_expense(budget_id):
    budget = Budget.query.get_or_404(budget_id)

    # Check if the current user is the owner of the budget
    if budget.user_id != current_user.id:
        flash("You are not authorized to add expenses to this budget.", "danger")
        return redirect(url_for('auth.view_budget', budget_id=budget_id))

    # Retrieve form data
    expense_name = request.form.get('expense_name')
    expense_amount = request.form.get('expense_amount')

    # Validate form inputs
    if not expense_name or not expense_amount:
        flash("Expense name and amount are required.", "danger")
        return redirect(url_for('auth.view_budget', budget_id=budget_id))

    try:
        expense_amount = float(expense_amount)
        if expense_amount <= 0:  # Ensure the amount is positive
            raise ValueError("Amount must be a positive number.")
    except ValueError:
        flash("Please enter a valid positive amount.", "danger")
        return redirect(url_for('auth.view_budget', budget_id=budget_id))

    # Add the new expense to the database
    new_expense = Expense(budget_id=budget.id, name=expense_name, amount=expense_amount)
    db.session.add(new_expense)
    db.session.commit()
    flash("Expense added successfully!", "success")

    return redirect(url_for('auth.view_budget', budget_id=budget_id))

@auth.route('/view_budget/<int:budget_id>', methods=['GET', 'POST'])
@login_required
def view_budget(budget_id):
    # Get the specified budget or return a 404 if not found
    budget = Budget.query.get_or_404(budget_id)

    # Check if the current user is the owner of the budget
    if budget.user_id != current_user.id:
        flash("You are not authorized to view this budget.", "danger")
        return redirect(url_for('views.home'))

    # Get all expenses associated with the budget
    expenses = Expense.query.filter_by(budget_id=budget_id).all()

    # Fetch all budgets for the current user to show in the dropdown
    previous_budgets = Budget.query.filter_by(user_id=current_user.id).all()

    # Check if a previous budget is selected from the dropdown
    selected_budget_id = request.args.get('previous_budget', type=int)
    if selected_budget_id:
        budget = Budget.query.get_or_404(selected_budget_id)
        expenses = Expense.query.filter_by(budget_id=selected_budget_id).all()

    # Render the view_budget template with budget and expenses
    return render_template('view_budget.html', budget=budget, expenses=expenses, previous_budgets=previous_budgets)



@auth.route('/create_budget', methods=['GET', 'POST'])
@login_required
def create_budget():
    if request.method == 'POST':
        trip_name = request.form.get('trip_name')  # Use trip_name instead of budget_name
        total_budget = request.form.get('total_budget')  # Use total_budget instead of budget_amount

        # Validate inputs
        if not trip_name or not total_budget:
            flash("Trip name and total budget are required.", "danger")
            return redirect(url_for('auth.create_budget'))

        try:
            total_budget = float(total_budget)
            if total_budget <= 0:
                raise ValueError("Total budget must be a positive number.")
        except ValueError:
            flash("Please enter a valid positive amount for the budget.", "danger")
            return redirect(url_for('auth.create_budget'))

        # Create a new budget
        new_budget = Budget(user_id=current_user.id, trip_name=trip_name, total_budget=total_budget)
        db.session.add(new_budget)
        db.session.commit()
        flash("Budget created successfully!", "success")
        return redirect(url_for('auth.view_budget', budget_id=new_budget.id))

    return render_template('create_budget.html')  # Render your budget creation form


@auth.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    # Check if the current user is the owner of the expense
    if expense.budget.user_id != current_user.id:
        flash("You are not authorized to edit this expense.", "danger")
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        # Update the expense with the form data
        expense.name = request.form['expense_name']
        expense.amount = request.form['expense_amount']
        db.session.commit()
        flash("Expense updated successfully.", "success")
        return redirect(url_for('auth.view_budget', budget_id=expense.budget.id))

    return render_template('edit_expense.html', expense=expense)

