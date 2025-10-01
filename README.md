# Chhota Savings + Credit Builder (API-first Backend)

A secure, scalable, API-first backend for micro-savings, gamified streaks, and AI-driven credit scores.

## Key Features

- **API-first**: Frontend-agnostic design for easy integration.
- **Secure**: JWT authentication, password hashing (Argon2), input validation.
- **Scalable**: Redis caching, Celery background tasks.
- **AI-powered**: Rule-based credit scoring with modular ML engine.
- **Gamified**: Streak tracking and badges for user engagement.

2. Tech Stack
Layer	Technology / Tools
Backend	Python, Django, Django REST Framework (DRF)
Database	PostgreSQL
Cache	Redis
AI / ML	Python scikit-learn / TensorFlow Lite (for predictions)
File Storage	AWS S3 (KYC / media)
Background Jobs	Celery (with Redis broker)
API Auth	JWT + optional OAuth2
Monitoring	Sentry, Prometheus, Grafana (optional)
Hosting	AWS Free Tier (EC2 + RDS + S3)
3. System Architecture
           ┌────────────────────┐
           │   Mobile / Web UI  │
           │  (React Native)    │
           └─────────▲──────────┘
                     │ REST API Calls
                     ▼
           ┌────────────────────┐
           │  Django Backend    │
           │ (DRF + JWT Auth)  │
           └─────────▲──────────┘
      ┌───────────────┼────────────────┐
      │               │                │
┌─────┴───────┐ ┌─────┴───────┐ ┌─────┴───────┐
│ User Module │ │ Savings Jar │ │ Gamification │
│ - Signup    │ │ Module      │ │ Module      │
│ - Login     │ │ - CRUD jars │ │ - Streaks  │
│ - Profile   │ │ - Deposit   │ │ - Badges   │
│ - KYC      │ │ - Withdraw   │ │ - Leaderboards│
└─────▲───────┘ └─────▲───────┘ └─────▲───────┘
      │               │                │
      └─────┐         │         ┌──────┘
            ▼         ▼         ▼
       ┌───────────────────────────────┐
       │      Credit Score Engine       │
       │  (AI / ML + Rule-Based Logic) │
       │  - Predicts saving behavior   │
       │  - Generates alternate score  │
       │  - Loan eligibility API       │
       └─────────────▲─────────────────┘
                     │
                     ▼
          ┌───────────────────┐
          │   Background Jobs │
          │  (Celery + Redis)│
          │ - Notifications  │
          │ - Score updates  │
          │ - Streak updates │
          └─────────▲─────────┘
                    │
      ┌─────────────┴─────────────┐
      │                           │
┌─────┴───────┐             ┌─────┴───────┐
│ PostgreSQL  │             │ Redis Cache │
│ - Users     │             │ - Streaks  │
│ - Transactions│           │ - Sessions │
│ - Jars     │             │ - Quick lookup│
│ - Scores   │             └─────────────┘
└────────────┘
      │
      ▼
┌──────────────┐
│ S3 Bucket    │
│ - KYC Docs   │
│ - User Media │
└──────────────┘

4. Database Schema (PostgreSQL)
Users
id | name | email | phone | password_hash | kyc_file | created_at

SavingsJar
id | user_id | plan_type | target_amount | current_amount | start_date | end_date | streak_count

Transactions
id | user_id | jar_id | type(deposit/withdraw) | amount | date

CreditScore
id | user_id | score | predicted_score | last_updated

Badges
id | user_id | badge_type | earned_at

5. API Endpoints
User Module

POST /api/signup/ → Signup new user

POST /api/login/ → Login + JWT token

GET /api/profile/ → Get user profile

PUT /api/profile/ → Update profile

POST /api/kyc-upload/ → Upload KYC to S3

Savings Jar

POST /api/jars/ → Create jar

GET /api/jars/ → List jars

POST /api/jars/deposit/ → Deposit money

POST /api/jars/withdraw/ → Withdraw

Gamification

GET /api/streaks/ → Get current streak

GET /api/badges/ → List earned badges

Credit Score / AI

GET /api/credit-score/ → Fetch current score

POST /api/predict-score/ → Admin triggers batch predictions

Admin

GET /api/admin/users/ → List users

GET /api/admin/transactions/ → All transactions

POST /api/admin/recalculate-scores/ → Re-run AI engine

6. Background Jobs (Celery + Redis)

Tasks:

Daily streak updates

Daily/weekly credit score calculation

Notifications / emails

Cache updates in Redis

Celery Broker & Backend: Redis

Example Task:

@celery.task
def update_credit_score(user_id):
    score = calculate_score(user_id)
    redis.set(f"user:{user_id}:score", score)
    postgres.update_score(user_id, score)

7. AI / ML Integration

Credit Score Logic:

Input: deposits, streaks, repayment history

Rule-based scoring for MVP (points per deposit / streak)

 ML model:

Predict probability of on-time deposit

Generate “predicted_score”

Output: persisted in PostgreSQL, cached in Redis

Model Storage: Local pickle / serialized in Django project
API Endpoint: /api/predict-score/

8. Caching (Redis)

Data Cached:

User streaks → fast retrieval for frontend

Credit scores → avoids recalculation on every request

Session tokens / JWT blacklisting

Django Integration:

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
    }
}

9. AWS Free Tier Optimization
Component	Free Tier Usage
EC2 t2.micro	Django backend (750 hrs/month)
RDS PostgreSQL	20GB storage, single instance
S3 Bucket	Store KYC, small media (few MB)
Redis	Run locally → no AWS cost
Celery	Local broker → no cost

With 0–100 users, this backend costs nothing from your pocket.

10. Development Roadmap
1: Core Backend

Django + PostgreSQL setup

User auth, profile, KYC upload

Savings Jar CRUD APIs

2: Gamification & AI Engine

Implement streak tracking, badges

Rule-based credit score

Transactions & caching in Redis

3: Loan Simulation & Admin Panel

Dummy loan unlocks

Admin dashboard (React / DRF browsable API)

API documentation + Postman collection

 4: Demo & Polish

Basic frontend screens

Notifications + background tasks

Testing, bug fixing, performance optimization

11. Security Measures

HTTPS / TLS everywhere

Password hashing (Argon2 / bcrypt)

JWT auth + optional OAuth2

Role-based access control

Input validation & rate limiting

Optional: penetration testing before pitch

12. Notes for AI Implementation

Build modular Django apps: user, savings, gamification, credit, admin

All functionality via API → frontend independent

Redis for caching, PostgreSQL for persistence

S3 for files, optional at MVP

Celery for background tasks

AI module should be pluggable, can start with rules and replace with ML later

Focus on backend first, frontend is only a demo