from django import forms
from .models import *

class UploadForm(forms.ModelForm):
    
    class Meta:
        model = Upload
        fields = ('video',)
        labels = {
            'video':"Browse file to upload"
        }

        widgets ={
            'video':forms.ClearableFileInput(attrs={'multiple': False,'hidden':True}),
        }

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.fields['video'].required = False