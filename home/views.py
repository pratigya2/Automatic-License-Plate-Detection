from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
from .forms import UploadForm
from .models import Upload
from .video import *
import time
x = None
y = "hello"
count = 1
# Create your views here.
def upload(request):
    global x
    global new
    global count
    form = UploadForm(data=request.POST, files=request.FILES)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if form.is_valid():
            instance = form.save()
            x = instance.video.path
            starttime = time.time()
            output_file = 'media/' +str(count)+ '.mp4'
            new = 'media/' + str(count)+'(2)'+'.mp4'
            video_generate(x,output_file,new)
            count += 1
            print(count)
            endtime = time.time()
            print(endtime-starttime)
            return JsonResponse({'message':'yes'})
    return render(request,'home/upload.html',{'form':form})
print(x)
def testimonals(request):
    return render(request,'home/testimonal.html')
def result(request):
    path = str(x)
    print(new)
    return render(request,'home/results.html',{'new':new})



   # video = VideoStream(path)
    # return StreamingHttpResponse(video, content_type='video/mp4')
    # response = StreamingHttpResponse(video_generate(path), content_type='video/mp4')


   