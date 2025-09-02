# To-Do List - Django Task Manager

A simple yet powerful To-Do List application built with Django. This project allows users to manage their daily tasks through a clean and intuitive web interface. It includes features for creating, updating, deleting, and filtering tasks, as well as a weekly schedule view to visualize tasks by day and time.

## ✨ Features

-   **User Authentication:** Secure user registration and login system.
-   **Task Management (CRUD):** Create, Read, Update, and Delete tasks.
-   **Task Filtering:** Filter tasks by their status (pending, completed, overdue) and priority (high, medium, low).
-   **Dynamic Status Updates:** Task statuses automatically update to "overdue" if the deadline passes.
-   **AJAX-Powered Quick Complete:** Mark tasks as complete or pending directly from the list view without a full page reload.
-   **Weekly Schedule View:** A visual calendar to see scheduled tasks for the week.
-   **Responsive Design:** A clean and user-friendly interface that works on different devices.

## 🛠️ Technologies Used

-   **Backend:** [Python](https://www.python.org/) with the [Django Framework](https://www.djangoproject.com/)
-   **Database:** [SQLite](https://www.sqlite.org/index.html) (for development)
-   **Frontend:** HTML, CSS, JavaScript
-   **UI/UX:**
    -   [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks) for form field customization.
    -   SweetAlert2 for attractive pop-up notifications.

## 🚀 Setup and Installation

Follow these steps to set up the project on your local machine.

### 1. Prerequisites

-   Python 3.10 or higher
-   `pip` (Python package installer)
-   `venv` (for creating virtual environments)

### 2. Clone the Repository

```bash
git clone <repository-url>
cd To-DoList1.0
```

### 3. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

**On macOS and Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 4. Install Dependencies

Install all the required packages from the `requirements/local.txt` file.

```bash
pip install -r requirements/local.txt
```

### 5. Apply Database Migrations

Run the following command to create the database schema based on the project's models.

```bash
python manage.py migrate
```

### 6. Create a Superuser

This will allow you to access the Django admin interface.

```bash
python manage.py createsuperuser
```
Follow the prompts to create a username, email, and password.

## ▶️ Running the Application

Once the setup is complete, you can run the development server.

```bash
python manage.py runserver
```

The application will be available at **http://127.0.0.1:8000/**. You can log in with the superuser credentials you created or register a new user.

## ✅ Running Tests

To run the automated tests and ensure the application is working correctly, use the following command:

```bash
python manage.py test
```

## 📂 Project Structure

```
To-DoList1.0/
├── gestor_tareas/      # Main Django project directory
│   ├── settings.py     # Project settings
│   └── urls.py         # Root URL configuration
├── tareas/             # Core application for task management
│   ├── models.py       # Database models
│   ├── views.py        # Application views (logic)
│   ├── forms.py        # Custom forms
│   ├── urls.py         # App-specific URLs
│   └── templates/      # HTML templates for the app
├── static/             # Static files (CSS, JS, images)
├── templates/          # Base HTML templates
├── requirements/       # Python dependencies
└── manage.py           # Django's command-line utility
```

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements or find any issues, feel free to open an issue or submit a pull request.

1.  **Fork the repository.**
2.  **Create a new branch:** `git checkout -b feature/your-feature-name`
3.  **Make your changes and commit them:** `git commit -m 'Add some feature'`
4.  **Push to the branch:** `git push origin feature/your-feature-name`
5.  **Open a pull request.**

---
*This README was generated based on an analysis of the project's structure and code.*
