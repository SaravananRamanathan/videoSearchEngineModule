"""
app:ccextractorProcess, its views are here.
"""
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from .forms import UploadFileForm
from .models import video
from .tasks import go_to_sleep,videoProcessing
import wave, math, contextlib
import speech_recognition as sr
from celery.result import AsyncResult
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import boto3
import botocore
from django.contrib import messages
def uploadButton(request):
    if request.method=="POST":
        "post method"
        print("received from ajax uploadButton clicked: {}".format(request.POST))
        data={
            "msg":"post method for deleting todolist item received.",
        }
        return JsonResponse(data);
    else:#get
        data={
          "msg":"message received ok",
        }
        return JsonResponse(data)

@csrf_exempt
def homePage(request):
    #request.upload_handlers.insert(0, ProgressBarUploadHandler(request))
    
    # this removes the first handler (MemoryFile....)
    request.upload_handlers.pop(0)#seems to work fine, this makes getting path for files less then 2mb possible..... 
    #request.upload_handlers.insert(0, ProgressBarUploadHandler.delay(request))

    return _homePage(request)

# todo : later need to add a logic if a media path in bucket is empty to begin with.
def key_exists(mykey, mybucket):
    s3_client = boto3.client('s3', 
        aws_access_key_id='<you-access-key-id>', 
        aws_secret_access_key='<your-secret-access-key>')
    response = s3_client.list_objects_v2(Bucket=mybucket, Prefix=mykey)
    if response:
      if 'Contents' in response:
        for obj in response['Contents']:
            if mykey == obj['Key']:
                return True
    return False

@csrf_protect
def _homePage(response):
    "home page"
    task_id=None
    if response.method=="POST":

        file = response.FILES['file']
        print(f"file_name test: {file.name}")
        #a=True  #-- used this to bypass the probelm that would arise if bucket path is empty to begin with.... need to add this to TODO
        if not key_exists('media/'+file.name, '<your-bucket-name>'):
            print("new file case")
            print(response.POST)
            form = UploadFileForm(response.POST, response.FILES)
            if form.is_valid():
                
                print("valid form... starting videoProcessing Task.")
                
                print(f"testing file: {file}")
            
                #video processing task.
                task_videoProcessing = videoProcessing.delay(file.temporary_file_path(),file.name)
                task_id=task_videoProcessing
                print(task_videoProcessing)


                #testing-stuff
                """while(True):
                    # grab the AsyncResult 
                    status = AsyncResult(task_id)
                    # print the task id
                    print(status.task_id)
                    # print the AsyncResult's status
                    print(status.status)
                    # print the result returned 
                    print(status.result)"""

                #upload video part.
                temp=video()
                temp.upload=file
                temp.save()
                print("upload completed")


                """while( (AsyncResult(task_id).result==None) or AsyncResult(task_id).status != 'FAILURE'):
                    "do nothing."
                    print(f"stuck in while loop :( {AsyncResult(task_id).result}")"""
                while(True):
                    status = AsyncResult(task_id)
                    if status.result==None:
                        "Do nothing."
                    else:
                        break
                #results
                #done_videoProcessing = task_videoProcessing.get()
                #print(done_videoProcessing)

                
                #result = videoProcessing.delay(response.FILES['file'] .temporary_file_path())
                #result=go_to_sleep.delay(1) 
                #return render(response, 'ccextractorProcess/home.html', context={'form':form,'task_id':result.task_id})
                #return HttpResponseRedirect(response.path_info)
            else:
                print("Not valid form")
                #return HttpResponseRedirect(response.path_info)
            #return HttpResponseRedirect('/success/url/')
            
        else:
            print("file exists case")
            form = UploadFileForm(response.POST, response.FILES)
            if form.is_valid():
                print("file exists case and form valid --sending error alert")
                messages.error(response, "file exist's, please choose a differnet file")
    else:
        form = UploadFileForm()
    
    #form = UploadFileForm()
    #result = go_to_sleep.delay(1)
    
    return render(response, 'ccextractorProcess/home.html', context={'form':form,'task_id':task_id})#,'task_id': result.task_id})   
