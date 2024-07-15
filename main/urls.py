from django.urls import path
from .views import SignupStep1View, SignupStep2View, SignupStep3View, LoginView

urlpatterns = [
    path('step1/', SignupStep1View.as_view(), name='signup_step_1'),
    path('step2/', SignupStep2View.as_view(), name='signup_step_2'),
    path('step3/', SignupStep3View.as_view(), name='signup_step_3'),
    path('login/', LoginView.as_view(), name='login'),
]
