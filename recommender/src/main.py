from fastapi import FastAPI
from .api.recommender import router
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get('/')
def home():
    return {
        "project_url":"https://github.com/Suraj1089/shareNotes",
        "Bard_Reversed_engineering":"https://github.com/acheong08/Bard",
        "Sponser_bard_reversed_engineering_at": {
            "Creator":"https://github.com/acheong08"
        }
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('src.main:app',host='0.0.0.0',port=8001,reload=True)