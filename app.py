from app import create_app

app = create_app()

if __name__ == "__main__":
    # For local dev: `python app.py`
    # In Docker we’ll use gunicorn (see Dockerfile)
    app.run(host="0.0.0.0", port=5000)
