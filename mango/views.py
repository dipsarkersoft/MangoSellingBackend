from django.shortcuts import render
from rest_framework import viewsets
from .models import MangoModels
from .serializers import MangoSerializer
from profiles.permission import IsSeller
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from categories.models import CategoriesModel
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination


class MangoListView(APIView):

    def get(self, request):
        cat_id = request.query_params.get('cat_id', None)
        search_query = request.query_params.get('search', None)
        if cat_id:
            try:
                mango=MangoModels.objects.filter(categories_id=cat_id)
            except MangoModels.DoesNotExist:
                return Response({'message':"Category Not Found"})
        else:
            mango=MangoModels.objects.all()
            
        
        if search_query:
            mango = mango.filter(
                name__icontains=search_query  # Case-insensitive search for name
            ).union(
                mango.filter(description__icontains=search_query)  # Case-insensitive search for description
            ) 
        
        # paginator = PageNumberPagination()
        # paginator.page_size = 1  
        # result_page = paginator.paginate_queryset(mango, request)
        # serializer = MangoSerializer(result_page, many=True)  
        # return paginator.get_paginated_response({
        #     'data': serializer.data,
        #     'message': 'All Products'
        # })
        
        serializer=MangoSerializer(mango,many=True)
        return Response({
            'data':serializer.data,
            'message':'All Product '
        }) 
      


class MangoCreateView(APIView):
    permission_classes=[IsSeller]
    serializer_class=MangoSerializer

    def post(self, request):
        serializer = MangoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data,
                'status':'sucess'
                }
                )
        return Response(
            ({
                'data': serializer.errors,
                'status':'sucess'
                }
                )
        )




class MangoDetailView(APIView):
   
    def get(self, request, id):
        try:
           
            mango = MangoModels.objects.get(id=id)
        except MangoModels.DoesNotExist:
          
            raise NotFound({'error': 'Mango not found'})
        
        serializer = MangoSerializer(mango)
        return Response({
            'data': serializer.data,
            'message': 'Mango details GEt successfully'
        })


class MangoUpDelView(APIView):
    permission_classes=[IsSeller]
    serializer_class=MangoSerializer


    def put(self, request,id):      
        try:
            mango = MangoModels.objects.get(id=id)
        except MangoModels.DoesNotExist:
            return Response({'error': 'Mango not found'})

        serializer = MangoSerializer(mango, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self,request,id):
        try:
             mango = MangoModels.objects.get(id=id)
        except MangoModels.DoesNotExist:
            return Response({'error': 'Mango not found'})
        mango.delete()
        return Response({'message': 'Mango deleted successfully'})


    

    

   

        




     