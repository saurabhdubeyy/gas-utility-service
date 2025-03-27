# Gas Utility Customer Service

A modern web application for managing gas utility service requests with Material Design UI. This system allows customers to submit service requests and support staff to manage and resolve them efficiently.

## Features

- **Customer Interface**
  - Account registration and management
  - Service request submission and tracking
  - Communication with support staff

- **Support Interface**
  - Dashboard with request statistics
  - Service request management
  - Internal notes and customer communication
  - Status update workflow

- **Modern UI/UX**
  - Material Design interface
  - Responsive layout for all devices
  - Intuitive navigation and workflows
  - Visual status indicators

## Technology Stack

- Django 5.1.7
- Material Design Bootstrap (MDB)
- FontAwesome icons
- SQLite database (configurable for production use)

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd gas_utility_service
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

4. Apply migrations:
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

7. Access the application at:
   ```
   http://127.0.0.1:8000/
   ```

## Support Staff Setup

See the detailed documentation in [SUPPORT_SETUP.md](SUPPORT_SETUP.md) for instructions on setting up and managing support staff accounts.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please contact [your-email@example.com]. 