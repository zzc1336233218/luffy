from rest_framework.generics import ListAPIView
from .models import CourseCategory
from .serializers import CourseCategoryModelSerializer
class CourseCategoryListAPIView(ListAPIView):
    """
    课程分类
    """
    queryset = CourseCategory.objects.filter(is_show=True, is_deleted=False).order_by("orders","-id")
    serializer_class = CourseCategoryModelSerializer


# from .models import Course
# from .serializers import CourseModelSerializer
# class CourseListAPIView(ListAPIView):
#     queryset = Course.objects.filter(is_show=True, is_deleted=False).order_by("orders","-id")
#     serializer_class = CourseModelSerializer

from .models import Course
from .serializers import CourseModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .paginations import CoursePageNumberPagination

class CourseListAPIView(ListAPIView):
    """课程列表"""
    queryset = Course.objects.filter(is_show=True, is_deleted=False).order_by("orders","-id")
    serializer_class = CourseModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['course_category']
    ordering_fields = ('id', 'students', 'price')
    pagination_class = CoursePageNumberPagination

from rest_framework.generics import RetrieveAPIView
from .serializers import CourseRetrieveModelSerializer
class CourseRetrieveAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_show=True, is_deleted=False).order_by("orders","-id")
    serializer_class = CourseRetrieveModelSerializer

from rest_framework.generics import ListAPIView
from .models import CourseChapter
from .serializers import CourseChapterModelSerializer
from django_filters.rest_framework import DjangoFilterBackend

class CourseChapterListAPIView(ListAPIView):
    queryset = CourseChapter.objects.filter(is_show=True, is_deleted=False).order_by("orders","-id")
    serializer_class = CourseChapterModelSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course']
