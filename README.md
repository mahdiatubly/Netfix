# Netfix

Netfix is a web application designed to facilitate service providers in showcasing their services and enabling customers to purchase services through the app. It is built using Django, a high-level Python web framework.

## Features

- **Service Provider Dashboard**: Service providers can create accounts and log in to manage their services.
- **Service Listing**: Service providers can list their services with detailed descriptions and pricing.
- **Customer Registration and Authentication**: Customers can register for accounts and log in securely.
- **Service Purchase**: Customers can browse through listed services and purchase them directly through the app.
- **User Profiles**: Customers and service providers have their profiles where they can manage personal information and view transaction history.
- **Search and Filter**: Users can search for services and filter them based on various criteria.
- **Responsive Design**: The application is responsive and works seamlessly across devices of different screen sizes.

## Technologies Used

- **Django**: The web framework used for backend development.
- **HTML/CSS/JavaScript**: For frontend development and user interface.
- **Bootstrap**: Frontend framework for responsive design.
- **SQLite/PostgreSQL**: Database management system.
- **Django Rest Framework**: For building RESTful APIs.
- **Payment Gateway Integration**: Integration with a payment gateway for handling transactions.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>

   ```
Notice the next a few steps can be excuted through build.sh script.

2. Set up the conda environment using the provided `env.yml` file:

   ```bash
   conda env create -f env.yml
   ```

3. Activate the conda environment:

   ```bash
   conda activate netfix_env
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://localhost:8000` in your web browser.

## Configuration

- **Database Configuration**: Configure the database settings in `settings.py` to use SQLite or PostgreSQL.
- **Email Configuration**: Configure SMTP settings in `settings.py` for sending transactional emails.
- **Security Settings**: Configure security settings such as CSRF protection, session management, etc., in `settings.py`.

## Deployment

- Netfix can be deployed on platforms like Heroku, AWS, or any other hosting provider that supports Django applications.
- Configure environment variables for sensitive information such as database credentials, API keys, etc., on the deployment platform.

## Contributing

Contributions are welcome! Fork the repository, create a new branch, make your changes, and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Support

For any inquiries or issues, please contact [mahdiatubly@gmail.com].

---
