# Command Reference - Акыл Жер Government Portal

## Quick Start

Use the provided shell script:
```bash
./run.sh
```

Or follow the manual commands below.

---

## Backend Commands (Django REST Framework)

### Setup (Already Done)
```bash
# Create virtual environment
cd backend
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install django djangorestframework django-cors-headers

# Create project and app (already done)
django-admin startproject akyl_jer .
python manage.py startapp core
```

### Running Backend Server
```bash
cd backend
source venv/bin/activate
python manage.py runserver 8000
```

**Access:**
- API: http://localhost:8000
- Health endpoint: http://localhost:8000/api/health/
- Admin panel: http://localhost:8000/admin/

### Running Backend Tests
```bash
cd backend
source venv/bin/activate
python manage.py test
```

**Expected output:**
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.XXXs

OK
Destroying test database for alias 'default'...
```

### Other Useful Backend Commands

**Run migrations:**
```bash
cd backend
source venv/bin/activate
python manage.py migrate
```

**Create superuser:**
```bash
cd backend
source venv/bin/activate
python manage.py createsuperuser
```

**Create new migrations:**
```bash
cd backend
source venv/bin/activate
python manage.py makemigrations
```

**Django shell:**
```bash
cd backend
source venv/bin/activate
python manage.py shell
```

---

## Frontend Commands (React + TypeScript + Vite)

### Setup (Already Done)
```bash
# Create Vite project (already done)
npm create vite@latest frontend -- --template react-ts

# Install dependencies
cd frontend
npm install

# Install additional packages
npm install antd react-router-dom
npm install --save-dev jest ts-jest @types/jest @testing-library/react @testing-library/jest-dom jest-environment-jsdom identity-obj-proxy
```

### Running Frontend Dev Server
```bash
cd frontend
npm run dev
```

**Access:**
- Frontend: http://localhost:5173

The Vite dev server will automatically proxy `/api/*` requests to `http://localhost:8000`.

### Running Frontend Tests
```bash
cd frontend
npm test
```

### Building for Production
```bash
cd frontend
npm run build
```

### Preview Production Build
```bash
cd frontend
npm run preview
```

### Linting
```bash
cd frontend
npm run lint
```

---

## Development Workflow

### Full Stack Development (2 Terminals)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python manage.py runserver 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open your browser to http://localhost:5173

---

## Running All Tests

**Backend + Frontend Tests (Sequential):**
```bash
# Backend tests
cd backend && source venv/bin/activate && python manage.py test

# Frontend tests
cd ../frontend && npm test
```

---

## Project Structure

```
agro-web/
├── backend/
│   ├── akyl_jer/              # Django project settings
│   │   ├── settings.py        # Main settings (CORS, apps, etc.)
│   │   ├── urls.py            # URL routing
│   │   └── wsgi.py
│   ├── core/                  # Core app
│   │   ├── views.py           # API views (health endpoint)
│   │   ├── tests.py           # API tests
│   │   └── models.py
│   ├── manage.py              # Django management script
│   ├── db.sqlite3             # SQLite database
│   └── venv/                  # Python virtual environment
│
├── frontend/
│   ├── src/
│   │   ├── pages/             # Page components
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── FarmsPage.tsx
│   │   │   ├── EventsPage.tsx
│   │   │   └── __tests__/     # Test files
│   │   ├── App.tsx            # Main app component
│   │   ├── main.tsx           # Entry point
│   │   └── setupTests.ts      # Jest setup
│   ├── vite.config.ts         # Vite configuration (proxy)
│   ├── jest.config.cjs        # Jest configuration
│   ├── package.json           # Dependencies and scripts
│   └── tsconfig.json          # TypeScript configuration
│
├── README.md                  # Main documentation
├── COMMANDS.md                # This file
└── run.sh                     # Quick start script
```

---

## Troubleshooting

### Backend Issues

**"ModuleNotFoundError: No module named 'rest_framework'"**
- Make sure the virtual environment is activated: `source venv/bin/activate`
- Reinstall packages: `pip install django djangorestframework django-cors-headers`

**"Port 8000 is already in use"**
- Kill the process: `lsof -ti:8000 | xargs kill -9`
- Or use a different port: `python manage.py runserver 8001`

### Frontend Issues

**"Cannot find module 'antd'"**
- Reinstall dependencies: `npm install`

**"Port 5173 is already in use"**
- Kill the process: `lsof -ti:5173 | xargs kill -9`
- Or Vite will automatically suggest a different port

**CORS Errors**
- Make sure the backend is running on port 8000
- Check `backend/akyl_jer/settings.py` for CORS configuration
- Verify Vite proxy in `frontend/vite.config.ts`

---

## API Endpoints

### Health Check
```
GET /api/health/
```

**Response:**
```json
{
  "status": "ok"
}
```

**Status Codes:**
- `200 OK`: API is healthy

---

## Environment Variables (Future)

For production, create `.env` files:

**Backend `.env`:**
```
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/dbname
ALLOWED_HOSTS=yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

**Frontend `.env`:**
```
VITE_API_URL=https://api.yourdomain.com
```

---

## Deployment (Future)

### Backend Deployment
- Use PostgreSQL instead of SQLite
- Set `DEBUG=False`
- Configure proper `ALLOWED_HOSTS`
- Collect static files: `python manage.py collectstatic`
- Use gunicorn or uwsgi as WSGI server
- Configure nginx as reverse proxy

### Frontend Deployment
- Build: `npm run build`
- Serve the `dist/` directory
- Configure environment variables for production API URL
- Set up proper CORS on backend

---

## Additional Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **React Documentation**: https://react.dev/
- **Vite Documentation**: https://vitejs.dev/
- **Ant Design**: https://ant.design/
- **TypeScript**: https://www.typescriptlang.org/
- **Jest**: https://jestjs.io/
- **React Testing Library**: https://testing-library.com/react
