from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conference, Question
from .forms import ConferenceForm, QuestionForm
from .serializers import QuestionSerializer
from rest_framework import viewsets
import openai
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import io
from django.core.files.base import ContentFile
import qrcode
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

openai.api_key = "sk-proj-BjEbHTYWuLknMiDri8f0T3BlbkFJafchElmdvNC5FpHttsga"

def home(request):
    return render(request, 'core/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


@login_required
def create_conference(request):
    if request.method == "POST":
        form = ConferenceForm(request.POST)
        if form.is_valid():
            conference = form.save(commit=False)
            conference.presenter = request.user
            conference.save()
            # Utiliser l'adresse IP locale ici
            ip_address = "192.168.1.10"  # Remplacez par l'adresse IP de votre machine
            conference.link = f"http://{ip_address}:8000/conference/{conference.id}/"
            conference.save()
            conference.generate_qr_code()
            return render(request, 'core/conference_created.html', {'conference': conference})
        else:
            print("Form is not valid:", form.errors)
    else:
        form = ConferenceForm()

    return render(request, 'core/create_conference.html', {'form': form})





def submit_question(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.conference = conference
            question.save()
            classify_question(question)
            return redirect('thank_you')
    else:
        form = QuestionForm()

    return render(request, 'core/submit_question.html', {'form': form, 'conference': conference})

def classify_question(question):
    prompt = f"Classify the following question into a category: \"{question.text}\".\n\nPossible categories can include any relevant topic discussed in the conference. If the question does not fit into any known category, label it as 'Other'."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )

    category = response.choices[0].text.strip()
    question.category = category
    question.save()

@login_required
def conference_dashboard(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    questions = conference.questions.all().order_by('category', 'created_at')
    
    categorized_questions = {}
    for question in questions:
        if question.category not in categorized_questions:
            categorized_questions[question.category] = []
        categorized_questions[question.category].append(question)
    
    sorted_categories = sorted(categorized_questions.items(), key=lambda item: len(item[1]), reverse=True)
    
    return render(request, 'core/conference_dashboard.html', {'conference': conference, 'categorized_questions': sorted_categories})

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        conference = get_object_or_404(Conference, id=self.request.data.get('conference_id'))
        question = serializer.save(conference=conference)
        classify_question(question)
