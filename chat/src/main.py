# main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse


app = FastAPI(
    title="Chat API",
    description="API for chat application",
    openapi_url="/chat/api/v1/auth/openapi.json",
    docs_url="/chat/api/v1/docs/",
    redoc_url="/chat/api/v1/redoc/"
)


# setup middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/',include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url='/chat/api/v1/docs')

@app.get("/chat/api/v1/auth", response_class=HTMLResponse)
async def read_root():
    return """
        <html>
            <head>
                <title>Chat API</title>
            </head>
            <body>
                <h1>Chat API</h1>
                <div>
                    <h2>Documentation</h2>
                    <p>Check out the <a href="/chat/api/v1/docs">documentation</a>.</p>
                </div>
            </body>
        </html>
    """


if __name__ == "__main__":
    
    uvicorn.run("main:app", host="localhost", port=8000)
