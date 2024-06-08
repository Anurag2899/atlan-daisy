from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.HealthCheck.as_view(), name="health-check"),
    path("forms/", views.FormListCreateView.as_view(), name="form-list-create"),
    path("forms/<int:pk>/", views.FormRetrieveUpdateDestroyView.as_view(), name="form-retrieve-update-destroy"),
    path("questions/", views.QuestionListCreateView.as_view(), name="question-list-create"),
    path("questions/<int:pk>/", views.QuestionRetrieveUpdateDestroyView.as_view(), name="question-retrieve-update-destroy"),
    path("responses/", views.ResponseListCreateView.as_view(), name="response-list-create"),
    path("responses/<int:pk>/", views.ResponseRetrieveUpdateDestroyView.as_view(), name="response-retrieve-update-destroy"),
    path("answers/", views.AnswerListCreateView.as_view(), name="answer-list-create"),
    path("answers/<int:pk>/", views.AnswerRetrieveUpdateDestroyView.as_view(), name="answer-retrieve-update-destroy"),
    path("forms/<int:form_id>/", views.FormView.as_view(), name="form-view"),
    path("submit/<int:form_id>/", views.FormDataView.as_view(), name="form-data"),
]
