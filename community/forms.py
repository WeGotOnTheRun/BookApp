from django import forms
from community import models


class WriteQuestion(forms.ModelForm):

    class Meta:
        model = models.Question
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super(WriteQuestion, self).__init__(*args, **kwargs)
        self.fields['content'].widget = forms.TextInput(
            attrs={
                'id': 'contentid',
                'class': 'form-control',
                'name': 'content',
                'placeholder': 'Question Content',
            }
        )
        self.fields['content'].required = True


class WriteAnswer(forms.ModelForm):

    class Meta:
        model = models.Answer
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super(WriteAnswer, self).__init__(*args, **kwargs)
        self.fields['content'].widget = forms.TextInput(
            attrs={
                'id': 'contentid',
                'class': 'form-control',
                'name': 'content',
                'placeholder': 'Answer Content',
            }
        )
        self.fields['content'].required = True
