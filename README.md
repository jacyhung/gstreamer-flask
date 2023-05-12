# gstreamer-flask wrapper for Radxa Rock 5B
Record the HDMI input from a Radxa Rock 5B, using gstreamer and wrapped with Python (flask webserver). What this project aims to do is to run gstreamer, but with an intuitive UI. I chose to use a webserver rather than an app as you could access this externally (assuming you're on the same network), from any web browser. 

There are two different versions in this repository. `app.py` is written for the gstreamer Python API, while `subprocess.py` is just running gstreamer using a subprocess. Both work the same. 

If you'd like to use the project, you may need to make some adjustments to the code. Also, this should (theoretically) work on anything Linux-based, of course with adjustments to the code. For example, this by default uses v4l2 for its video source on Linux.

Although, this should *theoretically* work out-of-the-box for Fujifilm X-T4 users. To grasp the required settings for your video input, run
```bash
v4l2-ctl -d /dev/videoX --get-fmt-video
```
<i>replace "X" with your corresponding video input, which you can list using `ls /dev/video*`</i>

Additionally, you may need to change the pixel format and video size in `format=NV16,width=3840,height=2160`, according to your camera. The Fujifilm X-T4 outputs in NV16 at 3840x2160 (Radxa Rock 5B HDMI-in does not support DCI [4096]).

You may also need to adjust the audio input source if you have multiple sources. Replace `alsasrc device=hw:4,0` with the correct hw identifier.

Change the file location if you wish to store the videos elsewhere. It's currently set as `/storage/`

Run the flask webserver and navigate to `http://localhost:5000`. You'll see a pretty barebones page, just a heading and button.

## How this works
The way this works is pretty basic. When you click the button, a POST request is sent to the backend to initiate the recording process. The script pauses for 500 milliseconds (otherwise this executes too quickly), then checks to see if the file for the video has been created. The file is checked to see if it has a size of at least 10 bytes, and then prompts the webpage. The reason we check if the filesize is at least 10 bytes is so that we can determine whether or not gstreamer is actually streaming any video. For example, if your camera is OFF, then the v4l2 source technically doesn't exist, therefore, gstreamer pauses and fails to record. However, the file still gets created, albeit has a file size of 0 bytes.

Pressing the Stop Recording button initiates another request, where the `is_recording` variable is already set to True, thus we can detect and stop the recording. Just as a last check, we compare the file size yet again to make sure it's at least 1MB, and then we tell the user that the recording was successful, and where the file was stored.

Obviously, this is not a perfect solution for those who want to bypass the 30-min recording limit (as mentioned in my blog), as this lacks portability, but is a pretty good middleground for now. I intend to get a mini OLED display and a battery, and potentially write a UI app to make this a cohesive unit. Feel free to use this project for what you will. :)

Read more about this at my blog here: <a href="https://jacyh.medium.com/bypass-fujifilm-x-t4s-30-minute-recording-limit-for-150-8a660c0efbbc">Bypass Fujifilm X-T4’s 30-minute recording limit for $150</a>
