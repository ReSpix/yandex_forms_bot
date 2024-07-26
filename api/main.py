from fastapi import FastAPI

app = FastAPI()

@app.get("/status")
def status():
    return {"Im, ok"}


@app.get('/receive/{text}')
def receive(text):
    print(text)
    return {"Received succesfully"}
