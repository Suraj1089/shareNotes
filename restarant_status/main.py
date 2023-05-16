from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get('/')
def home():
    return {"data":"home page"}

@app.get('/trigger_report')
def report_trigger():
    return {"report":"triggered"}

@app.get('/get_report')
def get_report():
    return {"data":"get report"}










if __name__ == '__main__':
    uvicorn.run('main:app',host='0.0.0.0',port=8000,reload=True)