# Best Contractors in Twin Cities

Homeowner landing page and lead intake for exclusive contractor matching.

## Files
- `best_contractors.py` — Flask server
- `best_contractors_twin_cities.html` — landing page
- `requirements.txt` — Flask, gunicorn
- `Procfile` — Railway start command

## Run locally
```bash
pip install -r requirements.txt
python best_contractors.py
```
Open http://127.0.0.1:5000

## Railway
Connect this repo and deploy. Railway will use the Procfile automatically.

## Lead view
Submitted leads are visible at `/leads` (in-memory for now).
