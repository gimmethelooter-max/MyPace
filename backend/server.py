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
    {
        "id": "p1",
        "name": "Cotton Calm Weighted Blanket",
        "category": "Home comfort",
        "price": 49.99,
        "rating": 4.8,
        "reviewed": "No electronics or magnets",
        "image": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80",
        "description": "A soft, breathable blanket designed to add a gentle sense of comfort during rest and wind-down time.",
        "whySafe": "It is a textile product with no magnets, no charging port, and no active electronic components.",
        "status": "screened"
    },
    {
        "id": "p2",
        "name": "Ceramic Tea & Infuser Set",
        "category": "Wellness",
        "price": 24.95,
        "rating": 4.7,
        "reviewed": "Non-electronic kitchenware",
        "image": "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=900&q=80",
        "description": "A calming tea ritual set for slow mornings, hydration and a relaxing daily routine.",
        "whySafe": "Made from ceramic and stainless steel with no electrical parts, magnetic closures, or wireless technology.",
        "status": "screened"
    },
    {
        "id": "p3",
        "name": "Cork Yoga & Stretch Mat",
        "category": "Movement",
        "price": 38.00,
        "rating": 4.6,
        "reviewed": "No electronics or magnets",
        "image": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=900&q=80",
        "description": "A supportive mat for gentle stretching and low-impact movement based on your care plan.",
        "whySafe": "This is a passive, non-electronic product that does not produce a magnetic field or require charging.",
        "status": "screened"
    },
    {
        "id": "p4",
        "name": "Analog Kitchen Timer",
        "category": "Home comfort",
        "price": 12.49,
        "rating": 4.5,
        "reviewed": "Battery-free mechanical timer",
        "image": "https://images.unsplash.com/photo-1556911220-bff31c812dba?auto=format&fit=crop&w=900&q=80",
        "description": "A classic mechanical timer that helps you pace meals, meds, or routines without any digital interference.",
        "whySafe": "It relies on simple mechanical movement, with no battery, screen, wireless connection, or EMI-producing parts.",
        "status": "screened"
    },
    {
        "id": "p5",
        "name": "Soft Cotton Walking Socks",
        "category": "Movement",
        "price": 16.99,
        "rating": 4.8,
        "reviewed": "Textile product; no electronics",
        "image": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=900&q=80",
        "description": "Comfort-focused socks that support everyday walking, mobility, and warm daily routines.",
        "whySafe": "A simple textile product with no embedded electronics, magnetic features, or charging components.",
        "status": "screened"
    },
    {
        "id": "p6",
        "name": "Breathing Exercise Cards",
        "category": "Mindfulness",
        "price": 14.00,
        "rating": 4.9,
        "reviewed": "Paper-based wellness aid",
        "image": "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?auto=format&fit=crop&w=900&q=80",
        "description": "A small set of guided breathing and calm-down prompts for mindful daily rituals.",
        "whySafe": "Paper-based and entirely passive, with no magnetic or electrical features that would affect implant function.",
        "status": "screened"
    },
    {
        "id": "p7",
        "name": "Large-Print Journal",
        "category": "Mindfulness",
        "price": 11.95,
        "rating": 4.7,
        "reviewed": "Paper product; no electronics",
        "image": "https://images.unsplash.com/photo-1517842645767-c639042777db?auto=format&fit=crop&w=900&q=80",
        "description": "A simple, clear journal for tracking symptoms, routines, check-ins, and day-to-day wellbeing.",
        "whySafe": "It is a paper-based tool without any electrical power source or magnetic components.",
        "status": "screened"
    },
    {
        "id": "p8",
        "name": "Woodland Reading Lamp",
        "category": "Home comfort",
        "price": 32.99,
        "rating": 4.4,
        "reviewed": "Use at recommended distance; no wireless function",
        "image": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80",
        "description": "A quiet, low-glare lamp for reading, wind-down, and comfortable evenings at home.",
        "whySafe": "It has no wireless charging or magnetic elements; if chosen, it should be used at a comfortable distance and according to the manufacturer's guidance.",
        "status": "review"
    },
    {
        "id": "p9",
        "name": "Pacemaker-Friendly Daily Living Guide",
        "category": "Services",
        "price": 39.00,
        "rating": 4.9,
        "reviewed": "Personalized daily-life guidance",
        "image": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=900&q=80",
        "description": "A brief virtual consult that reviews your routine, travel habits, and home setup for safer everyday choices.",
        "whySafe": "This is an informational service, not an implanted or electrical device, and it can be tailored to your device model and care plan.",
        "status": "screened",
        "service": True
    },
    {
        "id": "p10",
        "name": "Cardiac Travel Care Checklist",
        "category": "Travel",
        "price": 18.50,
        "rating": 4.8,
        "reviewed": "Helpful for airport, road trips, and routine travel",
        "image": "https://images.unsplash.com/photo-1527631746610-bca00a040d60?auto=format&fit=crop&w=900&q=80",
        "description": "A compact travel pack featuring a device ID checklist, emergency contacts, and travel-friendly reminders.",
        "whySafe": "It is a paper-based organizer that avoids magnets or electronics; it helps people carry essential medical information safely.",
        "status": "screened"
    }
]

CATEGORIES = ["All", "Home comfort", "Wellness", "Movement", "Mindfulness", "Travel", "Services"]
SAFETY = [
    {
        "title": "Strong magnets can matter",
        "body": "Some implants can be affected by strong magnetic fields, magnetic therapy products, or high-power electromagnetic equipment. MyPace prioritizes products without magnets or active electronics where possible."
    },
    {
        "title": "Wireless devices deserve extra checking",
        "body": "Wireless chargers, induction surfaces, and certain fitness accessories may create electromagnetic energy. A product can be simpler and calmer for daily use if it has no wireless function or charging coil."
    },
    {
        "title": "Carry your device information",
        "body": "Keep your pacemaker card, clinic contact information, and any emergency instructions close at hand when traveling, shopping, or using new devices."
    },
    {
        "title": "When in doubt, pause and consult",
        "body": "If a product causes symptoms, feels uncertain, or comes with a magnetic claim, ask your device team before using it. MyPace is a convenience guide, not medical clearance."
    },
]
WELLNESS = [
    {"kind": "do", "title": "Build calming routines", "body": "Keep a consistent sleep, meal, and movement schedule to support your rhythm and reduce day-to-day stress."},
    {"kind": "do", "title": "Choose low-interference essentials", "body": "Prefer goods that are battery-free, non-magnetic, and straightforward to use in your daily environment."},
    {"kind": "dont", "title": "Do not rely on every product label", "body": "Even if a product looks safe, device models differ and personal circumstances matter. Check the specific guidance from your cardiology team."},
    {"kind": "dont", "title": "Do not ignore new symptoms", "body": "Seek urgent medical advice for chest pain, feeling faint, severe breathlessness, or sudden unusual palpitations."},
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
    if category and category != "All":
        result = [p for p in result if p["category"] == category]
    if q:
        result = [
            p for p in result
            if q.lower() in (p["name"] + " " + p.get("description", "") + " " + p["category"]).lower()
        ]
    return result


@app.get("/api/products/{product_id}")
def product(product_id: str):
    item = next((p for p in catalog() if p["id"] == product_id), None)
    if not item:
        raise HTTPException(404, "Product not found")
    return item


@app.get("/api/categories")
def categories():
    return CATEGORIES


@app.get("/api/safety-tips")
def safety_tips():
    return SAFETY


@app.get("/api/wellness-tips")
def wellness_tips():
    return WELLNESS
