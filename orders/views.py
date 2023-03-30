from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Order
from .serializers import OrderSerializer
from .tasks import get_orders


@api_view(['GET'])
@permission_classes((AllowAny,))
def health_check(request):
    """
    Healthcheck for this API in Docker container
    """
    return Response({'status': 'Ok'})


class OrderViewSet(ModelViewSet):
    """
    CRUD for Order model. Allows only get data.
    """

    queryset = Order.objects.all().order_by('seq_num')
    http_method_names = ['get']
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        get_orders.delay()

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        get_orders.delay()

        return super().retrieve(request, *args, **kwargs)
