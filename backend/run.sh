# uv run fastapi dev app/main.py
# source .venv/bin/activate if not using venv already
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload