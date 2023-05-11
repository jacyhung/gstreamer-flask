from flask import Flask, render_template, request

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

import time
import os

app = Flask(__name__)

is_recording = False
pipeline = None
file_path = None

def create_pipeline():
    global pipeline
    global file_path
    date_str = time.strftime('%Y%m%d_%H%M%S')
    file_path = f"/storage/video_{date_str}.mkv"
    pipeline = Gst.parse_launch('v4l2src device=/dev/video0 ! video/x-raw,format=NV16,width=3840,height=2160 ! '
                    'tee name=t t. ! mpph265enc ! h265parse ! matroskamux name=mux ! '
                    f'filesink location="{file_path}" sync=false alsasrc device=hw:4,0 ! '
                    'audio/x-raw,channels=2 ! audioconvert ! opusenc ! mux. t. ! queue leaky=1')
    pipeline.set_state(Gst.State.READY)

def start_recording():
    global is_recording
    global pipeline
    pipeline.set_state(Gst.State.PLAYING)
    is_recording = True

def stop_recording():
    global is_recording
    global pipeline
    pipeline.send_event(Gst.Event.new_eos())
    pipeline.set_state(Gst.State.NULL)
    is_recording = False

@app.route('/')
def index():
    return render_template('index.html', recording=False)

@app.route('/record', methods=['GET', 'POST'])
def record():
    global is_recording
    global file_path
    if request.method == 'POST':
        if not is_recording:
            create_pipeline()
            start_recording()
            time.sleep(0.5)
            # Check the file size to determine if recording was successful
            file_size = os.path.getsize(file_path)
            recording_successful = file_size > 10  # If file size is greater than 10 bytes, recording was successful.. maybe
            return render_template('index.html', recording=True, recording_successful=recording_successful)
        else:
            stop_recording()
            file_size = os.path.getsize(file_path)
            # Let's check to make sure that it the file was at least 1MB in size
            recording_successful2 = file_size > 1048576
            return render_template('index.html', recording=False, recording_successful2=recording_successful2, file_path=file_path)
    else:
        recording = 'True' if is_recording else 'False'
        return render_template('index.html', recording=recording)

if __name__ == '__main__':
    GObject.threads_init()
    Gst.init(None)
    app.run(debug=True, host='0.0.0.0')
