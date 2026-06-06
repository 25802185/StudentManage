from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.classes.models import ClassInfo
from apps.teachers.models import Teacher
from apps.students.models import Student


class Command(BaseCommand):
    help = '生成测试数据'

    def handle(self, *args, **options):
        # 重置管理员密码
        admin = User.objects.filter(username='admin').first()
        if admin:
            admin.set_password('123456')
            admin.save()
            self.stdout.write('管理员密码已重置为 123456')
        else:
            admin = User.objects.create_superuser('admin', 'admin@example.com', '123456')
            admin.role = 'admin'
            admin.save()
            self.stdout.write('管理员账号已创建: admin / 123456')

        # 班级数据
        classes_data = [
            {'name': '计算机科学与技术一班', 'grade': '2022级', 'major': '计算机科学与技术'},
            {'name': '软件工程一班', 'grade': '2022级', 'major': '软件工程'},
            {'name': '数据科学一班', 'grade': '2023级', 'major': '数据科学与大数据技术'},
            {'name': '人工智能一班', 'grade': '2023级', 'major': '人工智能'},
        ]

        # 教师数据（每个班级一个班主任）
        teachers_data = [
            {'teacher_no': 'T2022001', 'name': '王建国', 'gender': 'male', 'title': '副教授'},
            {'teacher_no': 'T2022002', 'name': '李秀梅', 'gender': 'female', 'title': '讲师'},
            {'teacher_no': 'T2023001', 'name': '张志远', 'gender': 'male', 'title': '教授'},
            {'teacher_no': 'T2023002', 'name': '陈晓燕', 'gender': 'female', 'title': '副教授'},
        ]

        # 学生姓名库（真实感中文名）
        male_names = [
            '张伟', '王磊', '李强', '刘洋', '陈浩', '杨帆', '赵鑫', '黄勇',
            '周杰', '吴涛', '徐明', '孙亮', '马超', '朱军', '胡鑫', '郭鹏',
            '林峰', '何宇', '高飞', '罗晨', '谢斌', '韩冰', '唐杰', '曹阳',
            '许超', '邓威', '冯刚', '程龙', '蔡鑫', '彭浩', '潘旭', '袁博',
            '蒋磊', '余洋', '于亮', '叶枫', '田宇', '董健', '范伟', '苏明',
        ]
        female_names = [
            '王芳', '李娜', '张敏', '刘静', '陈丽', '杨柳', '赵婷', '黄燕',
            '周莉', '吴霞', '徐颖', '孙玲', '马兰', '朱琳', '胡蝶', '郭婧',
            '林雪', '何婷', '高洁', '罗佳', '谢芳', '韩梅', '唐静', '曹颖',
            '许晴', '邓丽', '冯娟', '程璐', '蔡婷', '彭蕾', '潘雅', '袁媛',
            '蒋雯', '余欢', '于倩', '叶蓁', '田甜', '董悦', '苏瑶', '方怡',
        ]

        # 创建班级和教师
        classes = []
        teachers = []
        for i, (cls_data, tch_data) in enumerate(zip(classes_data, teachers_data)):
            cls, _ = ClassInfo.objects.get_or_create(
                name=cls_data['name'],
                defaults={'grade': cls_data['grade'], 'major': cls_data['major']},
            )
            classes.append(cls)

            user, _ = User.objects.get_or_create(
                username=tch_data['teacher_no'],
                defaults={'role': 'teacher'},
            )
            user.set_password('123456')
            user.save()

            teacher, _ = Teacher.objects.get_or_create(
                teacher_no=tch_data['teacher_no'],
                defaults={
                    'user': user, 'name': tch_data['name'], 'gender': tch_data['gender'],
                    'title': tch_data['title'], 'class_ref': cls,
                },
            )
            teachers.append(teacher)
            self.stdout.write(f'班级: {cls.name} | 班主任: {teacher.name}')

        # 创建学生
        male_idx = 0
        female_idx = 0
        for cls_idx, cls in enumerate(classes):
            count = 0
            for i in range(20):
                if i % 2 == 0:
                    name = male_names[male_idx % len(male_names)]
                    gender = 'male'
                    male_idx += 1
                else:
                    name = female_names[female_idx % len(female_names)]
                    gender = 'female'
                    female_idx += 1

                student_no = f'2022{cls_idx + 1:02d}{i + 1:03d}'
                age = 20 if cls.grade == '2022级' else 19

                user, created = User.objects.get_or_create(
                    username=student_no,
                    defaults={'role': 'student'},
                )
                user.set_password('123456')
                user.save()

                student, created = Student.objects.get_or_create(
                    student_no=student_no,
                    defaults={
                        'user': user, 'name': name, 'gender': gender, 'age': age,
                        'class_ref': cls, 'phone': f'138{student_no[-8:]}',
                        'email': f'{student_no}@stu.edu.cn',
                        'address': 'XX省XX市XX区XX路XX号',
                    },
                )
                if created:
                    count += 1

            cls.student_count = cls.students.count()
            cls.save()
            self.stdout.write(f'{cls.name}: 创建 {count} 名学生')

        # 创建课程
        from apps.courses.models import Course
        from apps.scores.models import Score
        import random

        courses_data = {
            '计算机科学与技术一班': [
                ('数据结构与算法', 4), ('操作系统', 3), ('计算机网络', 3),
                ('数据库原理', 3), ('软件工程导论', 2),
            ],
            '软件工程一班': [
                ('Java程序设计', 4), ('Web前端开发', 3), ('软件测试', 3),
                ('项目管理', 2), ('设计模式', 2),
            ],
            '数据科学一班': [
                ('概率论与数理统计', 4), ('机器学习', 3), ('数据挖掘', 3),
                ('Python编程', 3), ('大数据处理', 2),
            ],
            '人工智能一班': [
                ('深度学习', 4), ('自然语言处理', 3), ('计算机视觉', 3),
                ('强化学习', 3), ('智能系统设计', 2),
            ],
        }

        for cls in classes:
            for course_name, credit in courses_data.get(cls.name, []):
                Course.objects.get_or_create(
                    name=course_name, class_ref=cls,
                    defaults={
                        'credit': credit,
                        'teacher': cls.teachers.first(),
                        'description': f'{cls.name}的{course_name}课程',
                    },
                )
            self.stdout.write(f'{cls.name}: 创建 {len(courses_data.get(cls.name, []))} 门课程')

        # 为部分学生成绩打分
        semester = '2025-2026-1'
        score_count = 0
        for cls in classes:
            courses = cls.courses.all()
            students = cls.students.all()
            for course in courses:
                for student in students:
                    Score.objects.get_or_create(
                        student=student, course=course, semester=semester,
                        defaults={'score': round(random.uniform(50, 100), 1)},
                    )
                    score_count += 1
        self.stdout.write(f'创建 {score_count} 条成绩记录')

        self.stdout.write(self.style.SUCCESS('测试数据创建完成！'))
