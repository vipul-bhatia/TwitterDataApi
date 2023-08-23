from typing import List
from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from bson.objectid import ObjectId
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demonstration purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient('mongodb+srv://priyam:pqrs.123@cluster0.1uefwpt.mongodb.net/')
db = client['disaster_management']

class DisasterTweet(BaseModel):
    _id: str
    text: str
    predicted_category: str

class ContactData(BaseModel):
    name: str
    email: str
    subject: str
    message: str


@app.get("/fetch_energy/", response_model=List[DisasterTweet])
async def fetch_energy_data():
    return fetch_all_data_from_collection("energy")

@app.get("/fetch_food/", response_model=List[DisasterTweet])
async def fetch_food_data():
    return fetch_all_data_from_collection("food")

@app.get("/fetch_medical/", response_model=List[DisasterTweet])
async def fetch_medical_data():
    return fetch_all_data_from_collection("medical")

@app.get("/fetch_water/", response_model=List[DisasterTweet])
async def fetch_water_data():
    return fetch_all_data_from_collection("water")

@app.post("/save_contact_data/")
async def save_contact_data(data: ContactData):
    collection = db["contact_us"]
    result = collection.insert_one(data.dict())
    return {"_id": str(result.inserted_id)}


def fetch_all_data_from_collection(collection_name: str):
    collection = db[collection_name]

    # Fetch all documents
    documents = collection.find()

    results = []
    for document in documents:
        
        tweet = {
            "_id": str(document["_id"]),
            "text": document["text"],
            "predicted_category": document["predicted_category"]
        }
        results.append(tweet)

    return results


