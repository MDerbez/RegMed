# RegMed 🏥
CS50 Project Homecare Electronic Record System

A simple, web-based electronic health record (EHR) system designed specifically for homecare services. Built with Flask and Bootstrap for a clean, responsive interface.

## 🚀 Live Demo

Deploy this application instantly to the cloud:

[![Deploy on Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/MDerbez/RegMed)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/TEMPLATE_URL)

## ✨ Features

- **Patient Management**: Add and view patient information including contact details and medical history
- **Medical Records**: Document visits, diagnoses, treatments, and notes
- **Dashboard**: Quick overview of recent activity and key metrics
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Simple Interface**: Clean, intuitive design for healthcare professionals

## 🛠️ Technology Stack

- **Backend**: Python (Flask)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Icons**: Font Awesome
- **Deployment**: Gunicorn WSGI server

## 📦 Local Installation

1. Clone the repository:
```bash
git clone https://github.com/MDerbez/RegMed.git
cd RegMed
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and visit `http://localhost:5000`

## 🌐 Deployment Options

### Heroku
1. Click the "Deploy to Heroku" button above, or
2. Manual deployment:
```bash
heroku create your-app-name
git push heroku main
```

### Railway
1. Click the "Deploy on Railway" button above, or
2. Connect your GitHub repository to Railway

### Other Platforms
The app includes configuration files for various platforms:
- `Procfile` - For Heroku and similar platforms
- `railway.json` - For Railway deployment
- `runtime.txt` - Specifies Python version

## 🔧 Configuration

Set the following environment variables for production:
- `SECRET_KEY`: A secure secret key for Flask sessions
- `PORT`: The port to run the application (automatically set by most platforms)

## ⚠️ Important Notes

- **Demo Application**: This is a demonstration version using in-memory storage
- **Data Persistence**: Data is not saved between application restarts
- **Production Use**: For production deployment, implement:
  - Database storage (PostgreSQL, MySQL, etc.)
  - User authentication and authorization
  - Data validation and sanitization
  - HTTPS/SSL encryption
  - Backup and recovery procedures
  - HIPAA compliance measures (if applicable)

## 🎯 Getting Started

1. **Add Patients**: Start by adding patient information to the system
2. **Document Visits**: Record medical visits, diagnoses, and treatments
3. **View Records**: Access patient history and recent activity from the dashboard

## 📋 Project Structure

```
RegMed/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Procfile           # Deployment configuration
├── runtime.txt        # Python version specification
├── app.json           # Heroku app configuration
├── railway.json       # Railway deployment config
└── templates/         # HTML templates
    ├── base.html      # Base template
    ├── index.html     # Dashboard
    ├── patients.html  # Patient list
    ├── add_patient.html
    ├── records.html   # Medical records
    ├── add_record.html
    └── about.html     # About page
```

## 👨‍💻 Development

This project was created as part of the CS50 course, demonstrating:
- Web application development with Flask
- Responsive design with Bootstrap
- Form handling and data validation
- Template rendering with Jinja2
- Cloud deployment practices

## 📝 License

This project is for educational purposes as part of the CS50 course.
