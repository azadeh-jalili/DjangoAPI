from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from tp_book.models import Book
from tp_book.serializers import BookModelSerializer
from rest_framework.decorators import api_view


class GetAllData(APIView):  # class Base
    def get(self, request):
        query = Book.objects.all().order_by('-created_at')
        serializers = BookModelSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def allAPI(request):  # Function Base
    if request.method == 'GET':
        query = Book.objects.all().order_by('-created_at')
        serializer = BookModelSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetFavData(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = Book.objects.filter(fav=True)
        serializers = BookModelSerializer(query, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class UpdateFavData(APIView):
    def get(self, request, pk):
        query = Book.objects.get(pk=pk)
        serializer = BookModelSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = Book.objects.get(pk=pk)
        serializers = BookModelSerializer(query, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class PostModelData(APIView):  # class based
    def post(self, request):
        serializer = BookModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def SetData(request):
    if request.method == 'POST':
        serializer = BookModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchData(APIView):
    def get(self, request):
        search = request.GET['name']
        query = Book.objects.filter(store_name__contains=search)
        serializer = BookModelSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteData(APIView):
    def get(self, request, pk):
        query = Book.objects.get(pk=pk)
        serializer = BookModelSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        query = Book.objects.get(pk=pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
