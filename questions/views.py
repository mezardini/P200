from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import Questions, CustomUser as User
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, send_mass_mail
import random
from mistralai.models.chat_completion import ChatMessage
from mistralai.client import MistralClient
from django.shortcuts import render
import environ
env = environ.Env()
environ.Env.read_env()

# @login_required(login_url='signin')
def generate(request):

    
    return render(request, 'questions.html')


def index(request):

    return render(request, 'home.html')



def questions(request):

    if request.method == 'POST':
        scope_of_study = request.POST['details']
        study_goals = request.POST['study_goals']
        difficulty_level = request.POST['difficulty']

        api_key = env('MistralAPIKEY')
        model = "mistral-tiny"

        client = MistralClient(api_key=api_key)


        mcq_message = [
            ChatMessage(
                role="user",
                content=f"Generate 20 multiple choice questions for this course whose scope of study is {scope_of_study} and the difficulty level of the questions should be {difficulty_level} level, the study goal is {study_goals}, 4 choices for each question. Write the option that is correct."
            )
        ]

        saq_message = [
            ChatMessage(
                role="user",
                content=f"Generate 15 short answer questions for this course whose scope of study is {scope_of_study} and the difficulty level of the questions should be {difficulty_level} level, the study goal is {study_goals}. write the answer and make it short."
            )
        ]

        eq_message = [
            ChatMessage(
                role="user",
                content=f"Generate 15 essay questions for this course whose scope of study is {scope_of_study} and the difficulty level of the questions should be {difficulty_level} level, the study goal is {study_goals}. write the answer and make it short."
            )
        ]

        sections = {
            'm_c_q': mcq_message,
            's_a_q': saq_message,
            'e_q': eq_message,
        }

        result = {}

        for key, message in sections.items():
            chat_response = client.chat(
                model=model,
                messages=message,
            )

            result[key] = chat_response.choices[0].message.content

        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
        else:
            user = User.objects.get(id=1)
        question = Questions.objects.create(

            scope_of_study=scope_of_study,
            study_goals=study_goals,
            difficulty_level=difficulty_level,
            multiple_choice_questions=result.get('m_c_q', ''),
            short_answer_questions=result.get('s_a_q', ''),
            essay_questions=result.get('e_q', ''),
            question_id=random.randint(100000, 999999),
            creator=user,

        )
        question.save()
        send_mail(
            'New Question at Practice50',
            'A question: "'+scope_of_study+'" has been asked on Practice50',
            'settings.EMAIL_HOST_USER',
            ['mezardini@gmail.com'],
            fail_silently=False,
        )
        if request.user.is_authenticated:
            return redirect(answer, question.question_id)
        else:
            context = {'question': question}
            return render(request, 'answers.html', context)
    
    else:

        return redirect(generate)


def answer(request, question_id):

    question = Questions.objects.get(question_id=question_id)

    context = {'question': question}
    return render(request, 'answers.html', context)


def error_404_view(request, exception):

    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')


def signin(request):

    return render(request, 'signin.html')


def signout(request):
    logout(request)
    return redirect('login')


def TandC(request):

    return render(request, 'TandC.html')


def policy(request):

    return render(request, 'policy.html')


class DashboardView(LoginRequiredMixin, View):
    login_url = 'signin'
    template_name = 'dashboard.html'

    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        

        try:
            questions = Questions.objects.filter(creator=user_id)
            user = User.objects.get(id=user_id)
            user_credit = int(user.credit) * 50

        except ObjectDoesNotExist:
            user = None
            questions = []

        context = {
            'questions': questions,
            'user': user,
            'user_credit': user_credit
        }
        return render(request, self.template_name, context)
