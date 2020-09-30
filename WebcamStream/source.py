from flask import Flask, render_template, Response
from WebcamStream.webcam import Camera
from WebcamStream.resource import gen

# Flask setup
app = Flask(__name__)


@app.route('/')
def index(): return render_template('index.html')


@app.route('/video_feed')
def video_feed(): return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


# Run Flask Server, if invoked on this module; on debug mode
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
