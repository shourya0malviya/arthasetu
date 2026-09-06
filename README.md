# ⚡ ArthaSetu — AI Powered Local Skill Intelligence Platform

### *Bhopal's Digital Naka* | College Minor Project

---

```
  ___        _   _            ____       _
 / _ \      | | | |          / ___|  ___| |_ _   _
/ /_\ \_ __| |_| |__   __ _\___ \ / _ \ __| | | |
|  _  | '__| __| '_ \ / _` |___) |  __/ |_| |_| |
|_| |_|_|  \__|_| |_|\__,_|____/ \___|\__|\__,_|
```

> **"Post your work need in plain language — AI finds the right local worker."**

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Setup Guide](#setup-guide)
5. [Environment Variables](#environment-variables)
6. [Database Setup](#database-setup)
7. [API Integration (Gemini)](#gemini-api-integration)
8. [Running the App](#running-the-app)
9. [Feature Walkthrough](#feature-walkthrough)
10. [How AI Works in This Project](#how-ai-works)
11. [Future Improvements](#future-improvements)
12. [Viva Questions & Answers](#viva-qa)

---

## 🎯 Project Overview

**ArthaSetu** (अर्थसेतु — "Bridge of Livelihood") is a full-stack web application that acts as a smart matchmaking platform between clients who need local services and skilled workers in Bhopal.

### The Problem
Finding reliable local workers (plumbers, electricians, carpenters, etc.) is difficult and unorganised. People rely on word-of-mouth or informal contacts.

### The Solution
A "Digital Naka" (digital labour market) where:
- **Clients** describe their work need in natural language
- **AI (Google Gemini)** understands the description and detects the required skill
- **The system** matches the best-rated available workers from the database

### Example Flow
```
User types:  "मेरे घर में पानी का pipe leak हो रहा है"
Gemini AI:   { skill: "Plumber", confidence: 96 }
System:      Fetches top-rated Plumbers from DB
Result:      Shows 3 matching plumbers with contact details
```

---

## 🛠️ Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Frontend    | HTML5, CSS3, Bootstrap 5, Vanilla JS |
| Backend     | Python 3.x + Flask                |
| Database    | MySQL (via XAMPP)                 |
| AI Engine   | Google Gemini 1.5 Flash API       |
| Auth        | Flask Session + Werkzeug (hashing)|
| Fonts/Icons | Google Fonts (Syne + DM Sans), Bootstrap Icons |

---

## 📁 Project Structure

```
arthasetu/
│
├── app.py                  # Main Flask application (all routes & logic)
├── schema.sql              # MySQL database schema + seed data
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── README.md               # This file
│
├── static/
│   ├── css/
│   │   └── style.css       # Main stylesheet (dark theme, full custom)
│   ├── js/
│   │   └── main.js         # Frontend JavaScript (animations, UX)
│   └── img/                # (for any images you add later)
│
└── templates/
    ├── base.html           # Base layout (navbar, footer, flash messages)
    ├── index.html          # Landing / Home page
    ├── login.html          # Login form
    ├── register.html       # Registration form (client + worker)
    ├── post_job.html       # Client: post job with AI preview
    ├── match_results.html  # AI match results display
    ├── client_dashboard.html   # Client dashboard
    ├── worker_dashboard.html   # Worker dashboard
    ├── update_profile.html     # Worker profile edit
    ├── browse_workers.html     # Public worker listing + search
    ├── admin_dashboard.html    # Analytics/overview page
    └── 404.html            # Error page
```

---

## ⚙️ Setup Guide

### Prerequisites
- [XAMPP](https://www.apachefriends.org/) (for MySQL)
- [Python 3.8+](https://www.python.org/downloads/)
- A Google Gemini API key ([get one free here](https://aistudio.google.com/app/apikey))
- A terminal / command prompt

---

### Step 1 — Clone or Download the Project

Place the `arthasetu/` folder anywhere on your computer, e.g.:
```
C:\Users\YourName\Desktop\arthasetu\
```

---

### Step 2 — Start XAMPP MySQL

1. Open **XAMPP Control Panel**
2. Start **Apache** and **MySQL**
3. Open your browser → http://localhost/`phpmyadmin`


---

### Step 3 — Create the Database

In phpMyAdmin:
1. Click **"New"** in the left sidebar
2. Database name: `arthasetu_db` → Click **Create**
3. Click the **SQL** tab
4. Paste the contents of `schema.sql` into the text box
5. Click **Go** to execute

✅ This creates all 5 tables and inserts sample workers automatically.

---

### Step 4 — Set Up Python Environment

Open a terminal in the `arthasetu/` folder:

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

---

### Step 5 — Configure Environment Variables

```bash
# Copy the example file
copy .env.example .env        # Windows
cp .env.example .env          # Mac/Linux
```

Now open `.env` in any text editor and fill in your values:
```
SECRET_KEY=any_random_string_here_change_this
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=             ← leave blank if XAMPP default
MYSQL_DB=arthasetu_db
GEMINI_API_KEY=your_key_here
```

---

### Step 6 — Run the Application

```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

Open your browser and go to: **http://localhost:5000** 🎉

---

## 🔐 Environment Variables

| Variable        | Description                          | Example Value          |
|-----------------|--------------------------------------|------------------------|
| `SECRET_KEY`    | Flask session secret (any string)    | `arthasetu_xyz_2024`   |
| `MYSQL_HOST`    | Database host                        | `localhost`            |
| `MYSQL_USER`    | MySQL username                       | `root`                 |
| `MYSQL_PASSWORD`| MySQL password (blank for XAMPP)     | *(leave empty)*        |
| `MYSQL_DB`      | Database name                        | `arthasetu_db`         |
| `GEMINI_API_KEY`| Your Google Gemini API key           | `AIzaSy...`            |

---

## 🗄️ Database Setup

The `schema.sql` file creates these 5 tables:

### Tables

| Table        | Purpose                                         |
|--------------|-------------------------------------------------|
| `users`      | All users (clients + workers). Has `role` field |
| `workers`    | Extended profile for workers (skill, exp, etc.) |
| `jobs`       | Job postings from clients                       |
| `ai_matches` | AI match results (job ↔ worker + score)         |
| `ratings`    | Client ratings for workers (1–5 stars)          |

### Entity Relationship
```
users (1) ──< workers (1)      [one user = one worker profile]
users (1) ──< jobs (many)      [one client = many job posts]
jobs  (1) ──< ai_matches (many)[one job = multiple matches]
workers(1) ──< ai_matches (many)
jobs  (1) ──< ratings (many)
```

---

## 🤖 Gemini API Integration

### Getting Your API Key
1. Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account (free)
3. Click **"Create API Key"**
4. Copy the key and paste it in your `.env` file

### How It's Used in ArthaSetu

The AI integration lives in `app.py` inside the `extract_skill_with_ai()` function.

**The Prompt sent to Gemini:**
```
A client posted: "I need urgent wiring repair in my room"

Identify the skill from: [Plumber, Electrician, Carpenter, Painter, ...]
Give confidence score (0-100) and one-line reasoning.

Respond ONLY in JSON:
{ "skill": "Electrician", "confidence": 94, "reasoning": "..." }
```

**Gemini Response (parsed):**
```json
{
  "skill": "Electrician",
  "confidence": 94,
  "reasoning": "Wiring repair clearly indicates electrical work"
}
```

**Backend then:**
```python
matched_workers = get_matching_workers("Electrician", limit=5)
# Queries DB: SELECT workers WHERE skill_category = 'Electrician'
# Orders by: rating DESC, total_jobs DESC
```

### Fallback System
If the API key is missing or Gemini is unavailable, the app automatically falls back to **keyword-based matching** — so the app always works even without internet.

---

## ▶️ Running the App

```bash
# Make sure XAMPP MySQL is running first!
python app.py
```

### Test Accounts (create via Register page)
| Role   | Steps                                          |
|--------|------------------------------------------------|
| Client | Register → Role: Client → Login → Post a job   |
| Worker | Register → Role: Worker → Login → Edit Profile |

---

## 🎬 Feature Walkthrough

### 1. Home Page (`/`)
- Dynamic hero with rotating demo text
- Floating worker cards (CSS animations)
- Stats pulled live from DB
- Skill category grid linking to filtered worker lists
- AI demo code box

### 2. Register (`/register`)
- Toggle between Client / Worker roles
- Hashed passwords (Werkzeug `pbkdf2:sha256`)
- Workers get empty profile auto-created

### 3. Post a Job (`/client/post-job`)
- **Live AI preview** — as you type (after 20 chars), calls `/api/detect-skill`
- Debounced AJAX (1 second delay) to avoid spam
- Quick skill inject buttons
- On submit: full AI analysis → save job → fetch workers → save matches

### 4. AI Match Results (`/client/post-job` POST)
- Shows detected skill + confidence ring (SVG animation)
- Lists matched workers ranked by rating
- WhatsApp direct link
- Inline rating form

### 5. Client Dashboard (`/client/dashboard`)
- Job history table with status
- Quick action cards

### 6. Worker Dashboard (`/worker/dashboard`)
- Profile card with completion progress bar
- Incoming job matches list (with client phone)
- Availability colour indicator

### 7. Browse Workers (`/workers`)
- Search by name or description
- Filter by skill category
- Availability colour chips

### 8. Analytics (`/admin`)
- Chart.js donut (jobs by status)
- Bar chart (workers by skill)
- Top workers leaderboard
- Recent jobs feed

---

## 🔮 Future Improvements

1. **Real-time notifications** — use WebSockets (Flask-SocketIO) to alert workers of new matches instantly
2. **Location-based filtering** — integrate Google Maps API, show workers within X km radius
3. **Payment integration** — Razorpay/UPI QR codes for booking deposits
4. **Worker verification** — Aadhaar-based document upload and admin verification badge
5. **Multi-language support** — Hindi UI using Flask-Babel
6. **Mobile app** — Convert to PWA (Progressive Web App) with service workers
7. **AI-powered pricing** — Gemini estimates fair price range based on job type and location
8. **Review system** — Rich reviews with photos
9. **Worker scheduling** — Calendar integration for booking time slots
10. **Admin panel** — Full CRUD dashboard for managing users, flagging abuse, analytics

---

## 🎓 Viva Questions & Answers

### Basic Questions

**Q1. What is ArthaSetu and what problem does it solve?**
> ArthaSetu is a web-based platform that connects clients needing local services (plumbing, electrical, carpentry, etc.) with skilled workers in Bhopal. The problem it solves is the lack of a centralised, trusted marketplace for informal labour. Instead of relying on word-of-mouth, clients simply describe their need in natural language and AI finds the right worker.

**Q2. Why did you choose Flask over Django?**
> Flask is a micro-framework — lightweight, flexible, and easier to understand for beginners. For a project of this scope, Flask provides all the routing, session management, and database connectivity we need without the overhead of Django's ORM and admin system. It's also ideal for learning because you explicitly write what you need.

**Q3. What database did you use and why MySQL?**
> We used MySQL because it's relational, widely supported, and integrates seamlessly with XAMPP (a common local development stack in Indian colleges). MySQL enforces data integrity through foreign keys and supports complex joins needed for matching workers to jobs.

**Q4. Explain the database schema.**
> We have 5 tables: `users` (all accounts with a role field), `workers` (extended profile for worker accounts), `jobs` (client postings), `ai_matches` (links jobs to matched workers with a score), and `ratings` (star ratings from clients). The design follows third normal form to avoid data duplication.

---

### AI / Technical Questions

**Q5. How does the AI matching work? Explain step by step.**
> 1. Client submits a job description in natural language
> 2. Flask sends a structured prompt to Google Gemini API
> 3. The prompt asks Gemini to identify the skill from a fixed list and return JSON
> 4. Flask parses the JSON response (skill + confidence score)
> 5. A SQL query fetches workers with matching `skill_category`, ordered by rating
> 6. Results are stored in `ai_matches` table and displayed to the client

**Q6. What is prompt engineering? How did you use it?**
> Prompt engineering is the practice of carefully designing the text instructions given to an AI model to get reliable, structured output. In ArthaSetu, we engineered a prompt that: (a) gives the AI context about what the platform does, (b) restricts it to a fixed skill list to prevent random outputs, (c) asks for confidence scores, and (d) strictly demands JSON format — making the response machine-parsable.

**Q7. What if the Gemini API is unavailable?**
> We built a keyword-based fallback system (`keyword_skill_match()` function). It scans the job description for skill-related words (e.g. "pipe", "leak", "drain" → Plumber) and assigns a confidence score. This ensures the app works offline or when the API quota is exceeded.

**Q8. Why Gemini 1.5 Flash specifically?**
> Gemini 1.5 Flash is Google's fast, cost-efficient model ideal for simple classification tasks. Since we only need skill detection (not complex reasoning), Flash gives near-instant responses at low API cost compared to the Pro model. The free tier is sufficient for a college project.

**Q9. How are passwords stored securely?**
> We use Werkzeug's `generate_password_hash()` which applies PBKDF2-SHA256 with 600,000 iterations and a random salt. Plain text passwords are never stored. On login, `check_password_hash()` compares the input against the stored hash.

**Q10. Explain Flask sessions. How do you manage login state?**
> Flask sessions use server-signed cookies (signed with `SECRET_KEY`). On login, we store `user_id`, `user_name`, and `user_role` in `session`. Every protected route checks `session['user_id']` using the `@login_required` decorator we created. On logout, `session.clear()` removes all values.

---

### Design / Architecture Questions

**Q11. What is the MVC pattern and does your project follow it?**
> MVC stands for Model-View-Controller. In ArthaSetu: **Model** = MySQL tables + SQL queries in app.py, **View** = Jinja2 HTML templates in `/templates`, **Controller** = Flask route functions in app.py. We follow a simplified MVC structure appropriate for a Flask application.

**Q12. Why did you use Jinja2 templating?**
> Jinja2 is Flask's built-in templating engine. It allows us to write HTML with dynamic Python-like expressions (`{{ variable }}`), template inheritance (`extends 'base.html'`), loops, and conditionals. The `base.html` layout prevents code duplication — the navbar and footer are written once and reused everywhere.

**Q13. What is a REST API? Did you implement one?**
> A REST API is a web interface that returns data (usually JSON) instead of HTML. Yes — we implemented one endpoint: `POST /api/detect-skill` which accepts a JSON job description and returns the AI-detected skill. This is used for the live preview feature via JavaScript `fetch()` without reloading the page.

**Q14. How does the live AI preview on the job posting form work?**
> JavaScript listens to `input` events on the textarea. After 20 characters are typed, a debounced (1-second delay) AJAX `fetch()` call is made to `/api/detect-skill`. The Flask backend runs Gemini detection and returns JSON. JavaScript then updates the preview box with the skill name, confidence bar, and reasoning — all without a page reload. This is AJAX (Asynchronous JavaScript and XML).

**Q15. What security measures have you implemented?**
> (1) Password hashing — never plain text. (2) Session-based auth with signed cookies. (3) Route protection via `@login_required` decorator. (4) Role checks on dashboard routes (clients can't access worker pages). (5) Parameterised SQL queries using `%s` placeholders — prevents SQL injection. (6) Flask's CSRF protection via secret key.

---

### Conceptual Questions

**Q16. What is SQL injection and how did you prevent it?**
> SQL injection is an attack where malicious SQL code is inserted into input fields (e.g., `' OR '1'='1`). We prevented it by using **parameterised queries**: `cur.execute("SELECT * FROM users WHERE email = %s", (email,))`. The `%s` placeholder is handled by the MySQL library which safely escapes the input — the database treats it as data, not executable code.

**Q17. What is the difference between GET and POST requests?**
> GET requests are for fetching data — parameters are in the URL (e.g. `/workers?skill=Plumber`). POST requests are for submitting data — parameters are in the request body, not visible in URL. We use GET for browsing/filtering and POST for login, registration, and job submission because POST is more secure for sensitive data.

**Q18. Explain the concept of foreign keys in your database.**
> Foreign keys enforce relationships between tables. For example, `workers.user_id` is a foreign key referencing `users.id`. This means you can't add a worker profile without a valid user. The `ON DELETE CASCADE` clause means if a user is deleted, their worker profile and jobs are automatically deleted too — maintaining data consistency.

**Q19. What is Bootstrap 5 and why use it?**
> Bootstrap 5 is a CSS framework with pre-built responsive grid system, components (cards, buttons, tables, navbar), and utilities. Using it saved hundreds of lines of CSS for layout and responsiveness. We then added `style.css` on top for custom theming (dark navy colours, orange accents, custom cards).

**Q20. How would you scale this application for 10,000 users?**
> For production scaling: (1) Move from SQLite/MySQL to PostgreSQL on a cloud server. (2) Use Gunicorn + Nginx instead of Flask's dev server. (3) Add Redis caching for frequent AI results. (4) Deploy on AWS/GCP/Heroku. (5) Use connection pooling for the database. (6) Implement a job queue (Celery) for async AI processing. (7) Add CDN for static files.

---

## 📞 Contact & Credits

- **Project Type:** College Minor Project
- **Platform:** Bhopal, Madhya Pradesh, India
- **AI Used:** Google Gemini 1.5 Flash
- **Built with:** Python + Flask + MySQL + Bootstrap 5

---

*ArthaSetu — Bridging skills, building Bhopal.* ⚡
