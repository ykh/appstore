import os
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


class UnitTestHelpers:
    @staticmethod
    def generate_file(name='test.png'):
        file = BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(file, 'PNG')
        file.seek(0)

        return SimpleUploadedFile(name, file.read(), content_type='image/png')

    @staticmethod
    def generate_temp_file():
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        image = Image.new('RGB', (100, 100), color='red')
        image.save(temp_file, format='PNG')
        temp_file.seek(0)

        return temp_file

    @staticmethod
    def delete_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
