from rest_framework.views import APIView
from rest_framework.response import Response
from apps.students.models import Student
from apps.teachers.models import Teacher
from apps.classes.models import ClassInfo
from apps.courses.models import Course
from apps.scores.models import Score
from apps.users.permissions import IsAdminOrTeacher


class DashboardView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def get(self, request):
        user = request.user
        if user.role == 'admin':
            return Response({
                'student_count': Student.objects.count(),
                'teacher_count': Teacher.objects.count(),
                'class_count': ClassInfo.objects.count(),
                'course_count': Course.objects.count(),
            })
        class_ref = user.teacher_profile.class_ref
        return Response({
            'student_count': Student.objects.filter(class_ref=class_ref).count(),
            'teacher_count': 1,
            'class_count': 1,
            'course_count': Course.objects.filter(class_ref=class_ref).count(),
        })


class ScoreDistributionView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def get(self, request):
        course_id = request.query_params.get('course')
        qs = Score.objects.all()
        if course_id:
            qs = qs.filter(course_id=course_id)
        if request.user.role == 'teacher':
            class_ref = request.user.teacher_profile.class_ref
            qs = qs.filter(student__class_ref=class_ref)
        levels = {'优秀': 0, '良好': 0, '中等': 0, '及格': 0, '不及格': 0}
        for s in qs:
            if s.score >= 90:
                levels['优秀'] += 1
            elif s.score >= 80:
                levels['良好'] += 1
            elif s.score >= 70:
                levels['中等'] += 1
            elif s.score >= 60:
                levels['及格'] += 1
            else:
                levels['不及格'] += 1
        return Response(levels)


class ClassStudentsView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def get(self, request):
        classes = ClassInfo.objects.all()
        data = [{'name': c.name, 'count': c.student_count} for c in classes]
        return Response(data)
