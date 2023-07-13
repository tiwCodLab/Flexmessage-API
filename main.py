from routes.flexaver_routes import user
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get("/")
def main_page():
    return "Welcome to Flexaver."
 
app.include_router(user)
