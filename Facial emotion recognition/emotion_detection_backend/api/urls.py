from django.urls import path
from .views import EmotionDetectionView

urlpatterns = [
    path('predict/', EmotionDetectionView.as_view(), name='emotion_predict'),
]
