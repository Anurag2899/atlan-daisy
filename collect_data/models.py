from django.db import models


class Form(models.Model):
    title = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    


class Question(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=255)
    mandatory = models.BooleanField(default=False)
    


class Response(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="responses")
    


class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    
