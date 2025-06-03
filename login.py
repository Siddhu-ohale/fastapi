# from fastapi import FastAPI, HTTPException, Depends, Request, Form
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel, Field
# from sqlalchemy import create_engine, Column, String, Integer
# from sqlalchemy.orm import sessionmaker, declarative_base, Session
# from dotenv import load_dotenv
# import os

# # ------------------- FastAPI App -------------------
# app = FastAPI()

# # ------------------- Templates & Static -------------------
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# # ------------------- Load .env Variables -------------------
# load_dotenv()

# username = os.getenv("sql_username")
# password = os.getenv("password")
# host     = os.getenv("host")
# port     = os.getenv("port")
# db_name  = os.getenv("db_name")

# if not all([username, password, host, port, db_name]):
#     raise Exception("Environment variables not loaded properly. Check .env file.")

# # ------------------- Database Setup -------------------
# DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # ------------------- Dependency -------------------
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # ------------------- SQLAlchemy Model -------------------
# class User(Base):
#     __tablename__ = 'users'
#     id       = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), unique=True, nullable=False)
#     password = Column(String(100), nullable=False)

# # Create users table
# Base.metadata.create_all(bind=engine)

# # ------------------- Routes -------------------

# @app.get("/", response_class=HTMLResponse)
# def home(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})

# @app.get("/register", response_class=HTMLResponse)
# def register_get(request: Request):
#     return templates.TemplateResponse("register.html", {"request": request})

# @app.post("/register")
# def register_user(
#     request: Request,
#     username: str = Form(...),
#     password: str = Form(...),
#     db: Session = Depends(get_db)
# ):
#     existing_user = db.query(User).filter(User.username == username).first()
#     if existing_user:
#         return templates.TemplateResponse("register.html", {
#             "request": request,
#             "msg": "Username already exists"
#         })

#     # Save password as plain text (⚠️ Not secure)
#     new_user = User(username=username, password=password)
#     db.add(new_user)
#     db.commit()
#     return templates.TemplateResponse("login.html", {
#         "request": request,
#         "msg": "Registration successful. Please login."
#     })

# @app.get("/portfolio", response_class=HTMLResponse)
# def portfolio(request: Request):
#     return templates.TemplateResponse("Portfolio.html", {"request": request})

# @app.post("/login")
# def login_user(
#     request: Request,
#     username: str = Form(...),
#     password: str = Form(...),
#     db: Session = Depends(get_db)
# ):
#     user = db.query(User).filter(User.username == username).first()
#     if not user or user.password != password:
#         return templates.TemplateResponse("login.html", {
#             "request": request,
#             "msg": "Invalid credentials"
#         })

#     return RedirectResponse(url="/portfolio", status_code=303)


from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
import os
import logging

# ------------------- Logging Setup -------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs.log"),  # Log file
        logging.StreamHandler()           # Terminal console
    ]
)
logger = logging.getLogger(__name__)

# ------------------- FastAPI App -------------------
app = FastAPI()

# ------------------- Templates & Static -------------------
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ------------------- Load .env Variables -------------------
load_dotenv()

username = os.getenv("sql_username")
password = os.getenv("password")
host     = os.getenv("host")
port     = os.getenv("port")
db_name  = os.getenv("db_name")

if not all([username, password, host, port, db_name]):
    logger.error("Environment variables not loaded properly.")
    raise Exception("Environment variables not loaded properly. Check .env file.")

# ------------------- Database Setup -------------------
DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ------------------- Dependency -------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------- SQLAlchemy Model -------------------
class User(Base):
    __tablename__ = 'users'
    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

# Create users table
Base.metadata.create_all(bind=engine)

# ------------------- Routes -------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    logger.info("Home page visited.")
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def register_get(request: Request):
    logger.info("Register page visited.")
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        logger.warning(f"Attempt to register with existing username: {username}")
        return templates.TemplateResponse("register.html", {
            "request": request,
            "msg": "Username already exists"
        })

    # Save password as plain text (⚠️ Not secure)
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    logger.info(f"User registered successfully: {username}")
    return templates.TemplateResponse("login.html", {
        "request": request,
        "msg": "Registration successful. Please login."
    })

@app.get("/portfolio", response_class=HTMLResponse)
def portfolio(request: Request):
    logger.info("Portfolio page accessed.")
    return templates.TemplateResponse("Portfolio.html", {"request": request})

@app.post("/login")
def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        logger.warning(f"Login failed: user '{username}' not found.")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "msg": "User not found"
        })

    if user.password != password:
        logger.warning(f"Login failed: wrong password for user '{username}'.")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "msg": "Invalid password"
        })

    logger.info(f"User logged in successfully: {username}")
    return RedirectResponse(url="/portfolio", status_code=303)
