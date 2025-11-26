# 🌾 Акыл Жер Government PortalA comprehensive government web portal for agricultural and veterinary system management in Kazakhstan. The system enables monitoring of farms, livestock, disease outbreaks, and crop issues across different districts.**Tech Stack:**- **Backend:** Django REST Framework (Python)- **Frontend:** React + TypeScript + Vite + Ant Design  - **Database:** SQLite (development)## 📋 Features✅ **Farms Registry** - Track registered farms with farmer details, location, and livestock  ✅ **Animal Herds Management** - Monitor different animal types and headcounts per farm  ✅ **Events & Outbreaks** - Record veterinary visits, vaccinations, disease reports, and mortality events  ✅ **Crop Issues Tracking** - Report and manage crop problems (pests, diseases, water stress, etc.)  ✅ **Dashboard** - View aggregated statistics and key metrics  ✅ **District Filtering** - Filter all data by administrative district  ✅ **Status Management** - Update event and crop issue statuses (new, in progress, resolved)  ✅ **Responsive UI** - Mobile-friendly design with agriculture-themed branding## 📁 Project Structure```agro-web/├── backend/                           # Django REST Framework API│   ├── akyl_jer/                     # Django project settings│   │   ├── settings.py               # Django configuration│   │   ├── urls.py                   # API routes│   │   └── wsgi.py                   # WSGI config│   ├── core/                         # Core application│   │   ├── models.py                 # Data models (District, Farm, Herd, Event, CropIssue)│   │   ├── serializers.py            # DRF serializers for API responses│   │   ├── views.py                  # API viewsets and endpoints│   │   ├── tests.py                  # Comprehensive API tests (21 tests)│   │   ├── admin.py                  # Django admin configuration│   │   ├── migrations/               # Database migrations│   │   └── management/               # Custom management commands│   │       └── commands/│   │           └── seed_fake_data.py # Generate demo data│   ├── manage.py                     # Django management script│   ├── requirements.txt              # Python dependencies│   └── venv/                         # Python virtual environment (not in git)│├── frontend/                          # React + TypeScript + Vite│   ├── src/│   │   ├── pages/                    # Page components│   │   │   ├── DashboardPage.tsx     # Dashboard with KPIs and charts│   │   │   ├── FarmsPage.tsx         # Farm registry with filters│   │   │   ├── EventsPage.tsx        # Events & outbreaks tracking│   │   │   └── CropIssuesPage.tsx    # Crop issues management│   │   ├── types/                    # TypeScript type definitions│   │   │   ├── farm.ts│   │   │   ├── event.ts│   │   │   └── cropIssue.ts│   │   ├── lib/│   │   │   └── api.ts                # Centralized API client with error handling│   │   ├── __tests__/                # Frontend tests│   │   ├── App.tsx                   # Main app with routing and layout│   │   ├── App.css                   # Global styles│   │   ├── index.css                 # Base styles│   │   └── main.tsx                  # Application entry point│   ├── public/                       # Static assets│   ├── package.json                  # Node dependencies│   ├── vite.config.ts                # Vite configuration│   ├── tsconfig.json                 # TypeScript configuration│   └── .env.example                  # Environment variables template│├── .gitignore                        # Git ignore rules├── README.md                         # This file└── run_all_tests.sh                  # Script to run all tests```---## 🚀 Getting Started### PrerequisitesBefore you begin, ensure you have the following installed:- **Python 3.8+** ([Download Python](https://www.python.org/downloads/))- **Node.js 16+** and npm ([Download Node.js](https://nodejs.org/))- **Git** ([Download Git](https://git-scm.com/downloads))### Step 1: Clone the Repository```bashgit clone <your-repo-url>cd agro-web```---## 🔧 Backend Setup (Django REST Framework)### 1. Navigate to Backend Directory```bashcd backend```### 2. Create a Virtual Environment**On Linux/Mac:**```bashpython3 -m venv venvsource venv/bin/activate```**On Windows:**```bashpython -m venv venvvenv\Scripts\activate```### 3. Install Dependencies```bashpip install -r requirements.txt```Or if `requirements.txt` doesn't exist:```bashpip install django djangorestframework django-cors-headers```### 4. Run Database Migrations```bashpython manage.py migrate```This creates the SQLite database and all required tables.### 5. Seed Database with Sample Data (Recommended)```bashpython manage.py seed_fake_data```This creates:- 3 districts (Almaty, Nur-Sultan, Shymkent)- 6-10 farms with realistic farmer names and locations- 15-30 animal herds (cattle, sheep, goats, horses, poultry)- 10-15 veterinary events (visits, vaccinations, disease reports, mortality)- 8-15 crop issues (pests, diseases, water stress, nutrient deficiencies)### 6. Create Admin User (Optional)```bashpython manage.py createsuperuser```Follow the prompts to create an admin account for accessing `/admin/`.### 7. Start the Backend Server```bashpython manage.py runserver 8000```✅ **Backend is now running at:** `http://localhost:8000`**Available Endpoints:**- API Root: `http://localhost:8000/`- Health Check: `http://localhost:8000/api/health/`- Districts: `http://localhost:8000/api/districts/`- Farms: `http://localhost:8000/api/farms/`- Events: `http://localhost:8000/api/events/`- Crop Issues: `http://localhost:8000/api/crop-issues/`- Dashboard: `http://localhost:8000/api/dashboard/summary/`- Admin Panel: `http://localhost:8000/admin/`### 8. Run Backend Tests (Optional)```bashpython manage.py test```**Expected Output:**```Found 21 test(s).Creating test database for alias 'default'........................----------------------------------------------------------------------Ran 21 tests in 1.025sOK```---## 💻 Frontend Setup (React + TypeScript + Vite)**Open a new terminal** (keep the backend server running).### 1. Navigate to Frontend Directory```bashcd frontend```### 2. Install Dependencies```bashnpm install```This installs all required packages including React, TypeScript, Vite, Ant Design, React Router, etc.### 3. Configure Environment VariablesCreate a `.env` file in the `frontend` directory:```bashcp .env.example .env```Edit `.env` to set the backend API URL:```envVITE_API_BASE_URL=http://localhost:8000```### 4. Start the Development Server```bashnpm run dev```✅ **Frontend is now running at:** `http://localhost:5173`The app will automatically open in your browser.### 5. Run Frontend Tests (Optional)```bashnpm test```---## 🎯 Using the Application### 1. Access the Web PortalOpen your browser and navigate to: **`http://localhost:5173`**### 2. Navigate Through PagesUse the sidebar to access different sections:- **Dashboard** - View overall statistics and metrics- **Farms Registry** - Browse and search registered farms- **Events & Outbreaks** - Track veterinary events and disease outbreaks- **Crop Issues** - Monitor and manage crop problems### 3. Filter DataEach page includes filters:- **District Filter** - Filter data by administrative region- **Status Filter** - Filter by status (new, in_progress, resolved)- **Search** - Search by farmer name, crop type, etc.### 4. Update StatusFor Events and Crop Issues:- Click the status dropdown in any row- Select a new status (New → In Progress → Resolved)- Changes are saved automatically### 5. Access Admin Panel (Optional)If you created a superuser:1. Go to `http://localhost:8000/admin/`2. Login with your superuser credentials3. Manage data directly through Django admin interface---## 📊 API Endpoints### Districts- `GET /api/districts/` - List all districts### Farms- `GET /api/farms/` - List all farms- `GET /api/farms/{id}/` - Get specific farm- Query params: `?district=<code>`, `?search=<query>`### Events- `GET /api/events/` - List all events- `GET /api/events/{id}/` - Get specific event- `PATCH /api/events/{id}/` - Update event status- Query params: `?district=<code>`, `?event_type=<type>`, `?status=<status>`### Crop Issues- `GET /api/crop-issues/` - List all crop issues- `GET /api/crop-issues/{id}/` - Get specific crop issue- `POST /api/crop-issues/` - Create new crop issue- `PATCH /api/crop-issues/{id}/` - Update crop issue status- Query params: `?district=<code>`, `?crop_type=<type>`, `?problem_type=<type>`, `?severity=<level>`, `?status=<status>`### Dashboard- `GET /api/dashboard/summary/` - Get dashboard statistics- Query params: `?district=<code>`---## 🛠️ Development Commands### Backend```bash# Activate virtual environmentsource venv/bin/activate          # Linux/Macvenv\Scripts\activate              # Windows# Run development serverpython manage.py runserver 8000# Run testspython manage.py test

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Seed database
python manage.py seed_fake_data

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell
```

### Frontend

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npx tsc --noEmit

# Linting
npm run lint
```

---

## 🧪 Testing

### Run All Tests

From the project root:

```bash
./run_all_tests.sh
```

Or manually:

**Backend:**
```bash
cd backend
source venv/bin/activate
python manage.py test
```

**Frontend:**
```bash
cd frontend
npm test
```

---

## 🏗️ Production Deployment

### Backend (Django)

1. Update `settings.py`:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use PostgreSQL instead of SQLite
   - Set up proper `SECRET_KEY`

2. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

3. Use a production server (Gunicorn, uWSGI)
4. Set up Nginx as reverse proxy
5. Use environment variables for sensitive data

### Frontend (React)

1. Build for production:
   ```bash
   npm run build
   ```

2. Deploy the `dist/` folder to:
   - Static hosting (Netlify, Vercel, GitHub Pages)
   - CDN (Cloudflare, AWS S3 + CloudFront)
   - Web server (Nginx, Apache)

3. Update `.env.production` with production API URL

---

## 📝 Data Models

### District
- name, code

### Farm
- district, farmer_name, phone, village, location (lat/lng)

### Herd
- farm, animal_type, headcount

### Event
- farm, event_type, disease_suspected, description, animals_affected, status

### CropIssue
- farm, crop_type, problem_type, title, description, severity, area_affected_ha, status

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👥 Support

For questions or issues:
- Create an issue in the GitHub repository
- Contact the development team

---

## 🎉 Acknowledgments

- Built for agricultural management in Kazakhstan
- Designed for government and farm administrators
- Supports multilingual content (English/Kazakh/Russian)

---

**Happy Farming! 🌾🐄🐑**
