# Ocean of Notions - Masterworks

Ocean of Notions is a Django-based web application designed for the Ocean of Notions Theatre Company's educational outreach program, Masterworks. This application allows educators to sign up, book workshops, and cancel them. It is adaptable to fit into a preexisting company page or stand-alone. Future features include real-time messaging between the company and their customers.

## Project Structure

The project structure is linked here : 


## Setup Instructions

### Prerequisites

- Python 3.8+
- Django 3.2+
- Pip (Python package installer)

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/ocean-of-notions.git
    cd ocean-of-notions
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
- **landing_page.html**: Homepage template. (There is a home.html, and while that has a few links, it's not used).
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

## Testing

A link to the table detailing the validations can be found here : 





