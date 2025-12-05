IncByteLogic — Upside Cybersecurity Demo

Overview
- Static frontend demo of an Upside-style cybersecurity landing site located in `public/`.
- Client-side persistence uses `localStorage` for demo login, contact messages and `service-requests` (requests saved from `request-form.html`).
- A simple Python fallback API server is available as `server.py` (if Python is installed).

Quick local test (static files only)
1. Open `public/index.html` in your browser (double-click the file or drag to browser).
2. To run a local static server (recommended) with Python 3 installed:

```powershell
cd "c:\Users\frajq\OneDrive\Desktop\jjjjjj\public"
python -m http.server 8000
# Then open http://localhost:8000
```

Python fallback API server (optional)
- If you want API endpoints and a small demo DB, run `server.py` (requires Python 3).

```powershell
cd "c:\Users\frajq\OneDrive\Desktop\jjjjjj"
python server.py
# Server listens on http://localhost:3000 and serves the frontend from the 'public' folder
```

Notes about environment
- The project contains prepared Node.js server files in some branches, but this repo uses a Python fallback (`server.py`). If you'd rather run a Node/Express server, install Node.js (LTS) and I can provide `server.js` and `package.json` adjustments.
- The demo stores a plaintext demo user for convenience: `demo@incbytelogic.local` / `DemoPass123`. Do not use this for production.

Next steps I can do for you (pick any, or I'll proceed):
- Enable a Node.js backend and add secure password hashing and email notifications.
- Tune the per-service pricing multipliers.
- Polish UI/RTL layout and accessibility checks.

Contact
- incbytelogic@gmail.com — عمان، الأردن — واتس: 0780502944
