from rest_framework import serializers
from moviestore.models import AdminLogin,MovieStore,Plan

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminLogin
        fields = ['username','email','password']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieStore
        fields = [ 'id','moviename','description','thumbnail', 'video','rating']


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id','planname','description','price','duration']




