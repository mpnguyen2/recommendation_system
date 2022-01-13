from django.shortcuts import render
from django.http import HttpResponse

#from . serializer import *
#from . models import *
from rest_framework.views import APIView
from rest_framework.response import Response


def rate_form(request):
    return render(request, 'form.html', {'book_list':['Linear algebra', 'Analysis']})

def search_result(request):
    if request.method == "GET":
        rating_list = request.GET.getlist('rating_list')
        print(rating_list)
    return render(request, 'search_result.html', {'rating_list': rating_list})

'''
class ReactView(APIView):
    
    serializer_class = ReactSerializer
  
    def get(self, request):
        detail = [ {"name": detail.name,"detail": detail.detail} 
        for detail in React.objects.all()]
        return Response(detail)
  
    def post(self, request):
  
        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return  Response(serializer.data)

#from django.http import HttpResponse

#def index(requests):
    #return HttpResponse('Hello. You\'re at index page')

    def view1(request):
'''