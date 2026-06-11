import io
from datetime import datetime
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status as http_status
from django_filters.rest_framework import DjangoFilterBackend
import openpyxl

from rest_framework.permissions import IsAuthenticated
from .models import Score
from .serializers import ScoreSerializer, ScoreBatchSerializer
from apps.users.permissions import IsAdminOrTeacher
from apps.courses.models import Course
from apps.courses.serializers import CourseSerializer
from apps.students.models import Student


class ScoreViewSet(ModelViewSet):
    queryset = Score.objects.select_related('student', 'course').all()
    serializer_class = ScoreSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['course', 'student', 'course__semester', 'student__class_ref']
    search_fields = ['student__name', 'student__student_no', 'course__name']
    ordering_fields = ['score', 'created_at']

    def get_permissions(self):
        if self.action in ['my_courses']:
            return [IsAuthenticated()]
        if self.action in ['list', 'retrieve', 'export_excel']:
            return [IsAuthenticated()]
        return [IsAdminOrTeacher()]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == 'student':
            return qs.filter(student__user=user)
        if user.role == 'teacher' and hasattr(user, 'teacher_profile'):
            qs = qs.filter(student__class_ref=user.teacher_profile.class_ref)
        return qs

    @action(detail=False, methods=['post'], url_path='batch')
    def batch_create(self, request):
        serializer = ScoreBatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            course = Course.objects.get(id=data['course'])
        except Course.DoesNotExist:
            return Response({'detail': '课程不存在'}, status=400)
        created, updated = 0, 0
        for item in data['scores']:
            try:
                student = Student.objects.get(id=item['student'])
            except Student.DoesNotExist:
                continue
            _, is_new = Score.objects.update_or_create(
                student=student, course=course,
                defaults={'score': item['score']},
            )
            if is_new:
                created += 1
            else:
                updated += 1
        return Response({'detail': f'新增 {created} 条，更新 {updated} 条成绩'})

    @action(detail=False, methods=['get'], url_path='my-courses')
    def my_courses(self, request):
        student = Student.objects.filter(user=request.user).first()
        if not student:
            return Response([])
        course_ids = Score.objects.filter(student=student).values_list('course_id', flat=True).distinct()
        courses = Course.objects.filter(id__in=course_ids)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='export')
    def export_excel(self, request):
        course_id = request.query_params.get('course')
        qs = self.get_queryset()
        if course_id:
            qs = qs.filter(course_id=course_id)
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = '成绩'
        headers = ['学号', '姓名', '课程', '成绩', '学期']
        ws.append(headers)
        for s in qs:
            ws.append([
                s.student.student_no, s.student.name,
                s.course.name, s.score, s.course.semester.name,
            ])
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = f'attachment; filename=scores_{datetime.now():%Y%m%d}.xlsx'
        return response
