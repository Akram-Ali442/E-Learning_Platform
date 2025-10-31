# courses/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Subject, Course, Module, Content, Text, Video, Image, File
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

class Command(BaseCommand):
    help = 'يملء قاعدة البيانات ببيانات تجريبية للتعليم'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='حذف جميع البيانات قبل إضافة البيانات الجديدة',
        )
    
    def handle(self, *args, **options):
        self.stdout.write('🚀 بدء إضافة البيانات إلى النظام...')
        
        # حذف البيانات إذا طلب المستخدم
        if options['clear']:
            self.clear_data()
        
        with transaction.atomic():
            self.create_users()
            self.create_subjects()
            self.create_courses()
            self.create_modules()
            self.create_contents()
            self.generate_report()
        
        self.stdout.write(self.style.SUCCESS('🎉 تم الانتهاء من إضافة جميع البيانات!'))
    
    def clear_data(self):
        """حذف جميع البيانات من قاعدة البيانات"""
        self.stdout.write('🗑️  جاري حذف جميع البيانات...')
        
        # حذف المحتويات أولاً (بسبب العلاقات)
        Content.objects.all().delete()
        self.stdout.write('   ✅ تم حذف المحتويات')
        
        # حذف النماذج المختلفة
        Text.objects.all().delete()
        Video.objects.all().delete()
        Image.objects.all().delete()
        File.objects.all().delete()
        self.stdout.write('   ✅ تم حذف النصوص والفيديوهات والصور والملفات')
        
        # حذف الوحدات
        Module.objects.all().delete()
        self.stdout.write('   ✅ تم حذف الوحدات')
        
        # حذف الكورسات
        Course.objects.all().delete()
        self.stdout.write('   ✅ تم حذف الكورسات')
        
        # حذف المواد (مع الاحتفاظ بالمستخدمين)
        Subject.objects.all().delete()
        self.stdout.write('   ✅ تم حذف المواد الدراسية')
        
        # حذف المستخدمين ما عدا superuser
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write('   ✅ تم حذف المستخدمين (ما عدا superuser)')
        
        self.stdout.write('✨ تم تنظيف قاعدة البيانات بالكامل')
    
    def create_users(self):
        self.stdout.write('👥 جاري إنشاء المستخدمين...')
        
        users_data = [
            {
                'username': 'ahmed_teacher', 
                'password': 'teacher123', 
                'first_name': 'أحمد', 
                'last_name': 'علي', 
                'is_staff': True
            },
            {
                'username': 'sara_teacher', 
                'password': 'teacher123', 
                'first_name': 'سارة', 
                'last_name': 'محمد', 
                'is_staff': True
            },
            {
                'username': 'mohamed_student', 
                'password': 'student123', 
                'first_name': 'محمد', 
                'last_name': 'خالد', 
                'is_staff': False
            },
        ]
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_staff': user_data['is_staff']
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'   ✅ تم إنشاء المستخدم: {user.username}')
    
    def create_subjects(self):
        self.stdout.write('📚 جاري إنشاء المواد الدراسية...')
        
        subjects_data = [
            {'title': 'الرياضيات', 'slug': 'mathematics'},
            {'title': 'الفيزياء', 'slug': 'physics'},
            {'title': 'البرمجة', 'slug': 'programming'},
        ]
        
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                slug=subject_data['slug'],
                defaults={'title': subject_data['title']}
            )
            if created:
                self.stdout.write(f'   ✅ تم إنشاء المادة: {subject.title}')
    
    def create_courses(self):
        self.stdout.write('🎓 جاري إنشاء الكورسات...')
        
        ahmed = User.objects.get(username='ahmed_teacher')
        sara = User.objects.get(username='sara_teacher')
        math = Subject.objects.get(slug='mathematics')
        programming = Subject.objects.get(slug='programming')
        
        courses_data = [
            {
                'owner': ahmed, 
                'subject': math, 
                'title': 'الجبر الأساسي', 
                'slug': 'basic-algebra', 
                'overview': 'دورة الجبر للمبتدئين'
            },
            {
                'owner': sara, 
                'subject': programming, 
                'title': 'Python للمبتدئين', 
                'slug': 'python-basics', 
                'overview': 'تعلم البرمجة بلغة Python'
            },
        ]
        
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                slug=course_data['slug'],
                defaults=course_data
            )
            if created:
                self.stdout.write(f'   ✅ تم إنشاء الكورس: {course.title}')
    
    def create_modules(self):
        self.stdout.write('📝 جاري إنشاء الوحدات الدراسية...')
        
        algebra_course = Course.objects.get(slug='basic-algebra')
        python_course = Course.objects.get(slug='python-basics')
        
        modules_data = [
            {
                'course': algebra_course, 
                'title': 'مقدمة في الجبر', 
                'description': 'المفاهيم الأساسية للجبر'
            },
            {
                'course': algebra_course, 
                'title': 'المعادلات الخطية', 
                'description': 'حل المعادلات من الدرجة الأولى'
            },
            {
                'course': python_course, 
                'title': 'أساسيات Python', 
                'description': 'المتغيرات والعمليات الأساسية'
            },
        ]
        
        for module_data in modules_data:
            module, created = Module.objects.get_or_create(
                course=module_data['course'],
                title=module_data['title'],
                defaults={'description': module_data['description']}
            )
            if created:
                self.stdout.write(f'   ✅ تم إنشاء الوحدة: {module.title}')
    
    def create_contents(self):
        self.stdout.write('📄 جاري إنشاء المحتويات التعليمية...')
        
        ahmed = User.objects.get(username='ahmed_teacher')
        sara = User.objects.get(username='sara_teacher')
        
        algebra_intro = Module.objects.get(title='مقدمة في الجبر')
        algebra_equations = Module.objects.get(title='المعادلات الخطية')
        python_basics = Module.objects.get(title='أساسيات Python')
        
        # الحصول على أنواع المحتوى
        text_content_type = ContentType.objects.get_for_model(Text)
        video_content_type = ContentType.objects.get_for_model(Video)
        image_content_type = ContentType.objects.get_for_model(Image)
        file_content_type = ContentType.objects.get_for_model(File)
        
        # إنشاء محتوى نصي
        text1, created_text1 = Text.objects.get_or_create(
            owner=ahmed,
            title='ما هو الجبر؟',
            defaults={
                'content': 'الجبر هو فرع من فروع الرياضيات الذي يتعامل مع الرموز والمتغيرات. يساعدنا الجبر في حل المشكلات الرياضية باستخدام رموز مثل x و y لتمثيل القيم المجهولة.'
            }
        )
        
        text2, created_text2 = Text.objects.get_or_create(
            owner=sara,
            title='مدخل إلى Python',
            defaults={
                'content': 'Python هي لغة برمجة عالية المستوى وسهلة التعلم. تتميز ببساطة تركيبها وتعدد استخداماتها في مجالات مثل تطوير الويب وتحليل البيانات والذكاء الاصطناعي.'
            }
        )
        
        # إنشاء محتوى فيديو
        video1, created_video1 = Video.objects.get_or_create(
            owner=ahmed,
            title='شرح المعادلات الخطية',
            defaults={
                'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
            }
        )
        
        # إنشاء محتوى صورة
        image1, created_image1 = Image.objects.get_or_create(
            owner=sara,
            title='مثال على كود Python',
            defaults={
                'file': 'images/python_example.png'
            }
        )
        
        # إنشاء محتوى ملف
        file1, created_file1 = File.objects.get_or_create(
            owner=ahmed,
            title='تمارين الجبر',
            defaults={
                'file': 'files/algebra_exercises.pdf'
            }
        )
        
        # ربط المحتويات بالوحدات
        content_objects = [
            (algebra_intro, text1, text_content_type, 'النص'),
            (python_basics, text2, text_content_type, 'النص'),
            (algebra_equations, video1, video_content_type, 'الفيديو'),
            (python_basics, image1, image_content_type, 'الصورة'),
            (algebra_intro, file1, file_content_type, 'الملف'),
        ]
        
        for module, item, content_type, type_name in content_objects:
            content, created = Content.objects.get_or_create(
                module=module,
                content_type=content_type,
                object_id=item.id,
                defaults={'order': 0}
            )
            if created:
                self.stdout.write(f'   ✅ تم ربط {type_name}: {item.title}')
    
    def generate_report(self):
        self.stdout.write('\n📊 تقرير البيانات المضافة:')
        self.stdout.write(f'   👥 المستخدمين: {User.objects.count()}')
        self.stdout.write(f'   📚 المواد: {Subject.objects.count()}')
        self.stdout.write(f'   🎓 الكورسات: {Course.objects.count()}')
        self.stdout.write(f'   📝 الوحدات: {Module.objects.count()}')
        self.stdout.write(f'   📄 المحتويات: {Content.objects.count()}')
        
        # عرض المحتويات لكل وحدة
        self.stdout.write('\n🔍 المحتويات حسب الوحدات:')
        for module in Module.objects.all():
            contents = module.contents.all()
            self.stdout.write(f'   📖 {module.title}: {contents.count()} محتوى')
            for content in contents:
                item_type = content.content_type.model
                item_title = content.item.title if content.item else 'غير معروف'
                self.stdout.write(f'      - {item_title} (نوع: {item_type})')