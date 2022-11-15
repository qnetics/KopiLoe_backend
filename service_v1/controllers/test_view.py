from django.shortcuts import render
from django.http import JsonResponse
from ..models import Todo
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt 
import json



@csrf_exempt ## To exempt from default requirement for CSRF tokens to use postman
def TheModelView(request):

    if request.method == "GET" :
        #Serialize the data into json
        data = serializers.serialize("json", Todo.objects.all())
        print(serializers.serialize('json', Todo.objects.all())[0])
        # Turn the JSON data into a dict and send as JSON response
        return JsonResponse(json.loads(data), safe=False)

    if request.method == "POST" :
        # Turn the body into a dict
        body = json.loads(request.body.decode("utf-8"))
        #create the new item
        newrecord = Todo.objects.create(item=body['item'])
        # Turn the object to json to dict, put in array to avoid non-iterable error
        data = json.loads(serializers.serialize('json', [newrecord]))
        # send json response with new object
        return JsonResponse(data, safe=False)

@csrf_exempt ## To exempt from default requirement for CSRF tokens to use postman
def TheModelViewTwo(request, id):
        print(id)
        if (request.method == "PUT"):
        # Turn the body into a dict
            body = json.loads(request.body.decode("utf-8"))
        # update the item
            Todo.objects.filter(pk=id).update(item=body['item'])
            newrecord = Todo.objects.filter(pk=id)
        # Turn the object to json to dict, put in array to avoid non-iterable error
            data = json.loads(serializers.serialize('json', newrecord))
        # send json response with updated object
            return JsonResponse(data, safe=False)

        if (request.method == "DELETE"):
        # delete the item, get all remaining records for response
            Todo.objects.filter(pk=id).delete()
            newrecord = Todo.objects.all()
        # Turn the results to json to dict, put in array to avoid non-iterable error
            data = json.loads(serializers.serialize('json', newrecord))
        # send json response with updated object
            return JsonResponse(data, safe=False)
