# Inventory API (Flask + JWT + SQLite)

A small-but-real Flask application with JWT auth, CRUD endpoints, Marshmallow validation, tests, Docker, and GitHub Actions.

## Quickstart (local)

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask db init
flask db migrate -m "init"
flask db upgrade
python -c "from app import create_app; from app.extensions import db; from app.seed import seed_basic; app=create_app(); 
from app.extensions import db as _db; 
from app.models import *; 
app.app_context().push(); seed_basic()"
python app.py
