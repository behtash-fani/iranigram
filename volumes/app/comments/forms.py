from django import forms
from .models import Comment, Response


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("phone_number", "content",)

    # phone_number = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    # content = forms.CharField(
    #     widget=forms.Textarea(
    #         attrs={'class': 'form-control', 'placeholder': 'Content'}))

    # def __init__(self, *args, **kwargs):
    #     super(CommentForm, self).__init__(*args, **kwargs)
    #     self.fields['message'].widget.attrs['style'] = 'height:120px;'


# class ResponseForm(forms.ModelForm):
#     file = forms.ImageField(required=False,
#                             widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}))
#     message = forms.CharField(
#         widget=forms.Textarea(
#             attrs={'class': 'form-control', 'placeholder': 'Message'}))

#     class Meta:
#         model = Response
#         fields = ['message', 'file']

#     def __init__(self, *args, **kwargs):
#         super(ResponseForm, self).__init__(*args, **kwargs)
#         self.fields['message'].widget.attrs['style'] = 'height:120px;'
