# Gas Utility Customer Service

A modern web application for managing gas utility service requests with Material Design UI. This system allows customers to submit service requests and support staff to manage and resolve them efficiently.

## 🌟 Live Demo

The application is deployed at: [https://gas-utility-service.onrender.com](https://gas-utility-service.onrender.com)

Demo Credentials:
- **Customer:** username: `customer1` password: `customer123`
- **Support:** username: `support_admin` password: `support_password123`

## ✨ Features

- **Material Design UI**
  - Modern, responsive interface
  - Intuitive user experience
  - Beautiful visual elements and animations

- **Customer Interface**
  - Account registration and profile management
  - Service request submission with attachments
  - Request tracking and status updates
  - Direct communication with support staff

- **Support Staff Interface**
  - Dashboard with service request statistics
  - Comprehensive request management
  - Internal notes and customer communications
  - Multi-step workflow for resolution
  - User management capabilities

## 🔧 Technology Stack

- **Backend:** Django 5.1.7
- **Frontend:** Material Design Bootstrap (MDB)
- **Database:** PostgreSQL (production) / SQLite (development)
- **Hosting:** Render
- **Other:** Whitenoise for static files, Gunicorn for production server

## 📋 Installation

### Local Development

1. Clone this repository:
   ```
   git clone https://github.com/saurabhdubeyy/gas-utility-service.git
   cd gas-utility-service
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv env
   env\Scripts\activate  # On Windows
   source env/bin/activate  # On macOS/Linux
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

### Production Deployment

This application is configured for deployment on Render, but can be deployed on any platform that supports Django.

Detailed deployment instructions are available in [DEPLOYMENT.md](DEPLOYMENT.md).

## 👥 Support Staff Setup

There are multiple ways to create support staff accounts:

1. **Using the Admin Interface**:
   - Log in as a superuser
   - Create a new user
   - Add them to the "Support" group
   - Create a SupportRepresentative object linked to this user

2. **Using the Direct URL**:
   - Visit `/support/create-default-user/` to create a default support user
   - This creates a user with credentials:
     - Username: `support_admin`
     - Password: `support_password123`

3. **Programmatically**:
   - Use the Django management command:
     ```
     python manage.py create_support_user
     ```

Complete details on support system functionality are available in [SUPPORT_SETUP.md](SUPPORT_SETUP.md).

## 🚀 Project Structure

```
gas_utility_service/
├── accounts/        # User authentication and profiles
├── requests/        # Service request management
├── support/         # Support staff functionality
├── templates/       # HTML templates
├── static/          # CSS, JS, and other static files
└── gas_utility_service/  # Project settings
```

## 🔒 Security

This application implements Django's security best practices:
- CSRF protection
- Secure password storage
- User permission controls
- Form validation

For production deployments, ensure:
- DEBUG is set to False
- SECRET_KEY is securely stored
- HTTPS is enabled

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please contact [saurabhdubeykpl@gmail.com]. 
