from mycelery.main import app

@app.task(name="send_mail")
def send_mail():
    return "hello. mail!!!!"