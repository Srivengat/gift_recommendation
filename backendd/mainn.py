
from Agent import rank_gifts_with_llm
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer, Text, Enum, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
import uuid
import re
from fastapi.staticfiles import StaticFiles


# ==========================
# DATABASE CONFIG
# ==========================

DATABASE_URL = "mysql+pymysql://root:SVB%402005@localhost/gifting_app"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI(title="Gifting Agent")

app.mount("/static", StaticFiles(directory="static"), name="static")

# ==========================
# CORS CONFIG
# ==========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# DATABASE MODELS
# ==========================

class Gift(Base):
    __tablename__ = "gifts"

    id = Column(String(36), primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    price = Column(Integer)
    image_url = Column(Text)
    relation = Column(String(100))
    occasion = Column(String(100))
    category = Column(Enum("personalized", "general"))
    active = Column(Boolean, default=True)


class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True)
    person = Column(String(100))
    occasion = Column(String(100))
    category = Column(Enum("personalized", "general"))
    budget = Column(Integer)


class Order(Base):
    __tablename__ = "orders"

    id = Column(String(36), primary_key=True)
    session_id = Column(String(36))
    gift_id = Column(String(36))
    is_personalized = Column(Boolean)
    address = Column(Text)
    payment_status = Column(String(50))


Base.metadata.create_all(bind=engine)

# ==========================
# DEPENDENCY
# ==========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================
# REQUEST MODELS
# ==========================

class StartChatResponse(BaseModel):
    session_id: str
    reply: str


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    done: bool
    recommendations: list | None = None
    buy: bool = False


class CreateOrderRequest(BaseModel):
    session_id: str
    gift_id: str


# ==========================
# NLP Extraction
# ==========================

PERSONS = ["mother", "father", "sister", "brother", "friend", "wife", "husband","girlfriend","boyfriend","gf","bf","mom","dad"]
OCCASIONS = ["birthday", "anniversary", "wedding", "festival"]
GIFT_TYPE = ["personalized", "personalised", "general", "ready-made"]

def extract_data(message: str):
    msg = message.lower()
    data = {"person": None, "occasion": None, "category": None, "budget": None}

    for p in PERSONS:
        if p in msg:
            data["person"] = p
            break

    for o in OCCASIONS:
        if o in msg:
            data["occasion"] = o
            break

    for g in GIFT_TYPE:
        if g in msg:
            if g in ["personalized", "personalised"]:
                data["category"] = "personalized"
            else:
                data["category"] = "general"
            break

    budget_match = re.search(r"\b\d{3,6}\b", msg)
    if budget_match:
        data["budget"] = int(budget_match.group())

    return data


# ==========================
# CHAT APIs
# ==========================

@app.post("/start-chat", response_model=StartChatResponse)
def start_chat(db: Session = Depends(get_db)):
    session_id = str(uuid.uuid4())
    session = SessionModel(id=session_id)
    db.add(session)
    db.commit()

    return {
        "session_id": session_id,
        "reply": "Hi 👋 Who are you planning to gift?"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):

    session = db.query(SessionModel).filter(SessionModel.id == request.session_id).first()
    if not session:
        return {"session_id": request.session_id, "reply": "Invalid session", "done": False}

    extracted = extract_data(request.message)

    if extracted["person"]:
        session.person = extracted["person"]
    if extracted["occasion"]:
        session.occasion = extracted["occasion"]
    if extracted["category"]:
        session.category = extracted["category"]
    if extracted["budget"]:
        session.budget = extracted["budget"]

    print(f"DEBUG: Message: {request.message}")
    print(f"DEBUG: Extracted: {extracted}")
    print(f"DEBUG: Session State: person={session.person}, occasion={session.occasion}, category={session.category}, budget={session.budget}")

    db.commit()

    if not session.person:
        return {"session_id": session.id, "reply": "Who are you planning to gift?", "done": False}
    if not session.occasion:
        return {"session_id": session.id, "reply": "What is the occasion?", "done": False}
    if not session.category:
        return {"session_id": session.id, "reply": "Do you want personalized or general gift?", "done": False}
    if not session.budget:
        return {"session_id": session.id, "reply": "What is your budget?", "done": False}

    # ===============================
    # AI Filtering
    # ===============================

    # Get a decent pool of active gifts
    gifts = db.query(Gift).filter(Gift.active == True).limit(50).all()

    gift_data_for_ai = [
        {
            "gift_id": g.id,
            "name": g.name,
            "description": g.description,
            "price": g.price,
            "relation": g.relation,
            "occasion": g.occasion,
            "category": g.category
        }
        for g in gifts
    ]

    user_preferences = {
        "person": session.person,
        "occasion": session.occasion,
        "category": session.category,
        "budget": session.budget
    }

    try:
        ranked_ids = rank_gifts_with_llm(user_preferences, gift_data_for_ai)
        # Match IDs and maintain AI's ranking order
        top3 = []
        for rid in ranked_ids:
            match = next((g for g in gifts if g.id == rid), None)
            if match:
                top3.append(match)
        
        # If AI failed to provide enough valid IDs, fill with relevant active gifts
        if len(top3) < 3:
            remaining = [g for g in gifts if g not in top3]
            top3.extend(remaining[:3-len(top3)])
            
    except Exception as e:
        print(f"DEBUG: AI Processing error: {e}")
        top3 = gifts[:3]

    recommendations = [
        {
            "gift_id": g.id,
            "name": g.name,
            "price": g.price,
            "image_url": g.image_url,
            "category": g.category
        }
        for g in top3
    ]

    return {
        "session_id": session.id,
        "reply": "Perfect 🎁 Here are the best gift suggestions for you!",
        "done": True,
        "buy": True,
        "recommendations": recommendations
    }


@app.post("/order/create")
def create_order(request: CreateOrderRequest, db: Session = Depends(get_db)):

    gift = db.query(Gift).filter(Gift.id == request.gift_id).first()
    if not gift:
        return {"error": "Invalid gift"}

    order_id = str(uuid.uuid4())

    order = Order(
        id=order_id,
        session_id=request.session_id,
        gift_id=request.gift_id,
        is_personalized=(gift.category == "personalized"),
        payment_status="PENDING"
    )
    db.add(order)
    db.commit()

    return {
        "order_id": order_id,
        "is_personalized": gift.category == "personalized"
    }