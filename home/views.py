from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
from .forms import UploadForm
from .models import Upload
from .video import *
import time
x = None
y = "hello"
# Create your views here.
def upload(request):
    global x
    form = UploadForm(data=request.POST, files=request.FILES)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if form.is_valid():
            instance = form.save()
            x = instance.video.path
            starttime = time.time()
            video_generate(x)
            endtime = time.time()
            print(endtime-starttime)
            return JsonResponse({'message':'yes'})
    return render(request,'home/upload.html',{'form':form})
print(x)
def testimonals(request):
    return render(request,'home/testimonal.html')
def result(request):
    path = str(x)
    print(output_file)
    return render(request,'home/results.html')



   # video = VideoStream(path)
    # return StreamingHttpResponse(video, content_type='video/mp4')
    # response = StreamingHttpResponse(video_generate(path), content_type='video/mp4')


   