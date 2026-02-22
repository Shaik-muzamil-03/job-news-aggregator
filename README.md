## Plan: AI Job Aggregator Backend (Python, Postgres, SQLAlchemy)

Build a backend service that scrapes job posts from Indeed and We Work Remotely for specified profiles, stores them in a Postgres database, and emails a daily digest. The stack uses Python (FastAPI recommended), SQLAlchemy ORM, and a task scheduler (e.g., Celery or APScheduler). The design ensures modularity for future expansion (e.g., more sources, user management).

**Docker Integration**

This project is designed to run in Docker containers for both the backend app and the Postgres database. All dependencies and services are orchestrated using `docker-compose` for easy local development and deployment.

### Quick Start with Docker

1. **Build and start all services:**

   ```sh
   docker-compose up --build
   ```

   This will start both the backend app and a Postgres database. The app will be available at http://localhost:8000 and Postgres at localhost:5432.

2. **Environment Variables:**
   - Configuration (such as the database URL) is managed via environment variables. See the provided `.env` file for an example.

3. **Stopping services:**

   ```sh
   docker-compose down
   ```

4. **Running database migrations:**
   (Add migration instructions here if using Alembic or similar.)

---

**Steps**

1. **Project Structure & Dependencies**
   - Organize codebase (app, models, scrapers, email, scheduler, config)
   - Define dependencies in [pyproject.toml](job-news-aggregator/pyproject.toml) (FastAPI/Flask, SQLAlchemy, psycopg2, requests/selenium, email libraries, scheduler)
2. **Database Design**
   - Use SQLAlchemy to define tables: `User`, `Profile`, `JobPost`, `ScrapeLog`
   - Set up Postgres connection and migration scripts
   - All database operations are performed against the Postgres container defined in `docker-compose.yml`.
3. **Scraping Module**
   - Implement scrapers for Indeed and We Work Remotely (requests/selenium, handle login/captcha if needed)
   - Support Google login for authentication if the option is available on the platform
   - Parse and normalize job post data
   - Store new posts in the database, avoid duplicates
4. **Email Notification System**
   - Compose daily email digests (Jinja2 templates or similar)
   - Integrate with SMTP or email API (e.g., SendGrid)
   - Track sent emails/logs
5. **Scheduler**
   - Use Celery (with Redis/RabbitMQ) or APScheduler for periodic scraping and emailing
   - Ensure tasks run every 24 hours per user/profile
6. **API Layer (Optional, for extensibility)**
   - REST API for managing users, profiles, and viewing job posts
   - Authentication (JWT or similar) if multi-user
7. **Configuration & Secrets**
   - Use environment variables or config files for DB, email, and API keys
   - Securely manage credentials
8. **Testing & Logging**
   - Add unit/integration tests for scrapers, email, and DB logic
   - Implement logging for monitoring and debugging

**Verification**

- Run end-to-end: add a profile, trigger scrape, verify DB entries, receive email
- Unit tests for each module (scraper, email, DB)
- Manual checks for edge cases (login failures, email delivery, duplicate posts)
- Test the full stack by running all services with Docker Compose

**Decisions**

- Use SQLAlchemy ORM for DB abstraction
- Celery preferred for robust scheduling (APScheduler as lightweight alternative)
- FastAPI recommended for future-proofing/extensibility
- Selenium for scraping if login/captcha required; requests/BeautifulSoup otherwise
- Email via SMTP or SendGrid for reliability
