from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from base.models import Consumer, Worker, Job, Review, Reciept, Problem, Bids, Notifications

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class BidSerializer(ModelSerializer):
    class Meta:
        model = Bids
        fields = '__all__'

class ConsumerSerializer(ModelSerializer):
    class Meta:
        model = Consumer
        fields = '__all__'

class WorkerSerializer(ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'

class JobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class RecieptSerializer(ModelSerializer):
    class Meta:
        model = Reciept
        fields = '__all__'

class ProblemSerializer(ModelSerializer):
    class Meta:
        model  = Problem
        fields = '__all__'

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'