from rest_framework import serializers
from .models import CourseCategory
class CourseCategoryModelSerializer(serializers.ModelSerializer):
    """
    课程分类序列化器
    """
    class Meta:
        model = CourseCategory
        fields = ["id","name"]

from .models import Course,Teacher

class TeacherModelSerializer(serializers.ModelSerializer):
    """
    老师信息序列化器
    """
    class Meta:
        model = Teacher
        fields = ["id","image","name","title","signature","brief"]

class CourseModelSerializer(serializers.ModelSerializer):
    """
    列表页课程信息序列化器
    """
    # 序列化器嵌套，返回外检对应的序列化器数据
    teacher = TeacherModelSerializer()
    class Meta:
        model = Course
        fields = ["id","name","students","lessons","pub_lessons","price","course_img","teacher","lessons_list","discount_name","real_price"]

class CourseRetrieveModelSerializer(serializers.ModelSerializer):
    """
    详情页课程信息序列化器
    """
    teacher = TeacherModelSerializer()
    class Meta:
        model = Course
        fields = ["id","name","students","lessons","pub_lessons","price","course_img","teacher","level_name","brief_html",
                  "course_video","discount_name","real_price","activity_time"]

from .models import CourseChapter,CourseLesson

class CourseLessonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ["id","lesson","name","free_trail"]

class CourseChapterModelSerializer(serializers.ModelSerializer):
    """
    详情页课程章节列表
    """
    coursesections = CourseLessonModelSerializer(many=True)
    class Meta:
        model = CourseChapter
        fields = ["id","chapter","name","coursesections"]