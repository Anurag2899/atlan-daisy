import os
import gspread
from rest_framework import status
from django.shortcuts import render, redirect
from django.http import Http404
from .models import Form, Question, Response, Answer
from .serializers import FormSerializer, QuestionSerializer, ResponseSerializer, AnswerSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response as APIResponse

from utils.sms import send_sms
from utils.gsheet import push_to_google_sheet


class HealthCheck(APIView):
    def get(self, request):
        return APIResponse("Health OK", status=200)


class FormListCreateView(APIView):
    def get(self, request):
        try:
            queryset = Form.objects.all()
            serializer = FormSerializer(queryset, many=True)
            return APIResponse(serializer.data, status=200)
        except Exception as e:
            return APIResponse({"error": str(e)}, status=500)

    def post(self, request):
        try:
            serializer = FormSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return APIResponse(serializer.data, status=200)
            return APIResponse({"error": "error"}, status=400)
        except Exception as e:
            return APIResponse({"error": str(e)}, status=500)


class FormRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk):
        try:
            form = Form.objects.get(pk=pk)
            serializer = FormSerializer(form)
            return APIResponse(serializer.data)
        except Form.DoesNotExist:
            return APIResponse({"error": "not found"}, status=404)
        except Exception as e:
            return APIResponse({"error": str(e)}, status=500)

    def delete(self, request, pk):
        try:
            form = Form.objects.get(pk=pk)
            form.delete()
            return Response(status=200)
        except Form.DoesNotExist:
            return APIResponse({"error": "not found"}, status=404)
        except Exception as e:
            return APIResponse({"error": str(e)}, status=500)


class QuestionListCreateView(APIView):
    def get(self, request):
        try:
            queryset = Question.objects.all()
            serializer = QuestionSerializer(queryset, many=True)
            return APIResponse(serializer.data, status=200)
        except Exception as e:
            return APIResponse({"error": str(e)}, status=500)

    def post(self, request):
        try:
            serializer = QuestionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return APIResponse(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except Exception as e:
            return APIResponse({"error": str(e)}, status=500)


class QuestionRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return None
        except Exception as e:
            raise e

    def get(self, request, pk):
        question = self.get_object(pk)
        if question is None:
            return APIResponse({"error": "not found"}, status=404)

        serializer = QuestionSerializer(question)
        return APIResponse(serializer.data)

    def put(self, request, pk):
        question = self.get_object(pk)
        if question is None:
            return APIResponse({"error": "not found"}, status=404)

        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(serializer.data)
        return APIResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        question = self.get_object(pk)
        if question is None:
            return APIResponse({"error": "not found"}, status=404)
        question.delete()
        return APIResponse(status=200)


class ResponseListCreateView(APIView):
    def get(self, request):
        try:
            queryset = Response.objects.all()
            serializer = ResponseSerializer(queryset, many=True)
            return APIResponse(serializer.data, status=200)
        except Exception as e:
            return APIResponse({"error": str(e)}, status=500)

    def post(self, request):
        try:
            serializer = ResponseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return APIResponse(serializer.data, status=200)
            return APIResponse(serializer.errors, status=400)
        except Exception as e:
            return APIResponse({"error": str(e)}, status=500)


class ResponseRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk):
        try:
            response = Response.objects.get(pk=pk)
            serializer = ResponseSerializer(response)
            return APIResponse(serializer.data)
        except Exception as e:
            return APIResponse({"error": str(e)}, status=500)

    def put(self, request, pk):
        try:
            response = Response.objects.get(pk=pk)
            serializer = ResponseSerializer(response, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return APIResponse(serializer.data)
            return APIResponse(serializer.errors, status=400)
        except Exception as e:
            return APIResponse({"error": str(e)}, status=500)

    def delete(self, request, pk):
        try:
            response = Response.objects.get(pk=pk)
            response.delete()
            return APIResponse(status=200)
        except Exception as e:
            return APIResponse({"error": str(e)}, status=500)


class AnswerListCreateView(APIView):
    def get(self, request):
        try:
            queryset = Answer.objects.all()
            serializer = AnswerSerializer(queryset, many=True)
            return APIResponse(serializer.data, status=200)
        except Exception as e:
            return APIResponse({"error": str(e)}, status=500)

    def post(self, request):
        try:
            serializer = AnswerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return APIResponse(serializer.data, status=200)
            return APIResponse(serializer.errors, status=400)
        except Exception as e:
            return APIResponse({"error": str(e)}, status=500)


class AnswerRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk):
        try:
            answer = Answer.objects.get(pk=pk)
            serializer = AnswerSerializer(answer)
            return APIResponse(serializer.data)
        except Exception as e:
            return APIResponse({"error": str(e)}, status=500)

    def put(self, request, pk):
        try:
            answer = Answer.objects.get(pk=pk)
            serializer = AnswerSerializer(answer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return APIResponse(serializer.data)
            return APIResponse(serializer.errors, status=400)
        except Exception as e:
            return APIResponse({"error": str(e)}, status=500)

    def delete(self, request, pk):
        try:
            answer = Answer.objects.get(pk=pk)
            answer.delete()
            return APIResponse(status=200)
        except Exception as e:
            return APIResponse({"error": str(e)}, status=500)


class FormView(APIView):
    def get(self, request, form_id):
        try:
            form = Form.objects.get(pk=form_id)
        except Form.DoesNotExist:
            raise Http404("Form does not exist.")
        return APIResponse({"form": form})


class FormDataView(APIView):
    def get(self, request, form_id):
        try:
            form = Form.objects.get(pk=form_id)
        except Form.DoesNotExist:
            return APIResponse({"error": "Form not found"}, status=404)

        data = {"form_id": form.id, "questions": []}
        questions = form.questions.all()
        for question in questions:
            answers = Answer.objects.filter(question=question)
            answer_texts = [answer.text for answer in answers]
            data["questions"].append({"question": question.text, "answers": answer_texts})
        phn = "+917250536658"
        send_sms(phn, data)
        push_to_google_sheet(data)
        return APIResponse(data)
