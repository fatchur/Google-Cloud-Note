from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello this is my ordinary custom app egnie ---------"

if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 8080
    app.run(threaded=True, port=8080) 
