from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from backend import settings
from .forms import RecommendationForm, SignUpForm
from .models import UserInformation
from openai import OpenAI
from pinecone import Pinecone
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from .update_arxiv_papers import embed_and_upload_to_pinecone
import os

def home(request):
    if request.user.is_authenticated:
        return redirect('recommendation')
    else:
        return render(request, 'home.html')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('recommendation')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('recommendation')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out!")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            user_info = UserInformation.objects.create(
                user=new_user,
                first_name=user_form.cleaned_data['first_name'],
                last_name=user_form.cleaned_data['last_name'],
                email=user_form.cleaned_data['email'],
                phone=user_form.cleaned_data['phone_number'],
                address=user_form.cleaned_data['address'],
                city=user_form.cleaned_data['city'],
                state=user_form.cleaned_data['state'],
                zipcode=user_form.cleaned_data['zipcode'],
            )
            login(request, new_user)
            return redirect('recommendation')
        else:
            messages.error(request, user_form.errors)
    else:
        user_form = SignUpForm()
    return render(request, 'register.html', {'form': user_form})

@login_required
def recommendation_results(request):
    recommendation = request.session.get('recommendation', None)
    if recommendation:
        return render(request, 'recommendation_results.html', {'recommendation': recommendation})
    else:
        return redirect('recommendation')

@login_required
def recommendation_view(request):
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            patient_data = {
                'age': form.cleaned_data.get('age'),
                'symptoms': form.cleaned_data.get('symptoms'),
                'medical_conditions': form.cleaned_data.get('medical_conditions'),
                'exercise': form.cleaned_data.get('exercise', 'Not specified')
            }

            prompt_template = """
            Based on the patient details: Age - {age}, Symptoms - {symptoms}, Medical Conditions - {medical_conditions}, 
            and the following research context: {context}.

            Please suggest appropriate medical treatments. Include the titles and direct quotes from the research papers you referenced, if necessary.
            """

            os.environ["PINECONE_API_KEY"] = settings.PINECONE_API_KEY
            pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
            index = PineconeVectorStore.from_existing_index(index_name="pocketdoc", embedding=embeddings)

            query_text = f"Age: {patient_data['age']}, Symptoms: {patient_data['symptoms']}, Medical conditions: {patient_data['medical_conditions']}"
            retriever = index.as_retriever()
            result = retriever.get_relevant_documents(query_text)

            context_text = "\n".join([f"Title: {res.metadata['title']}\nQuote: {res.page_content}" for res in result])
            prompt = prompt_template.format(age=patient_data['age'], symptoms=patient_data['symptoms'],
                                            medical_conditions=patient_data['medical_conditions'],
                                            context=context_text)

            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a providing valuable medical advice to patients."},
                    {"role": "user", "content": prompt}
                ]
            )
            recommendation = response.choices[0].message.content.strip()
            references = "\n".join([f"{i+1}. {res.metadata.get('title', 'No title')}\n   Quote: {res.page_content}" for i, res in enumerate(result)])

            formatted_recommendation = f"{recommendation}\n\nReferences:\n{references}"
            request.session['recommendation'] = formatted_recommendation
            return redirect('recommendation_results')


    else:
        form = RecommendationForm()

    return render(request, 'recommendation.html', {'form': form})

def generate_embeddings(text):
    openai.api_key = settings.OPENAI_API_KEY

    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=[text]
    )
    embeddings = response['data'][0]['embedding']
    return embeddings

def query_pinecone(query_text):
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    pinecone = embed_and_upload_to_pinecone(query_text, settings.OPENAI_API_KEY, settings.PINECONE_API_KEY, "pocketdoc")
    index = pinecone.Index('pocketdoc')

    query_embedding = generate_embeddings(query_text)
    result = index.query([query_embedding], top_k=5)

    return result['matches']
