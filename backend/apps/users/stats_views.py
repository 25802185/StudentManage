from django.db.models import Q
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
        class_ref = getattr(user, 'teacher_profile', None)
        class_ref = class_ref.class_ref if class_ref else None
        return Response({
            'student_count': Student.objects.filter(class_ref=class_ref).count() if class_ref else 0,
            'teacher_count': 1,
            'class_count': 1,
            'course_count': Course.objects.filter(class_ref=class_ref).count() if class_ref else 0,
        })


class ScoreDistributionView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def get(self, request):
        course_id = request.query_params.get('course')
        class_ref = request.query_params.get('class_ref')
        qs = Score.objects.select_related('student', 'course').all()
        if course_id:
            qs = qs.filter(course_id=course_id)
        if class_ref:
            qs = qs.filter(student__class_ref_id=class_ref)
        if request.user.role == 'teacher':
            profile = getattr(request.user, 'teacher_profile', None)
            if profile and profile.class_ref:
                qs = qs.filter(student__class_ref=profile.class_ref)
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


class PendingReviewsView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def get(self, request):
        from apps.students.models import InfoChangeRequest
        qs = InfoChangeRequest.objects.select_related('student').filter(status='pending')
        if request.user.role == 'teacher':
            profile = getattr(request.user, 'teacher_profile', None)
            if profile and profile.class_ref:
                qs = qs.filter(student__class_ref=profile.class_ref)
        data = [{
            'id': r.id,
            'student_name': r.student.name,
            'field_name': r.field_name,
            'old_value': r.old_value,
            'new_value': r.new_value,
            'created_at': r.created_at.strftime('%Y-%m-%d %H:%M'),
        } for r in qs[:10]]
        return Response(data)


class RecentLogsView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def get(self, request):
        from apps.logs.models import OperationLog
        logs = OperationLog.objects.select_related('user').order_by('-created_at')[:8]
        data = [{
            'id': l.id,
            'user': l.user.username if l.user else '系统',
            'action': l.action,
            'target': l.target,
            'detail': l.detail[:50] if l.detail else '',
            'created_at': l.created_at.strftime('%m-%d %H:%M'),
        } for l in logs]
        return Response(data)


class ScoreTrendView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def get(self, request):
        from django.db.models import Avg
        qs = Score.objects.select_related('course', 'student')
        if request.user.role == 'teacher':
            profile = getattr(request.user, 'teacher_profile', None)
            if profile and profile.class_ref:
                qs = qs.filter(student__class_ref=profile.class_ref)
        trend = (
            qs.values('course__semester__name')
            .annotate(avg=Avg('score'))
            .order_by('course__semester__name')
        )
        data = [{'semester': t['course__semester__name'], 'avg': round(t['avg'], 1)} for t in trend]
        return Response(data)


class GenderDistributionView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def get(self, request):
        qs = Student.objects.all()
        if request.user.role == 'teacher':
            profile = getattr(request.user, 'teacher_profile', None)
            if profile and profile.class_ref:
                qs = qs.filter(class_ref=profile.class_ref)
        male = qs.filter(gender='male').count()
        female = qs.filter(gender='female').count()
        return Response({'男': male, '女': female})


class ClassAvgScoreView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def get(self, request):
        from django.db.models import Avg
        qs = Score.objects.select_related('student__class_ref')
        if request.user.role == 'teacher':
            profile = getattr(request.user, 'teacher_profile', None)
            if profile and profile.class_ref:
                qs = qs.filter(student__class_ref=profile.class_ref)
        result = (
            qs.values('student__class_ref__name')
            .annotate(avg=Avg('score'))
            .order_by('student__class_ref__name')
        )
        data = [
            {'name': r['student__class_ref__name'] or '未分班', 'avg': round(r['avg'], 1)}
            for r in result
        ]
        return Response(data)


class ScoreSummaryView(APIView):
    permission_classes = [IsAdminOrTeacher]

    def get(self, request):
        qs = Score.objects.select_related('student', 'course')
        # 复用成绩列表的筛选逻辑
        class_ref = request.query_params.get('student__class_ref')
        course = request.query_params.get('course')
        semester = request.query_params.get('course__semester')
        search = request.query_params.get('search')
        if class_ref:
            qs = qs.filter(student__class_ref_id=class_ref)
        if course:
            qs = qs.filter(course_id=course)
        if semester:
            qs = qs.filter(course__semester=semester)
        if search:
            qs = qs.filter(
                Q(student__name__icontains=search) |
                Q(student__student_no__icontains=search)
            )
        if request.user.role == 'teacher':
            profile = getattr(request.user, 'teacher_profile', None)
            if profile and profile.class_ref:
                qs = qs.filter(student__class_ref=profile.class_ref)

        total = qs.count()
        if total == 0:
            return Response({'total': 0, 'avg': 0, 'excellent_rate': 0, 'pass_rate': 0})

        from django.db.models import Avg
        avg = qs.aggregate(avg=Avg('score'))['avg'] or 0
        excellent = qs.filter(score__gte=90).count()
        passed = qs.filter(score__gte=60).count()
        return Response({
            'total': total,
            'avg': round(avg, 1),
            'excellent_rate': round(excellent / total * 100, 1),
            'pass_rate': round(passed / total * 100, 1),
        })
