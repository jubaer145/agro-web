# Акыл Жер Government Portal

A government web portal for agricultural and veterinary system management, built with Django REST Framework (backend) and React + TypeScript + Vite + Ant Design (frontend).

## Project Structure

```
agro-web/
├── backend/                      # Django REST Framework API
│   ├── akyl_jer/                # Django project
│   ├── core/                    # Core app
│   │   ├── models.py           # District, Farm, Herd models
│   │   ├── serializers.py      # DRF serializers
│   │   ├── views.py            # API viewsets
│   │   ├── tests.py            # API tests
│   │   └── management/         # Management commands
│   │       └── commands/
│   │           └── seed_fake_data.py
│   ├── manage.py
│   └── venv/                    # Python virtual environment
├── frontend/                    # React + TypeScript + Vite
│   ├── src/
│   │   ├── pages/              # Page components
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── FarmsPage.tsx   # Farm registry with filters
│   │   │   └── EventsPage.tsx
│   │   ├── types/              # TypeScript types
│   │   │   └── farm.ts
│   │   ├── App.tsx             # Main app with routing
│   │   └── main.tsx            # Entry point
│   ├── package.json
│   └── vite.config.ts
├── README.md
└── run_all_tests.sh            # Complete test suite
```

## Backend Setup (Django REST Framework)

### Prerequisites
- Python 3.8+
- pip

### Installation & Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies (if not already done):**
   ```bash
   pip install django djangorestframework django-cors-headers
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Seed database with fake data:**
   ```bash
   python manage.py seed_fake_data
   ```
   This creates 3 districts, 6-10 farms, and 15-30 animal herds with realistic data.

6. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

### Running the Backend

```bash
# Make sure you're in the backend directory with venv activated
cd backend
source venv/bin/activate
python manage.py runserver 8000
```

The API will be available at: `http://localhost:8000`

- Health endpoint: `http://localhost:8000/api/health/`
- Admin panel: `http://localhost:8000/admin/`

### Running Backend Tests

```bash
cd backend
source venv/bin/activate
python manage.py test
```

Expected output:
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.XXXs

OK
Destroying test database for alias 'default'...
```

## Frontend Setup (React + TypeScript + Vite)

### Prerequisites
- Node.js 18+
- npm

### Installation

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies (if not already done):**
   ```bash
   npm install
   ```

### Running the Frontend

```bash
cd frontend
npm run dev
```

The frontend will be available at: `http://localhost:5173`

### Running Frontend Tests

```bash
cd frontend
npm test
```

Expected output:
```
PASS  src/pages/__tests__/DashboardPage.test.tsx
  DashboardPage
    ✓ renders Dashboard title
    ✓ calls /api/health/ and displays status
    ✓ handles API error gracefully
    ✓ displays system overview card

Test Suites: 1 passed, 1 total
Tests:       4 passed, 4 total
```

## Features

### Backend API
- **Health Endpoint**: `/api/health/` - Returns `{"status": "ok"}`
- **CORS Configuration**: Allows requests from `http://localhost:5173`
- **SQLite Database**: Configured for local development
- **Django Admin**: Full admin interface at `/admin/`

### Frontend Application

#### Pages
1. **Dashboard** (`/dashboard`)
   - Displays API health status
   - Shows system statistics (fake data)
   - System overview card

2. **Farms** (`/farms`)
   - Table view of registered farms
   - Filter and search functionality
   - Action buttons for view/edit

3. **Events** (`/events`)
   - Veterinary events and scheduling
   - Date filtering
   - Priority and status tags

#### UI/UX Features
- **Ant Design Components**: Professional UI components
- **Responsive Layout**: Works on desktop and mobile
- **Sidebar Navigation**: Easy navigation between sections
- **Header**: App title and branding
- **API Integration**: Real-time health check from backend

## Development Workflow

### Full Stack Development

1. **Terminal 1 - Backend:**
   ```bash
   cd backend
   source venv/bin/activate
   python manage.py runserver 8000
   ```

2. **Terminal 2 - Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open browser:**
   ```
   http://localhost:5173
   ```

The Vite dev server is configured to proxy `/api/*` requests to the Django backend at `http://localhost:8000`.

### Running All Tests

**Backend tests:**
```bash
cd backend && source venv/bin/activate && python manage.py test
```

**Frontend tests:**
```bash
cd frontend && npm test
```

## Technology Stack

### Backend
- **Django 5.2**: Web framework
- **Django REST Framework**: API framework
- **django-cors-headers**: CORS middleware
- **SQLite**: Database (development)

### Frontend
- **React 19**: UI library
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **Ant Design**: UI component library
- **React Router**: Client-side routing
- **Jest + Testing Library**: Testing framework

## API Documentation

### GET /api/health/

Check API health status.

**Response:**
```json
{
  "status": "ok"
}
```

**Status Codes:**
- `200 OK`: API is healthy

## Future Enhancements

- [ ] User authentication and authorization
- [ ] Real database models for Farms and Events
- [ ] CRUD operations for farms management
- [ ] Event scheduling and calendar view
- [ ] File uploads for farm documents
- [ ] Reporting and analytics
- [ ] Email notifications
- [ ] Mobile app support
- [ ] Docker containerization
- [ ] CI/CD pipeline

## Notes

- This is a development setup with **fake data** for demonstration
- SQLite is used for simplicity; use PostgreSQL for production
- Secret keys and debug settings should be configured properly for production
- CORS settings should be restricted in production

## License

MIT

## Contact

For questions or issues, please contact the development team.
