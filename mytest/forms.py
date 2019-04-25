from django import forms

class ProfileForm(forms.ModelForm):
    name = forms.CharField(max_length = 100, label='名字：')
    picture = forms.ImageField(label='图片：')