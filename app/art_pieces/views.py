from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from art_pieces.models import Portfolio
from art_pieces.serializers import PortfolioSerializer
from rest_framework.decorators import api_view

# Create your views here.
# def index(request):
#     return render(request, "tutorials/index.html")


def index(request):
    print("------------------------- I AM HERE")
    queryset = Portfolio.objects.all()
    return render(request, "art_pieces/index.html", {'art_pieces': queryset})


class index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'art_pieces/index.html'

    def get(self, request):
        queryset = Portfolio.objects.all()
        return Response({'art_pieces': queryset})


class list_all_tutorials(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'art_pieces/portfolio_list.html'

    def get(self, request):
        queryset = Portfolio.objects.all()
        return Response({'art_pieces': queryset})


# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def portfolio_list(request):
    if request.method == 'GET':
        art_pieces = Portfolio.objects.all()

        title = request.GET.get('title', None)
        if title is not None:
            art_pieces = art_pieces.filter(title__icontains=title)

        art_pieces_serializer = PortfolioSerializer(art_pieces, many=True)
        return JsonResponse(art_pieces_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        portfolio_data = JSONParser().parse(request)
        portfolio_serializer = PortfolioSerializer(data=portfolio_data)
        if portfolio_serializer.is_valid():
            portfolio_serializer.save()
            return JsonResponse(portfolio_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(portfolio_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Portfolio.objects.all().delete()
        return JsonResponse(
            {
                'message':
                '{} Art pieces were deleted successfully!'.format(count[0])
            },
            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def portfolio_detail(request, pk):
    try:
        portfolio = Portfolio.objects.get(pk=pk)
    except Portfolio.DoesNotExist:
        return JsonResponse({'message': 'The art piece does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        portfolio_serializer = PortfolioSerializer(portfolio)
        return JsonResponse(portfolio_serializer.data)

    elif request.method == 'PUT':
        portfolio_data = JSONParser().parse(request)
        portfolio_serializer = PortfolioSerializer(portfolio, data=portfolio_data)
        if portfolio_serializer.is_valid():
            portfolio_serializer.save()
            return JsonResponse(portfolio_serializer.data)
        return JsonResponse(portfolio_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        portfolio.delete()
        return JsonResponse({'message': 'Art piece was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def portfolio_list_published(request):
    art_pieces = Portfolio.objects.filter(published=True)

    if request.method == 'GET':
        portfolio_serializer = PortfolioSerializer(art_pieces, many=True)
        return JsonResponse(portfolio_serializer.data, safe=False)