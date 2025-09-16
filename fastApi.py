from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🔥 Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows all origins (good for development)
    allow_credentials=True,
    allow_methods=["*"],  # allows all HTTP methods: GET, POST, etc.
    allow_headers=["*"],  # allows all headers
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/search")
def search(height:float,weight:float):
    bmi=round(weight/(height*height),2)
    if(bmi<18.5):
        correctweight=round(18.5*(height*height),2)
        needToGain=round(correctweight-weight,2)
        return {"bmi":bmi,"status":"underweight","correct_bmi":correctweight,"needToGain":needToGain}
    elif(bmi>=18.5 and bmi<24.9):
        return {"bmi":bmi,"status":"normal"}    
   
    else:
        correctweight=round(24.9*(height*height),2)
        needToLose=round(weight-correctweight,2)
        return {"bmi":bmi,"status":"overweight","correct_bmi":correctweight,"needToLose":needToLose}