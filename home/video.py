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
import numpy as np
frames = []
output_file = 'media/output.mp4'
# class VideoStream:
#     def __init__(self, video_file):
#         self.cap = cv2.VideoCapture(video_file)
#         self.width  = int(self.cap.get(3))  # float `width`
#         self.height = int(self.cap.get(4))
#         self.fps =  int(self.cap.get(cv2.CAP_PROP_FPS))
#         self.frame_queue = Queue()
#         self.thread = threading.Thread(target=self._read_frames)
#         self.thread.daemon = True
#         self.thread.start()

#     def _read_frames(self):
#         while True:
#             ret, frame = self.cap.read()
#             if not ret:
#                 break
#             # process the frame here if needed
#             # scale down the frame to reduce the frame size
#             # convert the frame to JPEG
#             fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#             out = cv2.VideoWriter(output_file, fourcc, self.fps, (int(self.width), int(self.height)))
#             _, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 40])
#             self.frame_queue.put(jpeg.tobytes())
#             # read a frame from the queue and return it
#             frame = self.frame_queue.get()
#             out.write(frame)
#             out.release(0)
#     def __iter__(self):
#         return self
#     def __next__(self):
#         return(output_file)

    # def __next__(self):
    #     # read a frame from the queue and return it
    #     frame = self.frame_queue.get()
    #     return (b'--frame\r\n'
    #             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
def video_read(x):
    global width
    global height
    global fps
    print("y")
    print(x)
    vid = cv2.VideoCapture(x)
    width  = int(vid.get(3))  # float `width`
    height = int(vid.get(4))
    fps =  int(vid.get(cv2.CAP_PROP_FPS))
    currentframe = 0
    while(True):
        success,frame= vid.read()
        if success:
            frames.append(frame)
        else:
            break
    vid.release()

def video_generate(x):
    print("x")
    video_read(x)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (int(width), int(height)))
    for frame in frames:
        out.write(frame)

    # Release the VideoWriter object and close the output file
    out.release()
    stream = ffmpeg.input('media/output.mp4')
    print("hello")
#      stream = ffmpeg.hflip(stream)
    stream = ffmpeg.output(stream, 'media/output(2).mp4')
    ffmpeg.run(stream)
    # ffmpeg.('ffmpeg -i media/output.mp4 -vcodec libx264 -f mp4 media/output(2).mp4')
    # with open(output_file, 'rb') as video_file:
    #     response = HttpResponse(video_file.read(), content_type='video/mp4')
    #     response['Content-Disposition'] = 'inline; filename=output.mp4'
    #     return response

        # _, jpeg = cv2.imencode('.jpg', frame)
        # yield (b'--frame\r\n 'b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    