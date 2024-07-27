from mistralai.models.chat_completion import ChatMessage
from mistralai.client import MistralClient
from django.shortcuts import render
import environ
env = environ.Env()
environ.Env.read_env()


def generate(request):

    if request.method == 'POST':
        scope_of_study = request.POST['details']
        study_goals = request.POST['study_goals']
        difficulty_level = request.POST['difficulty']

        api_key = env('MistralAPIKEY')
        model = "mistral-tiny"

        client = MistralClient(api_key=api_key)

        CTC = 'CTA-Button-Copy'

        result = {}

        mcq_message = [
            ChatMessage(
                role="user",
                content=f"Generate 60 multiple choice questions for this course whose scope of study is {scope_of_study} and the difficulty level of the questions should be {difficulty_level} level, the study goal is {study_goals}, 4 choices for each question"
            )
        ]

        saq_message = [
            ChatMessage(
                role="user",
                content=f"Generate 60 short answer questions for this course whose scope of study is {scope_of_study} and the difficulty level of the questions should be {difficulty_level} level, the study goal is {study_goals}"
            )
        ]

        eq_message = [
            ChatMessage(
                role="user",
                content=f"Generate 80 essay questions for this course whose scope of study is {scope_of_study} and the difficulty level of the questions should be {difficulty_level} level, the study goal is {study_goals}"
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

        context = result  # directly use the result dictionary as the context

        return render(request, 'questions.html', context)

    return render(request, 'questions.html')


def index(request):

    return render(request, 'home.html')


def questions(request):
        scope_of_study = request.POST['details']
        study_goals = request.POST['study_goals']
        difficulty_level = request.POST['difficulty']

        api_key = env('MistralAPIKEY')
        model = "mistral-tiny"

        client = MistralClient(api_key=api_key)

        CTC = 'CTA-Button-Copy'

        result = {}

        mcq_message = [
            ChatMessage(
                role="user",
                content=f"Generate 3 multiple choice questions for this course whose scope of study is {scope_of_study} and the difficulty level of the questions should be {difficulty_level} level, the study goal is {study_goals}, 4 choices for each question"
            )
        ]

        saq_message = [
            ChatMessage(
                role="user",
                content=f"Generate 3 short answer questions for this course whose scope of study is {scope_of_study} and the difficulty level of the questions should be {difficulty_level} level, the study goal is {study_goals}"
            )
        ]

        eq_message = [
            ChatMessage(
                role="user",
                content=f"Generate 5 essay questions for this course whose scope of study is {scope_of_study} and the difficulty level of the questions should be {difficulty_level} level, the study goal is {study_goals}"
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

        context = result  # directly use the result dictionary as the context

        return render(request, 'questions_partial.html', result)
