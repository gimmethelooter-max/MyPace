# MyPace

A warm, calming product discovery PWA for people living with pacemakers. MyPace surfaces products that have been screened for compatibility considerations, but it never guarantees universal safety. Always confirm product guidance with your device manufacturer or clinician.

## Run locally

```bash
python -m uvicorn backend.server:app --reload --port 8001
```

Serve the frontend with any static server, or open `frontend/index.html` directly for the local-data fallback.

## API

- `GET /api/products?category=&q=`
- `GET /api/products/{id}`
- `GET /api/categories`
- `GET /api/safety-tips`
- `GET /api/wellness-tips`

MongoDB is optional. Set `MONGO_URL` and `DB_NAME` to use MongoDB; otherwise the API uses the curated in-memory seed catalog.
