from django.shortcuts import render
from .serializers import ProductSerializer
from rest_framework.views import APIView
from .models import product
from rest_framework.response import Response
from django.core.cache import cache
import random
class ProductList(APIView):

    def get(self,request):
        products= product.objects.all()
        serializer= ProductSerializer(products, many=True)
        return Response(serializer.data)

import logging

logger = logging.getLogger(__name__)

class CachedProductListView(APIView):
    def get(self, request):
        cache_product = cache.get("product_list")

        if cache_product is None:
            logger.info("Cache miss: Fetching products from the database.")
            products = product.objects.all()
            serializer = ProductSerializer(products, many=True)

            logger.info(f"Caching data: {serializer.data}")  # Log data being cached
            cache.set('product_list', serializer.data, timeout=60)  
            logger.info("Cache set for product_list.")
            return Response(serializer.data)

        logger.info("Cache hit: Returning cached product list.")
        return Response(cache_product)


class Addproduct(APIView):
    
    def post(self, request, number):
        products=[]
        for i in range(number):
            product={
                'name':f"product {i}",
                'price': random.randint(100,1000)
            }
            products.append(product)
        
        responses=[]
        for product in products:    
            serializer= ProductSerializer(data=product)
            if serializer.is_valid():
                serializer.save()
                responses.append(serializer.data)
            else:
                return Response(serializer.errors)
        return Response(responses)
        

    
