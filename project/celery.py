
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# إعداد Django's settings module كإعدادات Celery الافتراضية
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

# استخدام سلسلة نصية هنا يعني أن العامل لن يحتاج إلى
# إعادة التشغيل عند تحديث ملفات الإعدادات.
app.config_from_object('django.conf:settings', namespace='CELERY')

# اكتشاف المهام غير الموجودة في `tasks.py` في تطبيقات Django.
app.autodiscover_tasks()