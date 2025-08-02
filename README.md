# PES Pakistan Entrepreneurship Society - Web Application

A complete, full-stack web application for managing the Pakistan Entrepreneurship Society platform with member management, products, services, announcements, and contact functionality.

## 🚀 Features

### Authentication & User Management
- **Admin Login**: Full administrative access
- **Member Registration**: New member signup
- **JWT-based Authentication**: Secure session management
- **Role-based Access Control**: Admin vs Member permissions

### Core Functionality
- **Member Management**: CRUD operations for member data (Name, Email, Phone, Role, Skills, Achievements)
- **Products Management**: CRUD operations for products (Name, Description, Price, Image, Category)
- **Services Management**: CRUD operations for services (Name, Description, Contact Info, Price)
- **Announcements**: CRUD operations for notices (Title, Description, Date)
- **Contact Form**: Support form for inquiries (Name, Email, Message)

### Dashboards
- **Admin Dashboard**: Complete management interface with statistics
- **Member Dashboard**: View-only access to products, services, and announcements

## 🛠 Tech Stack

### Backend
- **Python 3.10+** with Flask
- **SQLite** database
- **SQLAlchemy** ORM
- **Flask-CORS** for cross-origin requests
- **Werkzeug** for password hashing

### Frontend
- **React.js** with Vite
- **React Router** for navigation
- **Tailwind CSS** for styling
- **Lucide React** for icons

## 📁 Project Structure

```
pes-app/
├── src/
│   ├── main.py                 # Flask application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py            # User model
│   │   ├── product.py         # Product model
│   │   ├── service.py         # Service model
│   │   ├── announcement.py    # Announcement model
│   │   └── contact.py         # Contact model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentication routes
│   │   ├── user.py            # User management routes
│   │   ├── product.py         # Product CRUD routes
│   │   ├── service.py         # Service CRUD routes
│   │   ├── announcement.py    # Announcement CRUD routes
│   │   └── contact.py         # Contact form routes
│   ├── database/
│   │   └── app.db             # SQLite database (auto-created)
│   └── static/                # Built React frontend files
├── venv/                      # Python virtual environment
├── requirements.txt           # Python dependencies
└── README.md                  # This file

pes-frontend/
├── src/
│   ├── App.jsx                # Main React application
│   ├── contexts/
│   │   └── AuthContext.jsx    # Authentication context
│   └── components/
│       ├── Navbar.jsx         # Navigation component
│       ├── Home.jsx           # Homepage
│       ├── Login.jsx          # Login form
│       ├── Register.jsx       # Registration form
│       ├── Dashboard.jsx      # Member dashboard
│       ├── AdminDashboard.jsx # Admin dashboard
│       ├── Products.jsx       # Products management
│       ├── Services.jsx       # Services management
│       ├── Announcements.jsx  # Announcements management
│       ├── Contact.jsx        # Contact form
│       └── Profile.jsx        # User profile management
├── package.json               # Node.js dependencies
├── vite.config.js            # Vite configuration
└── dist/                     # Built frontend files
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** installed
- **Node.js 18+** and npm installed
- **VS Code** (recommended)
- **Windows** environment

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd pes-app
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask application:**
   ```bash
   python src/main.py
   ```

   The backend will start on `http://localhost:5000`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd pes-frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Build the frontend:**
   ```bash
   npm run build
   ```

4. **Copy built files to Flask static directory:**
   ```bash
   xcopy /E /I dist\* ..\pes-app\src\static\
   ```

### Access the Application

1. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

2. **Default Admin Credentials:**
   - **Email:** admin@pes.com
   - **Password:** admin123

## 🔧 Development

### Backend Development

1. **Activate virtual environment:**
   ```bash
   cd pes-app
   venv\Scripts\activate
   ```

2. **Run Flask in development mode:**
   ```bash
   python src/main.py
   ```

### Frontend Development

1. **Start development server:**
   ```bash
   cd pes-frontend
   npm run dev
   ```

2. **Build for production:**
   ```bash
   npm run build
   ```

3. **Copy to Flask static directory:**
   ```bash
   xcopy /E /I dist\* ..\pes-app\src\static\
   ```

## 📊 Database Schema

### Users Table
- `id` (Primary Key)
- `name` (String)
- `email` (String, Unique)
- `phone` (String)
- `password_hash` (String)
- `role` (String: 'admin' or 'member')
- `skills` (Text)
- `achievements` (Text)
- `created_at` (DateTime)
- `is_active` (Boolean)

### Products Table
- `id` (Primary Key)
- `name` (String)
- `description` (Text)
- `price` (Float)
- `image_url` (String)
- `category` (String)
- `created_by` (Foreign Key to Users)
- `created_at` (DateTime)

### Services Table
- `id` (Primary Key)
- `name` (String)
- `description` (Text)
- `contact_info` (String)
- `price` (Float)
- `created_by` (Foreign Key to Users)
- `created_at` (DateTime)

### Announcements Table
- `id` (Primary Key)
- `title` (String)
- `description` (Text)
- `date` (DateTime)
- `created_by` (Foreign Key to Users)

### Contact Messages Table
- `id` (Primary Key)
- `name` (String)
- `email` (String)
- `message` (Text)
- `created_at` (DateTime)

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user info

### Users
- `GET /api/users` - Get all users (Admin only)
- `GET /api/users/<id>` - Get user by ID
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user (Admin only)

### Products
- `GET /api/products` - Get all products
- `POST /api/products` - Create product (Admin only)
- `GET /api/products/<id>` - Get product by ID
- `PUT /api/products/<id>` - Update product (Admin only)
- `DELETE /api/products/<id>` - Delete product (Admin only)

### Services
- `GET /api/services` - Get all services
- `POST /api/services` - Create service (Admin only)
- `GET /api/services/<id>` - Get service by ID
- `PUT /api/services/<id>` - Update service (Admin only)
- `DELETE /api/services/<id>` - Delete service (Admin only)

### Announcements
- `GET /api/announcements` - Get all announcements
- `POST /api/announcements` - Create announcement (Admin only)
- `GET /api/announcements/<id>` - Get announcement by ID
- `PUT /api/announcements/<id>` - Update announcement (Admin only)
- `DELETE /api/announcements/<id>` - Delete announcement (Admin only)

### Contact
- `POST /api/contact` - Submit contact form
- `GET /api/contact` - Get all contact messages (Admin only)

## 🎨 UI Features

### Responsive Design
- Mobile-friendly interface
- Touch-optimized controls
- Adaptive layouts

### User Experience
- Clean, modern interface
- Intuitive navigation
- Real-time form validation
- Success/error notifications
- Loading states

### Admin Features
- Comprehensive dashboard with statistics
- CRUD operations for all entities
- User management
- Contact message viewing

### Member Features
- Personal dashboard
- Profile management
- View products and services
- Read announcements
- Contact form access

## 🔒 Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **Session Management**: JWT-based authentication
- **Role-based Access**: Admin vs Member permissions
- **Input Validation**: Server-side validation for all forms
- **CORS Protection**: Configured for secure cross-origin requests

## 🐛 Troubleshooting

### Common Issues

1. **Database not found error:**
   - Delete `src/database/app.db` and restart the application
   - The database will be recreated automatically

2. **Frontend not loading:**
   - Ensure you've built the frontend: `npm run build`
   - Copy files to Flask static directory
   - Restart the Flask server

3. **CORS errors:**
   - Ensure Flask-CORS is installed: `pip install flask-cors`
   - Check that CORS is configured in `main.py`

4. **Virtual environment issues:**
   - Recreate virtual environment: `python -m venv venv`
   - Reinstall dependencies: `pip install -r requirements.txt`

### Development Tips

1. **Backend changes:** Restart Flask server to see changes
2. **Frontend changes:** Rebuild and copy to static directory
3. **Database changes:** Delete database file to reset schema
4. **New dependencies:** Update requirements.txt or package.json

## 📝 License

This project is created for educational purposes for the Pakistan Entrepreneurship Society.

## 🤝 Support

For support or questions about this application:
- Email: info@pes-pakistan.org
- Phone: +92-300-1234567

---

**Built with ❤️ for PES Pakistan Entrepreneurship Society**

