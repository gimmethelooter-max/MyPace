from __future__ import annotations

import os
from typing import Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

try:
    from pymongo import MongoClient
except ImportError:  # local frontend-only installs do not need MongoDB
    MongoClient = None

app = FastAPI(title="MyPace API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

PRODUCTS: list[dict[str, Any]] = [
    {"id":"p1","name":"Cotton Calm Weighted Blanket","category":"Home comfort","price":49.99,"rating":4.8,"reviewed":"No electronics or magnets","image":"https://images.unsplash.com/photo-1600369671236-e74521d4b6ad?auto=format&fit=crop&w=800&q=80","description":"A breathable, machine-washable cotton blanket for a restful wind-down routine.","amazon_url":"https://www.amazon.com/s?k=cotton+weighted+blanket","status":"screened"},
    {"id":"p2","name":"Ceramic Tea & Infuser Set","category":"Wellness","price":24.95,"rating":4.7,"reviewed":"Non-electronic kitchenware","image":"https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=800&q=80","description":"A simple ceramic set for herbal tea rituals and mindful pauses.","amazon_url":"https://www.amazon.com/s?k=ceramic+tea+infuser","status":"screened"},
    {"id":"p3","name":"Cork Yoga & Stretch Mat","category":"Movement","price":38.00,"rating":4.6,"reviewed":"No electronics or magnets","image":"https://images.unsplash.com/photo-1599447421416-3414500d18a5?auto=format&fit=crop&w=800&q=80","description":"A supportive, non-slip surface for gentle stretching and clinician-approved movement.","amazon_url":"https://www.amazon.com/s?k=cork+yoga+mat","status":"screened"},
    {"id":"p4","name":"Analog Kitchen Timer","category":"Home comfort","price":12.49,"rating":4.5,"reviewed":"Battery-free mechanical timer","image":"https://images.unsplash.com/photo-1556911220-bff31c812dba?auto=format&fit=crop&w=800&q=80","description":"A clear, easy-to-read timer with no wireless connectivity.","amazon_url":"https://www.amazon.com/s?k=analog+kitchen+timer","status":"screened"},
    {"id":"p5","name":"Soft Cotton Walking Socks","category":"Movement","price":16.99,"rating":4.8,"reviewed":"Textile product; no electronics","image":"https://images.unsplash.com/photo-1582966772680-860e372bb558?auto=format&fit=crop&w=800&q=80","description":"Breathable everyday socks for comfortable walks and routines.","amazon_url":"https://www.amazon.com/s?k=cotton+walking+socks","status":"screened"},
    {"id":"p6","name":"Breathing Exercise Cards","category":"Mindfulness","price":14.00,"rating":4.9,"reviewed":"Paper-based wellness aid","image":"https://images.unsplash.com/photo-1499209974431-9dddcece7f88?auto=format&fit=crop&w=800&q=80","description":"A pocket deck of gentle breathing prompts for calm moments.","amazon_url":"https://www.amazon.com/s?k=breathing+exercise+cards","status":"screened"},
    {"id":"p7","name":"Large-Print Journal","category":"Mindfulness","price":11.95,"rating":4.7,"reviewed":"Paper product; no electronics","image":"https://images.unsplash.com/photo-1517842645767-c639042777db?auto=format&fit=crop&w=800&q=80","description":"A friendly large-print journal for gratitude, questions, and daily notes.","amazon_url":"https://www.amazon.com/s?k=large+print+journal","status":"screened"},
    {"id":"p8","name":"Woodland Reading Lamp","category":"Home comfort","price":32.99,"rating":4.4,"reviewed":"Use at recommended distance; no wireless function","image":"https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=80","description":"A warm bedside lamp with a straightforward corded design.","amazon_url":"https://www.amazon.com/s?k=corded+bedside+reading+lamp","status":"review"},
]

CATEGORIES = ["All","Home comfort","Wellness","Movement","Mindfulness"]
SAFETY = [
    {"title":"Keep magnets and strong magnetic fields at a distance","body":"Some magnets, magnetic therapy products, and strong electromagnetic sources can affect implanted devices. Follow the distance guidance in your device manual and ask your clinic about anything uncertain."},
    {"title":"Check wireless and electrical products before use","body":"Compatibility can depend on model, power, distance, and how an item is used. Product labels here are screening notes—not a medical clearance."},
    {"title":"Carry your device identification","body":"Keep your device card and care team's contact details accessible, especially when travelling or attending appointments."},
    {"title":"When in doubt, pause and ask","body":"Do not use a product that causes symptoms or feels uncertain. Contact your cardiology team or device manufacturer for personalized advice."},
]
WELLNESS = [
    {"kind":"do","title":"Take gentle, approved movement breaks","body":"Short walks, stretching, and breathing pauses can support wellbeing when they fit your care plan."},
    {"kind":"do","title":"Create a calming routine","body":"Try a warm drink, quiet music, journaling, or a consistent bedtime wind-down."},
    {"kind":"dont","title":"Don't ignore new symptoms","body":"Stop and seek medical advice for concerning symptoms such as fainting, chest pain, severe breathlessness, or unusual palpitations."},
    {"kind":"dont","title":"Don't assume every product is universal","body":"Device models and personal circumstances differ. Use MyPace as a convenience filter, then verify important purchases."},
]

mongo_products = None
@app.on_event("startup")
def seed() -> None:
    global mongo_products
    url = os.getenv("MONGO_URL")
    if MongoClient and url:
        try:
            client = MongoClient(url, serverSelectionTimeoutMS=1500)
            client.admin.command("ping")
            collection = client[os.getenv("DB_NAME", "mypace")]["products"]
            if collection.count_documents({}) == 0:
                collection.insert_many(PRODUCTS)
            mongo_products = collection
        except Exception:
            mongo_products = None

def catalog() -> list[dict[str, Any]]:
    return list(mongo_products.find({}, {"_id": 0})) if mongo_products is not None else PRODUCTS

@app.get("/api/products")
def products(category: str | None = None, q: str | None = Query(default=None, min_length=1)):
    result = catalog()
    if category and category != "All": result = [p for p in result if p["category"] == category]
    if q: result = [p for p in result if q.lower() in (p["name"] + " " + p["description"] + " " + p["category"]).lower()]
    return result

@app.get("/api/products/{product_id}")
def product(product_id: str):
    item = next((p for p in catalog() if p["id"] == product_id), None)
    if not item: raise HTTPException(404, "Product not found")
    return item

@app.get("/api/categories")
def categories(): return CATEGORIES
@app.get("/api/safety-tips")
def safety_tips(): return SAFETY
@app.get("/api/wellness-tips")
def wellness_tips(): return WELLNESS
