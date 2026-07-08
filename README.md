# Engel & Volkers — Streamlit App

Docker deployment instructions

Build the Docker image:

```bash
docker build -t engel-volkers-app .
```

Run locally (map port 8501):

```bash
docker run -e PORT=8501 -p 8501:8501 engel-volkers-app
```

Open http://localhost:8501 in your browser.

To push to Docker Hub:

```bash
docker tag engel-volkers-app yourdockerhubusername/engel-volkers-app:latest
docker push yourdockerhubusername/engel-volkers-app:latest
```

Notes:
- The container runs `streamlit run app.py` and listens on `$PORT` (default 8501).
- If your app reads Excel files, ensure the uploaded file types are supported (xlsx requires `openpyxl`).
