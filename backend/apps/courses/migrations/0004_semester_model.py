from django.db import migrations, models
import django.db.models.deletion


def create_semesters(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Semester = apps.get_model('courses', 'Semester')
    # 从现有课程中提取不重复的学期字符串
    semester_values = set(Course.objects.values_list('semester_old', flat=True))
    semester_values.discard('')
    semester_values.discard(None)
    if not semester_values:
        semester_values = {'2025-2026-1'}
    # 按名称倒序排列，第一个标记为当前学期
    sorted_values = sorted(semester_values, reverse=True)
    semester_map = {}
    for i, name in enumerate(sorted_values):
        sem = Semester.objects.create(name=name, is_current=(i == 0))
        semester_map[name] = sem
    # 更新课程的学期外键
    for course in Course.objects.all():
        sem = semester_map.get(course.semester_old)
        if sem:
            Course.objects.filter(pk=course.pk).update(semester=sem)


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_semester'),
    ]

    operations = [
        # 1. 创建 Semester 表
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='学期名称')),
                ('is_current', models.BooleanField(default=False, verbose_name='当前学期')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '学期',
                'verbose_name_plural': '学期',
                'db_table': 'semesters',
                'ordering': ['-name'],
            },
        ),
        # 2. 把旧的 semester 字段重命名为 semester_old
        migrations.RenameField(
            model_name='course',
            old_name='semester',
            new_name='semester_old',
        ),
        # 3. 添加新的 semester 外键（暂时可为空）
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='courses.semester',
                verbose_name='学期',
            ),
        ),
        # 4. 数据迁移：创建学期记录并关联课程
        migrations.RunPython(create_semesters, migrations.RunPython.noop),
        # 5. 删除旧字段
        migrations.RemoveField(
            model_name='course',
            name='semester_old',
        ),
        # 6. 将外键设为非空
        migrations.AlterField(
            model_name='course',
            name='semester',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to='courses.semester',
                verbose_name='学期',
            ),
        ),
    ]
