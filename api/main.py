from fastapi import FastAPI

app = FastAPI()

@app.get("/status")
def status():
    return {"Im": "Ok"}


@app.get('/receive/{text}')
def receive(text):
    print(text)
    return {"OK"}
