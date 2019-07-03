from flask import Flask, render_template, Response, request, send_file
from multiprocessing import Process, Queue
import cv2 
import numpy as np
import time


app = Flask(__name__)
frame_queue = Queue(7)
#logging.basicConfig(filename='aaa.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
#logging.warning('======= SYSTEM WARMINGUP =========')


@app.route('/')
def index():
    """Video streaming home page."""
    print ('render')
    return render_template('index.html')


@app.route('/grabber')
def video_grabber(endpoint):
    """[summary]
    
    Arguments:
        endpoint {integer or sring} -- 0 for webcam or CCTV RTSP
    """
    # video capturer object
    data = json.loads(request.data)
    image = np.array(data['image']).astype(np.uint8)
    if frame_queue.qsize() < 7:
        frame_queue.put(image)


def gen():
    """Video streaming generator function."""
    filler = np.zeros((25, 60, 3)).astype(np.uint8)
    filler = cv2.resize(filler, (60, 25))

    while True:
        #ret, frame = cap.read()
        ret = None
        frame = None
        jpeg = None

        if frame_queue.qsize() > 0:
            print ("====>>>>>>>>>>>>>>", "get from  queue")
            frame = frame_queue.get()
            frame = cv2.resize(frame, (60, 25))
            ret_encode, jpeg = cv2.imencode('.jpg', )
        else:
            print ('--->>>>>>>>>>>>>>>', "get from filler")
            frame = filler
            ret_encode, jpeg = cv2.imencode('.jpg', frame)
            
        jpeg = jpeg.tobytes()
        time.sleep(10)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    print ('------------------------- ||')
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')





 
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500, debug=True, threaded=True, use_reloader=False)
