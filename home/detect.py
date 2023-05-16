from PIL import ImageDraw, Image
import torch
import time
import numpy as np
import cv2
from PIL import ImageFont
import PIL.ImageDraw as draw
import ffmpeg
import pandas
import os
import subprocess
import shutil

class Detector(object):
    def __init__(self, det_model_path, char_model_path):
        self.det_model = torch.hub.load(
            'yolov5', 'custom', path=det_model_path, force_reload=True, source='local')
        self.char_model = torch.hub.load(
            'yolov5', 'custom', path=char_model_path, force_reload=True, source='local')

    def infer(self, model, img):
        result = model(img)
        print(result)
        characters = result.pandas().xyxy[0].sort_values("xmin")
        return characters

    def frame_rate(self,inp_vid):
        start = time.time()
        if os.path.exists('media\images'):
            shutil.rmtree('media\images')
        os.mkdir('media\images')
        output_pattern = 'media\images\output_frame_%04d.png'
        command = ['ffprobe', '-v', '0', '-of', 'csv=p=0', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate', inp_vid]
        output = subprocess.check_output(command)
        frame_rate = eval(output.decode('utf-8'))
        command = ['ffmpeg', '-i', inp_vid, '-vf', f'fps={frame_rate}', output_pattern]
        subprocess.call(command)
        end = time.time()
        print(end-start)
        return frame_rate

    def inference(self, img):
        class_names = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
                            8: '8', 9: '9', 10: 'ba', 11: 'pa', 12: 'ga', 13: 'lu', 14: 'cha', 15:'0',
                            16:'1',17:'2',18:'3',19:'4',20:'5',21:'6',22:'7',23:'8',24:'9',25:'A',
                            26:'B'}  
        start_time = time.time()
        w,h,_ = img.shape
        det_result = self.det_model(img)
        det_result = det_result.pandas().xyxy[0].sort_values("xmin")
        if not det_result.empty:
            for index, row in det_result.iterrows():
                xmin, ymin, xmax, ymax = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
                lp = img[ymin:ymax,xmin:xmax]
                cv2.rectangle(img,(xmin,ymin),(xmax,ymax),(34,139,34),thickness = 3)
                char_result = self.infer(self.char_model, lp)
                licence_text = ''
                if not char_result.empty:
                    for index, row in char_result.iterrows():
                        licence_text+=class_names.get(int(row['class']))
                    print(licence_text)
                    cv2.putText(img,licence_text,(xmin,ymin),cv2.FONT_ITALIC,1,(255,99,71),3)  
        end_time = time.time()
        fps = 1/(end_time-start_time)
        cv2.putText(img,(f"{fps:.2f} FPS"),(int(0.9*w),int(0.05*h)),cv2.FONT_ITALIC,1,(255,99,71),5)            
        return img

    def infer_video(self, input_vid):
        path_split = input_vid.split("\\")
        filename = 'inp_' + path_split[-1]
        print(filename)
        write_video = 'media/'+ filename
        read_video = write_video.replace('inp','out')
        cap = cv2.VideoCapture(input_vid)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        arr = []
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        _, image = cap.read()
        out = cv2.VideoWriter(write_video, cv2.VideoWriter_fourcc(*'mp4v'),
                              int(cap.get(cv2.CAP_PROP_FPS)),
                              (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        start_time = time.time()

        for fno in range(total_frames):
            cap.set(cv2.CAP_PROP_POS_FRAMES, fno)
            _, image = cap.read()
            print(fno)
            img = self.inference(image)
            out.write(img)
        out.release()
        stream = ffmpeg.input(write_video)
        stream = ffmpeg.output(stream, read_video)
        ffmpeg.run(stream)
        end_time = time.time()
        print(end_time - start_time)
        return read_video
    
    def infer_image(self,img):
        image = cv2.imread(img)
        predicted_image = self.inference(image)
        path_split = img.split("\\")[-1]
        final_path = 'media/'+'inp_'+str(path_split)
        cv2.imwrite(final_path, predicted_image)
        return final_path

       
    def read(self,input_vid):
        frame_rate= self.frame_rate(input_vid)
        path_split = input_vid.split("\\")
        filename = 'inp_' + path_split[-1]
        print(filename)
        write_video = 'media/'+ filename
        folder_path = 'media/images'
        start_time = time.time()
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                img = self.inference(file_path)
                input_image_dir, input_image_filename = os.path.split(file_path)
                output_image_path = os.path.join(input_image_dir, input_image_filename)
                img.save(output_image_path)
        command = ['ffmpeg', '-framerate', str(frame_rate), '-i', 'media\images\output_frame_%04d.png', '-c:v', 'libx264', '-profile:v', 'high', '-crf', '20', '-pix_fmt', 'yuv420p', write_video]
        subprocess.call(command)
        end_time = time.time()
        shutil.rmtree('media\images')
        print(end_time - start_time)
        return write_video
       
