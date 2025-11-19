import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents

app = FastAPI(title="Hyderabad Realty Consultancy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LeadRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    message: Optional[str] = None
    interested_location: Optional[str] = None
    budget_in_inr: Optional[int] = None
    property_type: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Hyderabad Realty Consultancy API is running"}

@app.get("/api/properties")
def list_properties(location: Optional[str] = None, min_price: Optional[int] = None, max_price: Optional[int] = None, property_type: Optional[str] = None, limit: int = 20):
    """Public endpoint to browse properties"""
    filters = {}
    if location:
        filters["location"] = {"$regex": location, "$options": "i"}
    if property_type:
        filters["property_type"] = {"$regex": f"^{property_type}$", "$options": "i"}
    price_filter = {}
    if min_price is not None:
        price_filter["$gte"] = min_price
    if max_price is not None:
        price_filter["$lte"] = max_price
    if price_filter:
        filters["price_in_inr"] = price_filter

    try:
        docs = get_documents("property", filters, limit)
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/inquiry")
def create_inquiry(lead: LeadRequest):
    """Collect lead info from website contact form"""
    try:
        data = lead.dict()
        doc_id = create_document("inquiry", data)
        return {"id": str(doc_id), "status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
