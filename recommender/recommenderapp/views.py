import requests

import pandas as pd
from django.http import HttpResponseRedirect, HttpResponse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.shortcuts import render

from datetime import datetime
from .forms import SignUpForm, LoginForm
from .models import History

# GLOBAL VARIABLES
now = datetime.now()
new_dataframe = {}
df = {}
newParam = []
similarity_matrix = [[]]
movies = []
images = []


# Function for fetching image from tmdb website through api


def fetch_image_url(Mid):
    print("hello5")
    url = f"https://api.themoviedb.org/3/movie/{Mid}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    payload = {}
    headers = {}
    print("hello7")
    response = requests.request("GET", url, headers=headers, data=payload)
    print("hello6")
    return response.json().get("poster_path")


# training Data before using it


def trainData(request):
    print("hello")
    global new_dataframe
    new_dataframe = pd.read_csv(
        "C:\\Users\\admin\\PycharmProjects\\pythonProject\\RecommenderSystem\\recommender\\movies11 (1).csv")
    print("hello1")
    # retrieving popular movies
    global df
    df = new_dataframe
    print("hello2")
    df1 = df.sort_values(by=['popularity'])
    # sorting based on popularity
    global movies
    print("hello3")
    movies = df1['title'].tolist()
    global images
    images = df1['movie_id'].tolist()
    # collecting posters of movies
    print("Hello4")
    poster_path = []
    for i in range(0, 6):
        poster_path.append(fetch_image_url(images[i]))
        print("image")
        # print(fetch_image_url(images[i]))

    global newParam
    for i in range(len(poster_path)):
        temp = {}
        temp["title"] = movies[i]
        temp["image"] = poster_path[i]
        newParam.append(temp)

    # part of finding Cosine Similarity matrix
    cv = CountVectorizer(max_features=6000, stop_words='english')
    vectors = cv.fit_transform(new_dataframe['tags']).toarray()
    global similarity_matrix
    similarity_matrix = cosine_similarity(vectors)
    return HttpResponseRedirect("/home/")


# def showPage(request):
#     if request.method == "POST":
#         return HttpResponseRedirect("/trainModel/")
#     return render(request, "recommenderapp/home.html")


# home page

def index(request):
    params1 = {"popular": newParam}
    return render(request, 'recommenderapp/index.html', params1)


def generateRecommendation(request, movie1):
    global new_dataframe
    movieindex1 = new_dataframe[new_dataframe['title'] == movie1]

    # appending movies which are more related to searched movie
    movie_list1 = []
    if movieindex1.empty:
        print("not found")
    else:
        movieindex = new_dataframe[new_dataframe['title'] == movie1].index[0]
        print(movieindex)
        distances = similarity_matrix[movieindex]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:6]
        for i in movie_list:
            movie_list1.append({"title": new_dataframe.iloc[i[0]].title, "id": new_dataframe.iloc[i[0]].movie_id})
    return movie_list1


def signup(request):
    try:
        if not request.user.is_authenticated:
            if request.method == 'POST':
                fm = SignUpForm(request.POST)
                if fm.is_valid():
                    user = fm.save()
                    messages.success(request, 'Account Created Successfully')
                    return HttpResponseRedirect('/login/')
            else:
                if not request.user.is_authenticated:
                    fm = SignUpForm()
            return render(request, 'recommenderapp/signup.html', {'form': fm})
        else:
            return HttpResponseRedirect('/login/')
    except Exception:
        print("exception in signup")


def user_login(request):
    try:
        if not request.user.is_authenticated:
            if request.method == 'POST':
                fm = LoginForm(request=request, data=request.POST)
                if fm.is_valid():
                    uname = fm.cleaned_data['username']
                    upass = fm.cleaned_data['password']
                    user = authenticate(username=uname, password=upass)
                    if user is not None:
                        login(request, user)
                        messages.success(request, 'Logged in Successfully!!')
                        return HttpResponseRedirect('/dashboard/')
            else:
                fm = LoginForm()
            return render(request, 'recommenderapp/login.html', {'form': fm})
        else:
            return HttpResponseRedirect('/dashboard/')
    except Exception:
        print("exception in login")


def dashboard(request):
    newParam = []
    if request.method == 'POST':
        searchmovie = request.POST.get("searchmovie")
        # searched item will be stored in history
        hist = History(name=searchmovie, user=request.user)
        hist.save()
        param = generateRecommendation(request, searchmovie)
        # by calling generateRecommendation it will return list of movies
        for x in param:
            temp = {}
            temp["id"] = x.get("id")
            temp["image"] = fetch_image_url(x.get("id"))
            temp["title"] = x.get("title")
            newParam.append(temp)
    movies = []
    global new_dataframe
    for i in range(len(new_dataframe)):
        movies.append(new_dataframe["title"][i])
    params1 = {"movie": movies, "recommended": newParam}

    return render(request, 'recommenderapp/dashboard.html', params1)


# logout function for userLogout
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/home/')


def profile(request):
    if request.user.is_authenticated:
        user = request.user.id
    return render(request, 'recommenderapp/profile.html')


# retreiving history from history table of database
def history(request):
    history1 = History.objects.all()
    history2 = []
    for i in history1:
        # finding history of particular user
        if i.user == request.user:
            history2.append(i)
    param = {"history": history2}
    return render(request, 'recommenderapp/history.html', param)
