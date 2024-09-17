# Ocean of Notions - Masterworks

Ocean of Notions is a Django-based web application designed for the Ocean of Notions Theatre Company's educational outreach program, Masterworks. This application allows educators to sign up, book workshops via a Stripe payment gateway, and cancel them. It is adaptable to fit into a preexisting company page or stand-alone. The user can also leave a review for the workshops they've booked.


![Masterworks PR Image](https://github.com/user-attachments/assets/85b55b80-db36-4d37-9f92-d81eb09e2147)


## Project Structure

[Link to Google Sheets Document](https://docs.google.com/spreadsheets/d/1-f6QfLams4WqlazBVoMkG_brbBXNDETeN_XpVoQlGNw/edit?usp=sharing)


## Setup Instructions

### Prerequisites

- Python 3.8+
- Django 3.2+
- Pip (Python package installer)

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/MarMarAgain/PP4MWV2.git
    cd PP4MWV2
    ```

2. **Create a virtual environment:**

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations:**

    ```sh
    python manage.py migrate
    ```

5. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

7. **Access the application:**

    Open your browser and navigate to `http://127.0.0.1:8000`.

## Application Overview

### UX Design File Guide

![UX Design File](https://github.com/MarMarAgain/PP4MWV2/assets/158588349/244ec22b-6065-441a-a7aa-ef302ef15138)

### Accounts

The `accounts` app manages user registration, login, and profile management.

- **models.py**: Defines the user profile model.
- **forms.py**: Contains the forms for user registration and profile editing.
- **views.py**: Handles user registration, login, logout, and profile editing views.
- **urls.py**: URL configurations for account-related routes.
- **templates**: Contains templates for registration, login, and profile management.

### Purchase

The `bookings` app handles workshop bookings and cancellations.

- **models.py**: Defines the booking and workshop models.
- **views.py**: Manages the booking and cancellation logic.
- **urls.py**: URL configurations for booking-related routes.
- **templates**: Contains templates for booking-related pages.


### Workshops

The `workshops` app manages the workshop details, scheduling, and booking records.

- **models.py**: Defines the workshop, workshop date-time, and booking models.
- **views.py**: Handles views related to displaying and managing workshops.
- **urls.py**: URL configurations for workshop-related routes.
- **templates**: Contains templates for workshop-related pages.
  
### Other_Pages
This app currently holds very little but will be utilised more as the website develops

### Static Files

The `static` directory contains CSS, JavaScript, and image files used in the application.

### Templates

The `templates` directory contains HTML templates used in the application. Key templates include:

- **base.html**: Base template that other templates extend.
- **landing_page.html**: Homepage template.
- **signup.html**: User registration template.
- **login.html**: User login template.
- **password_reset.html**: Password reset template.
- **edit_profile.html**: User profile editing template.
- **workshop_detail.html**: Workshop details template.

## Deployment

### Using Heroku

1. **Login to Heroku:**

    ```sh
    heroku login
    ```

2. **Create a new Heroku app:**

    ```sh
    heroku create ocean-of-notions
    ```

3. **Add the Heroku remote:**

    ```sh
    git remote add heroku https://git.heroku.com/ocean-of-notions.git
    ```

4. **Deploy the application:**

    ```sh
    git push heroku main
    ```

5. **Run database migrations on Heroku:**

    ```sh
    heroku run python manage.py migrate
    ```

6. **Create a superuser on Heroku:**

    ```sh
    heroku run python manage.py createsuperuser
    ```

7. **Open the Heroku app:**

    ```sh
    heroku open
    ```

## Usage

1. **Register a new user:**
   - Navigate to the signup page and create a new account.

2. **Login:**
   - Use the login page to access your account.

3. **Edit Profile:**
   - Edit your profile information through the profile page.

4. **Book a Workshop:**
   - Browse available workshops and book a spot.
   - Email confirmation is sent to put the admins email and the users.

5. **Cancel a Booking:**
   - Cancel your bookings through the booking management page.
   - Email confirmation is sent to put the admins email and the users.
     
6. **Review a Booking:**
    - Leave a review for workshops booked.
   - Edit review feature.
    
## Testing

[Link to Google Sheets Document](https://docs.google.com/spreadsheets/d/1r9aXE0g0vNQ3vZQkkfax04xow1b_Bp2MzG0Hmn-zru4/edit?usp=sharing)

## References

### Books

1. **Django for Beginners: Build websites with Python and Django**
   - Vincent, W. S. (2018). *Django for Beginners: Build websites with Python and Django*. Leanpub.
       - **Reference - Project Structure and Setup Instructions**

2. **Django 3 By Example**
   - Melendez, A. (2020). *Django 3 By Example*. Packt Publishing.
       - **Reference - accounts/models.py, forms.py, views.py, urls.py**

5. **Python Crash Course, 2nd Edition: A Hands-On, Project-Based Introduction to Programming**
   - Matthes, E. (2019). *Python Crash Course, 2nd Edition: A Hands-On, Project-Based Introduction to Programming*. No Starch Press.
       - **Reference - General Python code**

6. **The Definitive Guide to Django: Web Development Done Right**
   - Holovaty, A., & Kaplan-Moss, J. (2009). *The Definitive Guide to Django: Web Development Done Right*. Apress.
       - **Reference - models.py, views.py, urls.py, templates**

### Online Resources

1. **Django Documentation**
   - Django Software Foundation. (n.d.). Django documentation. Retrieved from https://docs.djangoproject.com/en/stable/
       - **Reference - Project Structure, Setup Instructions, models.py, views.py, urls.py, templates**

2. **Mozilla Developer Network (MDN) Django Tutorial**
   - Mozilla Developer Network. (n.d.). Django Web Framework (Python). Retrieved from https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django
       - **Reference - General Django development**

4. **Django REST Framework**
   - Django REST Framework. (n.d.). Django REST framework. Retrieved from https://www.django-rest-framework.org/
       - **Reference - Adding API functionality (future feature)**

5. **Heroku: Deploying Django Apps**
   - Heroku. (n.d.). Deploying Django Apps on Heroku. Retrieved from https://devcenter.heroku.com/articles/deploying-python
       - **Reference - Deployment**

6. **Django Packages**
   - Django Packages. (n.d.). Django Packages. Retrieved from https://djangopackages.org/
       - **Reference - Enhancing project with additional packages**

### Corresponding References to Project Code

- **Project Structure and Setup Instructions**
  - Vincent, W. S. (2018). *Django for Beginners: Build websites with Python and Django*. Leanpub.
  - Melendez, A. (2020). *Django 3 By Example*. Packt Publishing.
  - Django Software Foundation. (n.d.). Django documentation. Retrieved from https://docs.djangoproject.com/en/stable/

- **General Django development**
  - Mozilla Developer Network. (n.d.). Django Web Framework (Python). Retrieved from https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django

- **accounts/models.py, forms.py, views.py, urls.py**
  - Melendez, A. (2020). *Django 3 By Example*. Packt Publishing.
  - Greenfeld, D. R., & Greenfeld, A. R. (2019). *Two Scoops of Django 3.x: Best Practices for the Django Web Framework*. Two Scoops Press.
  - Real Python. (n.d.). Django Tutorials. Retrieved from https://realpython.com/tutorials/django/

- **General Python code**
  - Matthes, E. (2019). *Python Crash Course, 2nd Edition: A Hands-On, Project-Based Introduction to Programming*. No Starch Press.

- **models.py, views.py, urls.py, templates**
  - Holovaty, A., & Kaplan-Moss, J. (2009). *The Definitive Guide to Django: Web Development Done Right*. Apress.




