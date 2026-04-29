from fastapi import FastAPI

app = FastAPI()

print(app)

@app.get("/")
def read_root():
    return {"message": "Welcome to your Productivity API!"}

@app.get("/status")
def check_status():
    return {"status" : "Online", "version": "1.0.0"}