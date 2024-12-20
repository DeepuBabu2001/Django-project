from django import forms
from .models import MovieStore,Plan


class AdminloginForm(forms.Form):
        email = forms.CharField()
        password = forms.CharField()

class ForgotForm(forms.Form):
     email = forms.CharField() 


class ResetForm(forms.Form):
     newpassword = forms.CharField()
     confirm = forms.CharField()



class MovieModelForm(forms.ModelForm):
    class Meta:
        model = MovieStore
        fields = ['moviename', 'description','thumbnail','video']


class PlanForm(forms.ModelForm):
     class Meta:
          model = Plan  
          fields = ['planname','description','price','duration',] 



















    