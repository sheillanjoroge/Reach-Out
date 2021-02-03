from django.test import TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import os


from .models import Hood, User


media_storage = settings.MEDIA_URL + 'profiles/'

class TestHood(TestCase):
    def setUp(self):
        self.a_user = User(username='sheilla', email='shish@gmail.com', password='123@Iiht')
        self.a_hood = Hood(name='Bamburi', location='Msa Rd', population='68971')
        self.a_user.save()
        self.a_hood.save()

    def tearDown(self):
        pass

    def test_createHood(self):
        self.a_hood.admin.add(self.a_user)

        self.assertEqual(len(Hood.objects.all()), 1)
        self.assertEqual(len(User.objects.all()), 1)

    def test_get_all_hoods(self):
        self.assertEqual(len(Hood.get_all_hoods()), 1)


class TestUser(TestCase):
    def setUp(self):
        self.a_user = User(username='sheilla', email='shish@gmail.com', password='123@Iiht')
        self.a_user.save()


    def test_default_image_present(self):
        self.assertEqual(self.a_user.picture.url, media_storage + 'default.jpg')
        
    def test_upload_profile(self):
        self.upload_image = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpg")
        self.a_user.picture = self.upload_image
        self.a_user.save()

        self.assertEqual(self.a_user.picture.name, 'profiles/file.jpg')

        directory_profiles = os.getcwd() + '\media'
        os.remove(directory_profiles + '\\' + self.a_user.picture.name)
