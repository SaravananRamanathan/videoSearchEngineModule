from django import forms
"""import random
import os

def generate_unique_name(path):
    def wrapper(instance, filename):
        extension = "." + filename.split('.')[-1]
        filename = str(random.randint(10,99)) + str(random.randint(10,99)) + str(random.randint(10,99)) + str(random.randint(10,99))  + extension
        return os.path.join(path, filename)
    return wrapper"""
class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()
    #file = forms.FileField(upload_to=generate_unique_name('/'))