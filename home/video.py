import os
import django
from django.http import HttpResponse
import threading
from queue import Queue
import subprocess
import ffmpeg

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ALPD.settings')
django.setup()
import cv2
import time
import numpy as np
frames = []
output_file = 'media/output.mp4'

def video_read(x):
    global width
    global height
    global fps

    vid = cv2.VideoCapture(x)
    width  = int(vid.get(3))  # float `width`
    height = int(vid.get(4))
    fps =  int(vid.get(cv2.CAP_PROP_FPS))
    currentframe = 0
    startime = time.time()
    while(True):
        success,frame= vid.read()
        if success:
            frames.append(frame)
            print("Type : ", frame.shape)
        else:
            break
    vid.release()


def video_generate(x):

    video_read(x)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (int(width), int(height)))
    for frame in frames:
        out.write(frame)

    # Release the VideoWriter object and close the output file
    out.release()
    startime = time.time()
    stream = ffmpeg.input('media/output.mp4')
    print("hello")
#      stream = ffmpeg.hflip(stream)
    stream = ffmpeg.output(stream, 'media/output(2).mp4')
    ffmpeg.run(stream)
    endtime = time.time()
    print(startime-endtime)
    # ffmpeg.('ffmpeg -i media/output.mp4 -vcodec libx264 -f mp4 media/output(2).mp4')
    # with open(output_file, 'rb') as video_file:
    #     response = HttpResponse(video_file.read(), content_type='video/mp4')
    #     response['Content-Disposition'] = 'inline; filename=output.mp4'
    #     return response

        # _, jpeg = cv2.imencode('.jpg', frame)
        # yield (b'--frame\r\n 'b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    