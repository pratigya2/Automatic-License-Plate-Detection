from PIL import ImageDraw, Image
import torch
import time
import numpy as np
import cv2


class Detector(object):
    def __init__(self, det_model_path, char_model_path):
        self.det_model = torch.hub.load(
            'yolov5', 'custom', path=det_model_path, force_reload=True, source='local')
        self.char_model = torch.hub.load(
            'yolov5', 'custom', path=char_model_path, force_reload=True, source='local')
        self.class_names = {'0': '०', '1': '१', '2': '२', '3': '३', '4': '४', '5': '५', '6': '६', '7': '७',
                            '8': '८', '9': '९', 'ba': 'बा', 'pa': 'प', 'ga': 'ग', 'lu': 'लु', 'cha': 'च', 'idk': ''}

    def infer(self, model, img):
        result = model(img)
        print(result)
        characters = result.pandas().xyxy[0].sort_values("xmin")
        return characters

    def inference(self, img):
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        fontColor = (255, 255, 255)
        thickness = 1
        lineType = 2
        bounding_box_color = (255, 0, 0)
        w, h, _ = img.shape
        gap = int(0.03*h)
        start_time = time.time()
        det_result = self.det_model(img)
        print(det_result)
        det_result = det_result.pandas().xyxy[0].sort_values("xmin")
        if not det_result.empty:
            for index, row in det_result.iterrows():
                xmin, ymin, xmax, ymax = int(row['xmin']), int(
                    row['ymin']), int(row['xmax']), int(row['ymax'])
                lp = img[ymin:ymax, xmin:xmax]
                img = cv2.rectangle(img, (xmin, ymin),
                                    (xmax, ymax), bounding_box_color, 2)
                char_result = self.infer(self.char_model, lp)
                licence_text = ""
                if not char_result.empty:
                    for index, row in char_result.iterrows():
                        licence_text += self.class_names.get(row['name'])
                    cv2.putText(img, licence_text,
                                (xmin, ymin),
                                font,
                                fontScale,
                                fontColor,
                                thickness)

            end_time = time.time()
            fps = 1/(end_time-start_time)
            cv2.putText(img, (f"{fps:.2f} FPS"),
                        (int(0.9*w), int(0.1*h)),
                        font,
                        fontScale,
                        fontColor,
                        thickness)
        return img

    def infer_video(self, input_vid):
        cap = cv2.VideoCapture(input_vid)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        arr = []
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        _, image = cap.read()
        out = cv2.VideoWriter('media/output_video.avi', cv2.VideoWriter_fourcc('F', 'M', 'P', '4'),
                              int(cap.get(cv2.CAP_PROP_FPS)),
                              (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        start_time = time.time()

        for fno in range(total_frames):
            cap.set(cv2.CAP_PROP_POS_FRAMES, fno)
            _, image = cap.read()
            print(fno)
            img = self.inference(image)
            out.write(img)
            arr = []
        out.release()

        stream = ffmpeg.input('media/output_video.avi.mp4')
        stream = ffmpeg.output(stream, 'media/output(2).mp4')
        ffmpeg.run(stream)
        end_time = time.time()
        print((end_time - start_time)/60)
