from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
from .forms import UploadForm
from .models import Upload
from .video import *
from .detect import *
import time
x = None
y = "hello"
count = 1
# Create your views here.
DetectionModel = Detector('home\static\lp.pt','home\static\character.pt')
# TRTModel = Detector('home\static\lp.engine','home\static\best.engine')


def upload(request):
    global x
    global new
    form = UploadForm(data=request.POST, files=request.FILES)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if form.is_valid():
            instance = form.save()
            x = instance.video.path
            starttime = time.time()
            if x.endswith('.mp4'):
                new = DetectionModel.infer_video(x)
            else:
                new = DetectionModel.infer_image(x)
            endtime = time.time()
            print(endtime-starttime)
            return JsonResponse({'message':'yes'})
    return render(request,'home/upload.html',{'form':form})
print(x)
def testimonals(request):
    return render(request,'home/testimonal.html')
def result(request):
    if new.endswith('.mp4'):
        return render(request,'home/results.html',{'new':new})
    else:
        return render(request,'home/image.html',{'new':new})



   # video = VideoStream(path)
    # return StreamingHttpResponse(video, content_type='video/mp4')
    # response = StreamingHttpResponse(video_generate(path), content_type='video/mp4')


   