from django.shortcuts import render
from django.http import HttpResponse

from .apps import RsAppConfig

from model_utils import *

#from . serializer import *
#from . models import *
#from rest_framework.views import APIView
#from rest_framework.response import Response

def rate_form(request):
    num_book_to_show = 10
    col_indices = np.random.randint(low=0, high=RsAppConfig.num_book, size=num_book_to_show)
    title_list, RsAppConfig.col_indices = return_random_titles(col_indices, RsAppConfig.isbn, RsAppConfig.title)
    return render(request, 'form.html', {'book_list': title_list})

def search_result(request):
    if request.method == "GET":
        partial_ratings = request.GET.getlist('rating_list')
        user_ratings = find_user_ratings(RsAppConfig.col_indices, partial_ratings, RsAppConfig.num_book)
        title_list = find_top_similar_users(user_ratings, RsAppConfig.embed_mat, RsAppConfig.high_ratings, 
            RsAppConfig.high_ratings_book_inds, RsAppConfig.users_db, 
            RsAppConfig.isbn, RsAppConfig.title)
    return render(request, 'search_result.html', {'return_list': title_list})

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