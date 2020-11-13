from rest_framework.generics import CreateAPIView
from .models import Order
from .serializers import OrderModelSerializer
from rest_framework.permissions import IsAuthenticated

class OrderAPIView(CreateAPIView):
    """订单试图"""
    queryset = Order.objects.filter(is_show=True,is_deleted=False)
    serializer_class = OrderModelSerializer
    permission_classes = [IsAuthenticated]