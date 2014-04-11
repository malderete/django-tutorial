from apps.blog.models import Post
from django.forms.widgets import Textarea
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from crispy_forms.bootstrap import FormActions
#from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
#from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


def check_size(value):
    if len(value) < 5 or len(value) > 30:
        raise ValidationError("Title shouldn't have less than 5 and more than 30 chars")

def without_asterix(value):
    if "*" in value:
        raise ValidationError("Value can't contain an asterix char")

class PostForm_0(forms.Form):

    title = forms.CharField(required=True, help_text="Help text here")
    content = Textarea(attrs={'cols': 60, 'rows': 15})


def check_title(value):
    if len(value) < 4:
        raise ValidationError("El titulo debe contener mas de 4 caracteres")
    return value


class PostForm(forms.ModelForm):
    title = forms.CharField(required=True, help_text="Aqui va el titulo del post", label="Titulo", validators=[without_asterix, check_size])

    class Meta:
        model = Post
        fields = ('title', 'content')
        widgets = {
            'content': Textarea(attrs={'cols': 60, 'rows': 15}),
        }

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Password",
        widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password",
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','last_name', 'first_name')


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

class PostFormCrispy(forms.ModelForm):
    title = forms.CharField(required=True, help_text="Aqui va el titulo del post", label="Titulo", validators=[without_asterix, check_size])

    class Meta:
        model = Post
        fields = ('title', 'content',)
        widgets = {
            'content': Textarea(attrs={'cols': 60, 'rows': 15}),
        }

    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(
            Field('author'),
            Field('title', rows="3"),
            Field('content', rows="4", cols="60"),
            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn btn-primary"),
                Submit('cancel', 'Cancel', css_class="btn btn-cancel"),
            )
        )
        return helper
