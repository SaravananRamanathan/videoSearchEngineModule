from ast import parse
from django.http import JsonResponse
from django.shortcuts import render
import boto3
from boto3.dynamodb.conditions import Attr
# Create your views here.

def videoSearchAnswer(request):
    ""
    if request.method=="POST":
        "post method"
        print("received on video-search-answer: {}".format(request.POST))
        #{'data': ['https://srvnn-django-bezen.s3.ap-south-1.amazonaws.com/media/cod1.mp4']} #sample received
        url=request.POST.get("data")
        wordToFind=request.POST.get("str")

        fileName = url[url.rfind('/')+1:]
        print(f"checking file name: {fileName}")

        #DynamoDb setup
        dynamodb = boto3.resource('dynamodb',
            region_name='ap-south-1', 
            aws_access_key_id='<your-access-key-id>', 
            aws_secret_access_key='<your-access-key-secret>')
        table = dynamodb.Table("wordsList")

        response = table.scan(
            FilterExpression=Attr('fileName').eq(fileName) & Attr('word').eq(wordToFind)
        )
        data = response.get('Items') 
        dataToSend = {"data":data,"count":response.get('Count')}
       
        return JsonResponse(dataToSend);
    else:
        data={
          "msg":"get method test ok",
        }
        return JsonResponse(data)

def infoPage(response):
    "info is where we goona display the library."
    
    s3 = boto3.resource('s3', 
        aws_access_key_id='<your-access-key-id>', 
        aws_secret_access_key='<your-access-key-secret>')
    #response = s3_client.list_objects_v2(Bucket="srvnn-django-bezen", Prefix="media/")

    #s3 = boto3.resource('s3')
    my_bucket = s3.Bucket('srvnn-django-bezen')
    urlPrefix="<your url prefix>"
    
    mediaFiles=my_bucket.objects.filter(Prefix="media/")
    print(f"testing mediafiles list: {mediaFiles}")
    parsedMediaFiles=[]
    for i in mediaFiles:
        temp=i.key
        temp = temp[temp.find('/')+1:]
        parsedMediaFiles.append(temp)
        """print(urlPrefix+i.key)
        print(i.key)
        print(i)"""
    
    #temp = "media/speech_test1.mp4"
    #print(temp[temp.find('/')+1:]) #method to get the name which can be used to search dynamodb




    return render(response, 'info/info.html', {"data":parsedMediaFiles})

    