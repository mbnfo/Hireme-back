from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),name = 'token_refresh'),

    path('authentification/<str:pk>/', views.createUser, name = 'createUser'),

    path('get/model/', views.getModelType, name = 'getModelTypes'),
    path('home/get/workers/<str:job_id>/', views.getWorkers, name = 'getWorkers'),
    path('home/get/reciept/<str:worker_id>/', views.getReciept, name = 'getReciept'),
    path('home/get/worker/reciepts/', views.getReciepts, name = 'multiple_reciepts'),
    path('home/get/reviews/<str:review_type>/<str:worker_get_id>/', views.getReview, name = 'getReview'),
    path('home/get/problem/', views.getProblem, name = 'getProblem'), 
    path('home/get/notifications/<str:request_type>/', views.getNotifications, name = 'notifications'),
    path('home/get/jobs/', views.getJobs, name = 'jobs'),
    path('home/get/basket/', views.consumerData, name = 'consumerData'),
    path('home/get/bids/<str:problem_id>/', views.getBids, name = 'getBids'),
    path('home/get/bids/bid/<str:bid_id>/', views.getBid, name = 'getBid'),
    path('home/get/candidate/<str:bid_id>/', views.getCandidate, name = 'getCandidate'),

    path('home/problem/bid/accept/', views.acceptBid, name = 'acceptBid'),
    path('home/problem/reciept/cancel/<str:problem_id>/', views.cancelReciept, name = 'cancelReciept'),
    path('home/problem/bid/reject/', views.rejectBid, name = 'rejectBid'),

    path('create/user/', views.createUser, name = 'CreateUser'),
    path('create/user/settings/<str:pk>/', views.settings, name = 'settings'),
    path('home/create/problem/', views.createProblem, name = 'createProblem'),
    path('home/create/bid/<str:problem_id>/', views.createBid, name = 'createBid'),
    path('home/create/review/<str:worker_id>/', views.createReview, name = 'createReview'),
]

'''
paths:
    get_models:
        http://127.0.0.1:8000/api/home/get/model/
    create_models:
        http://127.0.0.1:8000/api/home/create/model/
    create_models_with_id:
        http://127.0.0.1:8000/api/home/create/model/id/
'''