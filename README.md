# Backend Notes

A curated collection of backend development notes, examples, and a small FastAPI sample application — useful as a personal reference while learning backend engineering concepts and building small prototypes.

---

## Table of contents
- [What this is](#what-this-is)
- [Stack](#stack)
- [Repository layout](#repository-layout)
- [FastAPI sample app — quick start](#fastapi-sample-app---quick-start)
- [Notes & reference materials](#notes--reference-materials)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## What this is
Practical learning resources for backend technologies, including PDF/ DOCX notes on Python, MongoDB, TLS, and more, plus a small FastAPI example (in `fastapi_codewithharry`) demonstrating templates, static files, routes, and simple models.

### Stack
- Language(s): Python (primary), HTML, CSS  
- Framework / runtime: FastAPI + Uvicorn (sample app)
- Notable libraries: see `fastapi_codewithharry/pyproject.toml` for exact dependencies (the sample app uses FastAPI/Uvicorn and standard template/static tooling)

## Repository layout
Top-level entries:
```
Advance_python_notes.pdf              # In-depth Python notes
HTTPS_and_TLS_Handshake.docx          # Notes on TLS/HTTPS
MongoDB Handbook.pdf                  # MongoDB reference
TOML.docx                             # TOML format notes
asyncio_module.docx                   # asyncio reference
pipe_operator.docx                    # Pipe operator / functional helpers
requests_module.docx                  # requests usage notes
fastapi_codewithharry/                # Small FastAPI sample project (app, routes, templates, static)
```

fastapi_codewithharry/ (sample app)
```
.fastapi_codewithharry/.gitignore
.fastapi_codewithharry/.python-version
.fastapi_codewithharry/pyproject.toml   # Project manifest (dependencies)
.fastapi_codewithharry/uv.lock          # Dependency lock file
.fastapi_codewithharry/main.py          # App entrypoint (FastAPI app)
.fastapi_codewithharry/index.py         # Mounts static files / app setup
.fastapi_codewithharry/config/db.py     # DB configuration / connection helper
.fastapi_codewithharry/models/note.py   # Simple model for notes
.fastapi_codewithharry/schema/note.py   # Pydantic/schema definitions
.fastapi_codewithharry/routes/note.py   # CRUD routes / handlers for notes
.fastapi_codewithharry/templates/       # HTML templates (examples)
fastapi_codewithharry/templates/db_test.html
fastapi_codewithharry/templates/item.html
.fastapi_codewithharry/static/styles.css # Styles for templates
```

How it fits together:
- The `fastapi_codewithharry` folder contains a compact FastAPI example: route handlers live under `routes/`, data model/schema under `models/` and `schema/`, DB configuration in `config/`, and the templating/static assets under `templates/` and `static/`. The app is launched from `main.py`.

## FastAPI sample app — quick start
1. Clone the repo and change directory into the sample app:
```bash
git clone https://github.com/KamranRizvi265/Backend_Notes.git
cd Backend_Notes/fastapi_codewithharry
```

2. Install dependencies
- If you use Poetry:
```bash
poetry install
poetry run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
- If you use virtualenv + pip:
```bash
python -m venv .venv
# Activate the venv (Linux/macOS)
source .venv/bin/activate
# or on Windows PowerShell
.venv\Scripts\Activate.ps1

# Install dependencies listed in pyproject.toml (or manually):
pip install fastapi uvicorn jinja2
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

3. Open the app in your browser:
- Visit http://127.0.0.1:8000 (or the routes defined in `fastapi_codewithharry/routes/note.py`)
- The `templates/` and `static/` folders provide simple HTML examples.

Notes:
- Check `fastapi_codewithharry/pyproject.toml` (and `uv.lock`) for the authoritative dependency list and preferred install method.
- Check `fastapi_codewithharry/config/db.py` for database configuration; set any required environment variables if you want to connect to an external DB.

## Notes & reference materials
This repository includes a set of study notes and handbooks you may find useful:
- Advance_python_notes.pdf
- MongoDB Handbook.pdf
- HTTPS_and_TLS_Handshake.docx
- asyncio_module.docx
- requests_module.docx
- TOML.docx
- pipe_operator.docx

These are reference materials for personal learning and quick lookup.

## Contributing
- This repository is primarily a personal learning resource. If you'd like to contribute:
  - Open an issue describing the change you propose.
  - Send a small, focused pull request with a clear description.
  - Keep changes to the `fastapi_codewithharry` example isolated and documented.

## License
No license file detected. If you intend to share or accept contributions, add a LICENSE (for example, MIT) to make the terms explicit.

## Contact
Repository: https://github.com/KamranRizvi265/Backend_Notes

If you want, I can commit this README.md to the repository for you or suggest edits to tailor wording, add badges, or include examples of endpoints from `routes/note.py`.