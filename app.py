# ============================================================
# app.py — ArthaSetu Flask Application
# AI Powered Local Skill Intelligence Platform (Bhopal Edition)
# ============================================================

import os
import json
from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash, jsonify)
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

import google.generativeai as genai

# ── Load environment variables from .env file ──────────────


# ── Flask app setup ────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'arthasetu_dev_secret_2024')

# ── MySQL configuration # ── MySQL configuration ────────────────────────────────────
app.secret_key = 'arthasetu2024secret'

app.config['MYSQL_HOST']        = 'gateway01.ap-northeast-1.prod.aws.tidbcloud.com'
app.config['MYSQL_PORT']        = 4000
app.config['MYSQL_USER']        = '2FhJhaRgeitrSs1.root'
app.config['MYSQL_PASSWORD']    = 'JHhDYvizVL5LDWXp'
app.config['MYSQL_DB']          = 'test'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_SSL']         = True



mysql = MySQL(app)

# ── Gemini AI configuration ────────────────────────────────
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def login_required(f):
    """Decorator: redirect to login if user is not in session."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def extract_skill_with_ai(job_description: str) -> dict:
    """
    Send job description to Gemini API.
    Returns: { skill, confidence, reasoning }
    """
    if not GEMINI_API_KEY:
        # Fallback: keyword-based matching if no API key
        return keyword_skill_match(job_description)

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')

        # ── Prompt Engineering ──────────────────────────────
        prompt = f"""You are an AI assistant for ArthaSetu, a local skill-matching platform in Bhopal, India.

A client posted this job requirement:
"{job_description}"

Your task:
1. Identify the PRIMARY skill category required from this fixed list ONLY:
   Plumber, Electrician, Carpenter, Painter, Cleaner, AC Mechanic, Mason, Welder,
   Gardener, Driver, Cook, Security Guard, Tailor, Computer Technician, Other

2. Give a confidence score (0-100) for your detection.
3. Briefly explain your reasoning in one sentence.

Respond ONLY in this exact JSON format (no extra text):
{{
  "skill": "<skill from list>",
  "confidence": <number 0-100>,
  "reasoning": "<one sentence explanation>"
}}"""

        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        # Strip markdown code fences if present
        if raw_text.startswith('```'):
            raw_text = raw_text.split('```')[1]
            if raw_text.startswith('json'):
                raw_text = raw_text[4:]

        result = json.loads(raw_text.strip())
        return result

    except Exception as e:
        print(f"[Gemini Error] {e}")
        return keyword_skill_match(job_description)


def keyword_skill_match(description: str) -> dict:
    """
    Simple keyword-based fallback skill detection.
    Used when Gemini API is unavailable.
    """
    description = description.lower()
    skill_keywords = {
        'Plumber':            ['pipe', 'plumb', 'water', 'leak', 'tap', 'drain', 'bathroom', 'toilet'],
        'Electrician':        ['wire', 'electric', 'switch', 'socket', 'light', 'mcb', 'inverter', 'power', 'wiring'],
        'Carpenter':          ['wood', 'furniture', 'door', 'window', 'carpenter', 'cabinet', 'shelf'],
        'Painter':            ['paint', 'colour', 'color', 'wall', 'texture', 'waterproof'],
        'Cleaner':            ['clean', 'sweep', 'mop', 'dust', 'sofa', 'pest', 'sanitize'],
        'AC Mechanic':        ['ac', 'air condition', 'cooling', 'refrigerator', 'fridge', 'gas refill'],
        'Mason':              ['brick', 'cement', 'construction', 'plaster', 'tile', 'floor'],
        'Computer Technician':['computer', 'laptop', 'internet', 'wifi', 'printer', 'software'],
    }

    best_skill  = 'Other'
    best_count  = 0
    for skill, keywords in skill_keywords.items():
        count = sum(1 for kw in keywords if kw in description)
        if count > best_count:
            best_count = count
            best_skill = skill

    confidence = min(best_count * 20, 85) if best_count > 0 else 40
    return {
        'skill':      best_skill,
        'confidence': confidence,
        'reasoning':  'Detected via keyword analysis (AI fallback mode).'
    }


def get_matching_workers(skill: str, limit: int = 5) -> list:
    """
    Fetch available workers from DB matching the detected skill.
    Returns list of worker dicts.
    """
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT w.id AS worker_id, u.name, u.phone, u.city,
               w.skill_category, w.experience_years, w.address,
               w.description, w.availability, w.rating, w.total_jobs
        FROM workers w
        JOIN users u ON w.user_id = u.id
        WHERE LOWER(w.skill_category) = LOWER(%s)
          AND w.availability != 'offline'
        ORDER BY w.rating DESC, w.total_jobs DESC
        LIMIT %s
    """, (skill, limit))
    workers = cur.fetchall()
    cur.close()
    return workers


# ============================================================
# AUTH ROUTES
# ============================================================

@app.route('/')
def home():
    """Landing page."""
    # Quick stats for the homepage
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) AS cnt FROM workers")
    total_workers = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) AS cnt FROM jobs")
    total_jobs = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) AS cnt FROM users WHERE role = 'client'")
    total_clients = cur.fetchone()['cnt']
    cur.close()
    return render_template('index.html',
                           total_workers=total_workers,
                           total_jobs=total_jobs,
                           total_clients=total_clients)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration (client or worker)."""
    if request.method == 'POST':
        name     = request.form['name'].strip()
        email    = request.form['email'].strip().lower()
        password = request.form['password']
        role     = request.form['role']          # 'client' or 'worker'
        phone    = request.form.get('phone', '')

        # ── Basic validation ────────────────────────────────
        if not all([name, email, password, role]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return redirect(url_for('register'))

        # ── Check duplicate email ───────────────────────────
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            flash('Email already registered. Please login.', 'warning')
            cur.close()
            return redirect(url_for('login'))

        # ── Insert user ─────────────────────────────────────
        hashed_pw = generate_password_hash(password)
        cur.execute(
            "INSERT INTO users (name, email, password, role, phone) VALUES (%s,%s,%s,%s,%s)",
            (name, email, hashed_pw, role, phone)
        )
        mysql.connection.commit()
        user_id = cur.lastrowid

        # ── If worker, create empty worker profile ──────────
        if role == 'worker':
            cur.execute(
                "INSERT INTO workers (user_id, skill_category) VALUES (%s, %s)",
                (user_id, 'Other')
            )
            mysql.connection.commit()

        cur.close()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        email    = request.form['email'].strip().lower()
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user['password'], password):
            # ── Store user info in session ──────────────────
            session['user_id']   = user['id']
            session['user_name'] = user['name']
            session['user_role'] = user['role']

            flash(f"Welcome back, {user['name']}!", 'success')

            # Redirect based on role
            if user['role'] == 'worker':
                return redirect(url_for('worker_dashboard'))
            else:
                return redirect(url_for('client_dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Clear session and redirect to login."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# ============================================================
# CLIENT ROUTES
# ============================================================

@app.route('/client/dashboard')
@login_required
def client_dashboard():
    """Client dashboard — recent jobs and matches."""
    if session['user_role'] != 'client':
        return redirect(url_for('worker_dashboard'))

    cur = mysql.connection.cursor()

    # Recent jobs by this client
    cur.execute("""
        SELECT j.*, COUNT(am.id) AS match_count
        FROM jobs j
        LEFT JOIN ai_matches am ON j.id = am.job_id
        WHERE j.client_id = %s
        GROUP BY j.id
        ORDER BY j.posted_at DESC
        LIMIT 10
    """, (session['user_id'],))
    jobs = cur.fetchall()

    # Summary stats
    cur.execute("SELECT COUNT(*) AS cnt FROM jobs WHERE client_id = %s", (session['user_id'],))
    total_jobs = cur.fetchone()['cnt']

    cur.execute("SELECT COUNT(*) AS cnt FROM jobs WHERE client_id = %s AND status='completed'",
                (session['user_id'],))
    completed_jobs = cur.fetchone()['cnt']

    cur.close()
    return render_template('client_dashboard.html',
                           jobs=jobs,
                           total_jobs=total_jobs,
                           completed_jobs=completed_jobs)


@app.route('/client/post-job', methods=['GET', 'POST'])
@login_required
def post_job():
    """Client posts a new job — AI skill matching happens here."""
    if session['user_role'] != 'client':
        return redirect(url_for('worker_dashboard'))

    if request.method == 'POST':
        description = request.form['description'].strip()
        location    = request.form.get('location', 'Bhopal').strip()
        title       = request.form.get('title', '').strip()

        if not description:
            flash('Please describe what work you need.', 'danger')
            return redirect(url_for('post_job'))

        # ── Step 1: AI extracts required skill ─────────────
        ai_result = extract_skill_with_ai(description)
        detected_skill = ai_result.get('skill', 'Other')
        confidence     = ai_result.get('confidence', 0)
        reasoning      = ai_result.get('reasoning', '')

        # ── Step 2: Save job to database ────────────────────
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO jobs (client_id, title, description, location,
                              ai_detected_skill, status)
            VALUES (%s, %s, %s, %s, %s, 'open')
        """, (session['user_id'], title or description[:60],
              description, location, detected_skill))
        mysql.connection.commit()
        job_id = cur.lastrowid

        # ── Step 3: Find matching workers ───────────────────
        matched_workers = get_matching_workers(detected_skill, limit=5)

        # ── Step 4: Save match results ──────────────────────
        for i, worker in enumerate(matched_workers):
            # Assign match scores — top worker gets highest score
            match_score = max(confidence - (i * 5), 10)
            cur.execute("""
                INSERT INTO ai_matches (job_id, worker_id, match_score)
                VALUES (%s, %s, %s)
            """, (job_id, worker['worker_id'], match_score))

        # Update job status to 'matched' if workers found
        if matched_workers:
            cur.execute("UPDATE jobs SET status='matched' WHERE id=%s", (job_id,))

        mysql.connection.commit()
        cur.close()

        return render_template('match_results.html',
                               job_id=job_id,
                               description=description,
                               detected_skill=detected_skill,
                               confidence=confidence,
                               reasoning=reasoning,
                               matched_workers=matched_workers)

    return render_template('post_job.html')


# ============================================================
# WORKER ROUTES
# ============================================================

@app.route('/worker/dashboard')
@login_required
def worker_dashboard():
    """Worker dashboard — profile overview and job matches."""
    if session['user_role'] != 'worker':
        return redirect(url_for('client_dashboard'))

    cur = mysql.connection.cursor()

    # Get worker profile
    cur.execute("""
        SELECT w.*, u.name, u.email, u.phone, u.city
        FROM workers w JOIN users u ON w.user_id = u.id
        WHERE w.user_id = %s
    """, (session['user_id'],))
    profile = cur.fetchone()

    # Recent job matches for this worker
    cur.execute("""
        SELECT j.title, j.description, j.location, j.ai_detected_skill,
               j.posted_at, am.match_score, u.name AS client_name, u.phone AS client_phone
        FROM ai_matches am
        JOIN jobs j ON am.job_id = j.id
        JOIN users u ON j.client_id = u.id
        WHERE am.worker_id = %s
        ORDER BY am.matched_at DESC
        LIMIT 10
    """, (profile['id'],))
    job_matches = cur.fetchall()

    cur.close()
    return render_template('worker_dashboard.html',
                           profile=profile,
                           job_matches=job_matches)


@app.route('/worker/update-profile', methods=['GET', 'POST'])
@login_required
def update_worker_profile():
    """Worker updates their skill profile."""
    if session['user_role'] != 'worker':
        return redirect(url_for('client_dashboard'))

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        skill        = request.form['skill_category']
        experience   = request.form.get('experience_years', 0)
        address      = request.form.get('address', '')
        description  = request.form.get('description', '')
        availability = request.form.get('availability', 'available')
        phone        = request.form.get('phone', '')

        # Update worker table
        cur.execute("""
            UPDATE workers
            SET skill_category=%s, experience_years=%s,
                address=%s, description=%s, availability=%s
            WHERE user_id=%s
        """, (skill, experience, address, description,
              availability, session['user_id']))

        # Update phone in users table
        cur.execute("UPDATE users SET phone=%s WHERE id=%s",
                    (phone, session['user_id']))

        mysql.connection.commit()
        cur.close()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('worker_dashboard'))

    # GET — pre-fill form
    cur.execute("""
        SELECT w.*, u.name, u.email, u.phone
        FROM workers w JOIN users u ON w.user_id = u.id
        WHERE w.user_id = %s
    """, (session['user_id'],))
    profile = cur.fetchone()
    cur.close()
    return render_template('update_profile.html', profile=profile)


# ============================================================
# BROWSE WORKERS (Public)
# ============================================================

@app.route('/workers')
def browse_workers():
    """Public page to browse all available workers."""
    skill_filter = request.args.get('skill', '')
    search_query = request.args.get('q', '')

    cur = mysql.connection.cursor()
    if skill_filter:
        cur.execute("""
            SELECT w.*, u.name, u.phone, u.city
            FROM workers w JOIN users u ON w.user_id = u.id
            WHERE LOWER(w.skill_category) = LOWER(%s)
              AND w.availability != 'offline'
            ORDER BY w.rating DESC
        """, (skill_filter,))
    elif search_query:
        like = f'%{search_query}%'
        cur.execute("""
            SELECT w.*, u.name, u.phone, u.city
            FROM workers w JOIN users u ON w.user_id = u.id
            WHERE (w.skill_category LIKE %s OR u.name LIKE %s
                   OR w.description LIKE %s)
              AND w.availability != 'offline'
            ORDER BY w.rating DESC
        """, (like, like, like))
    else:
        cur.execute("""
            SELECT w.*, u.name, u.phone, u.city
            FROM workers w JOIN users u ON w.user_id = u.id
            WHERE w.availability != 'offline'
            ORDER BY w.rating DESC
        """)

    workers = cur.fetchall()

    # Skill categories for filter dropdown
    cur.execute("SELECT DISTINCT skill_category FROM workers ORDER BY skill_category")
    categories = [r['skill_category'] for r in cur.fetchall()]
    cur.close()

    return render_template('browse_workers.html',
                           workers=workers,
                           categories=categories,
                           skill_filter=skill_filter,
                           search_query=search_query)


# ============================================================
# ADMIN / ANALYTICS
# ============================================================

@app.route('/admin')
@login_required
def admin_dashboard():
    """Overview analytics page (accessible to any logged-in user in MVP)."""
    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) AS cnt FROM users WHERE role='client'")
    total_clients = cur.fetchone()['cnt']

    cur.execute("SELECT COUNT(*) AS cnt FROM workers")
    total_workers = cur.fetchone()['cnt']

    cur.execute("SELECT COUNT(*) AS cnt FROM jobs")
    total_jobs = cur.fetchone()['cnt']

    cur.execute("SELECT COUNT(*) AS cnt FROM ai_matches")
    total_matches = cur.fetchone()['cnt']

    # Jobs by status breakdown
    cur.execute("""
        SELECT status, COUNT(*) AS cnt FROM jobs GROUP BY status
    """)
    job_status_rows = cur.fetchall()
    job_status = {r['status']: r['cnt'] for r in job_status_rows}

    # Top workers by rating
    cur.execute("""
        SELECT u.name, w.skill_category, w.rating, w.total_jobs, w.availability
        FROM workers w JOIN users u ON w.user_id = u.id
        ORDER BY w.rating DESC LIMIT 6
    """)
    top_workers = cur.fetchall()

    # Recent jobs
    cur.execute("""
        SELECT j.title, j.ai_detected_skill, j.status, j.posted_at, u.name AS client
        FROM jobs j JOIN users u ON j.client_id = u.id
        ORDER BY j.posted_at DESC LIMIT 8
    """)
    recent_jobs = cur.fetchall()

    # Skill distribution
    cur.execute("""
        SELECT skill_category, COUNT(*) AS cnt
        FROM workers GROUP BY skill_category ORDER BY cnt DESC
    """)
    skill_dist = cur.fetchall()

    cur.close()
    return render_template('admin_dashboard.html',
                           total_clients=total_clients,
                           total_workers=total_workers,
                           total_jobs=total_jobs,
                           total_matches=total_matches,
                           job_status=job_status,
                           top_workers=top_workers,
                           recent_jobs=recent_jobs,
                           skill_dist=skill_dist)


# ============================================================
# API ENDPOINT — AJAX skill detection preview
# ============================================================

@app.route('/api/detect-skill', methods=['POST'])
def api_detect_skill():
    """
    AJAX endpoint: returns detected skill for a job description.
    Used for live preview on the job posting form.
    """
    data = request.get_json()
    if not data or not data.get('description'):
        return jsonify({'error': 'No description provided'}), 400

    result = extract_skill_with_ai(data['description'])
    return jsonify(result)


# ============================================================
# RATE A WORKER
# ============================================================

@app.route('/rate-worker/<int:job_id>/<int:worker_id>', methods=['POST'])
@login_required
def rate_worker(job_id, worker_id):
    """Client submits rating for a worker."""
    rating = int(request.form.get('rating', 5))
    review = request.form.get('review', '')

    cur = mysql.connection.cursor()

    # Save rating
    cur.execute("""
        INSERT INTO ratings (job_id, client_id, worker_id, rating, review)
        VALUES (%s, %s, %s, %s, %s)
    """, (job_id, session['user_id'], worker_id, rating, review))

    # Recalculate worker's average rating
    cur.execute("""
        SELECT AVG(rating) AS avg_r, COUNT(*) AS cnt
        FROM ratings WHERE worker_id = %s
    """, (worker_id,))
    stats = cur.fetchone()

    cur.execute("""
        UPDATE workers SET rating=%s, total_jobs=%s WHERE id=%s
    """, (round(stats['avg_r'], 2), stats['cnt'], worker_id))

    # Mark job as completed
    cur.execute("UPDATE jobs SET status='completed' WHERE id=%s", (job_id,))

    mysql.connection.commit()
    cur.close()

    flash('Thank you for your rating!', 'success')
    return redirect(url_for('client_dashboard'))


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('404.html'), 500   # reuse for MVP simplicity


# ============================================================
# RUN
# ============================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
