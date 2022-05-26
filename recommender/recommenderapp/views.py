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

now = datetime.now()
new_dataframe = {}
df = {}
newParam = []
similarity_matrix = [[]]
movies = []
images = []


def get_my_key(obj):
    return float(obj.popularity)


def fetch_image_url(Mid):
    url = f"https://api.themoviedb.org/3/movie/{Mid}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json().get("poster_path")


def trainData(request):
    global new_dataframe
    new_dataframe = pd.read_csv(
        "C:\\Users\\admin\\PycharmProjects\\pythonProject\\RecommenderSystem\\recommender\\movies11 (1).csv")
    global df
    df = new_dataframe
    # print(df)
    df1 = df.sort_values(by=['popularity'])
    # print(df1['popularity'], df1['title'])
    # movies = df1.to_dict()
    # print(movies)
    global movies
    movies = df1['title'].tolist()
    global images
    images = df1['movie_id'].tolist()
    poster_path = []
    for i in range(0, 7):
        poster_path.append(fetch_image_url(images[i]))
        print(fetch_image_url(images[i]))
    global newParam
    for i in range(len(poster_path)):
        temp = {}
        temp["title"] = movies[i]
        temp["image"] = poster_path[i]
        newParam.append(temp)
    cv = CountVectorizer(max_features=6000, stop_words='english')
    vectors = cv.fit_transform(new_dataframe['tags']).toarray()
    global similarity_matrix
    similarity_matrix = cosine_similarity(vectors)
    return HttpResponseRedirect("/home/")


def showPage(request):
    if request.method == "POST":
        return HttpResponseRedirect("/trainModel/")
    return render(request, "recommenderapp/home.html")


def index(request):
    # param = []
    # if request.method == 'POST':
    #     searchmovie = request.POST.get("searchmovie")
    #     print("-----------------------------------------------------HELOO---------------------------")
    #     param = generateRecommendation(request, searchmovie)
    # df = new_dataframe
    # print(df)
    # df1 = df.sort_values(by=['popularity'])
    # print(df1['popularity'], df1['title'])
    # movies = df1.to_dict()
    # print(movies)
    # movies = df1['title'].tolist()
    # images = df1['movie_id'].tolist()
    # poster_path = []
    # for i in range(0, 7):
    #     poster_path.append(fetch_image_url(images[i]))
    #     print(fetch_image_url(images[i]))
    # dict1 = {"movies": movies, "images": images}
    # for i in range(len(df1)):
    # movies.append(new_dataframe["title"])
    # print(df1[i])
    # movies.append(df[i])
    # print(df1[i])
    # temp = {}
    # temp["title"] = new_dataframe["title"]
    # temp["popularity"] = new_dataframe["popularity"]
    # movies.append(temp)
    # popularMovie = Movie.objects.all()
    # for i in range(len(popularMovie)):
    #     movies.append(popularMovie[i])
    # movies.sort(key=get_my_key, reverse=True)
    # n = len(popularMovie)
    # nSlides = n // 4 + ceil((n / 4) - (n // 4))
    # params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'movie': movies},
    # params1 = {"movie": params, "recommended": param}
    # params1 = {"dict1": dict1}
    # params1 = {"movie": movies, 'image': poster_path}
    params1 = {"popular": newParam}
    # params2 = {"movies": params1}
    # print(params1.get("movie")[0]["movie"][1].movie_id)
    return render(request, 'recommenderapp/index.html', params1)


def generateRecommendation(request, movie1):
    # movies_id = []
    # title = []
    # movie_tags = []
    # popularity = []
    # genres = []
    # cast = []
    # image = []

    # new_dataframe = pd.read_csv(
    #     "C:\\Users\\admin\\PycharmProjects\\pythonProject\\RecommenderSystem\\recommender\\movies11 (1).csv")
    # print(new_dataframe)

    # popularMovie = Movie.objects.all()
    # for i in popularMovie:
    #     movies_id.append(i.movie_id)
    #     title.append(i.title)
    #     movie_tags.append(i.movie_tags)
    #     popularity.append(i.popularity)
    #     genres.append(i.genres)
    #     cast.append(i.cast)
    #     image.append(i.image)
    #
    # data = {
    #     'movies_id': movies_id,
    #     'title': title,
    #     'movie_tags': movie_tags,
    #     'popularity': popularity,
    #     'genres': genres,
    #     'cast': cast,
    #     'image': image
    # }
    # new_dataframe = pd.DataFrame(data)

    # print(new_dataframe)

    # cv = CountVectorizer(max_features=6000, stop_words='english')
    # vectors = cv.fit_transform(new_dataframe['tags']).toarray()
    #
    # similarity_matrix = cosine_similarity(vectors)
    # print(similarity_matrix)
    # global new_dataframe
    # new_dataframe = pd.read_csv(
    #     "C:\\Users\\admin\\PycharmProjects\\pythonProject\\RecommenderSystem\\recommender\\movies11 (1).csv")
    global new_dataframe
    movieindex1 = new_dataframe[new_dataframe['title'] == movie1]
    print(movieindex1)
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
    # print("----------------------------minindex-----------------", movieindex)
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
        print("exception signup")


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
        print("exception login")


def dashboard(request):
    # new_dataframe1 = pd.read_csv(
    #     "C:\\Users\\admin\\PycharmProjects\\pythonProject\\RecommenderSystem\\recommender\\movies11 (1).csv")
    # param = []
    newParam = []
    # print('hi..')
    if request.method == 'POST':
        # new_dataframe = pd.read_csv(
        #     "C:\\Users\\admin\\PycharmProjects\\pythonProject\\RecommenderSystem\\recommender\\movies11 (1).csv")
        # print('hello')
        searchmovie = request.POST.get("searchmovie")
        # print("-----------------------------------------------------HELOO---------------------------")
        hist = History(name=searchmovie, user=request.user)
        hist.save()
        # print('welcome')
        param = generateRecommendation(request, searchmovie)
        # image = []
        for x in param:
            temp = {}
            temp["id"] = x.get("id")
            temp["image"] = fetch_image_url(x.get("id"))
            temp["title"] = x.get("title")
            newParam.append(temp)
            # fetch_image_url(x.get("id"))
    movies = []
    # new_dataframe1 = pd.read_csv(
    #     "C:\\Users\\admin\\PycharmProjects\\pythonProject\\RecommenderSystem\\recommender\\movies11 (1).csv")
    global new_dataframe
    for i in range(len(new_dataframe)):
        # movies.append(new_dataframe["title"])
        movies.append(new_dataframe["title"][i])
        # print(i)
    # movies.sort(key=get_my_key, reverse=True)
    # n = len(popularMovie)
    # nSlides = n // 4 + ceil((n / 4) - (n // 4))
    # params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'movie': movies},
    params1 = {"movie": movies, "recommended": newParam}
    # print(params1.get("movie")[0]["movie"][1].movie_id)
    return render(request, 'recommenderapp/dashboard.html', params1)


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/home/')


def profile(request):
    if request.user.is_authenticated:
        user = request.user.id
    return render(request, 'recommenderapp/profile.html')


def history(request):
    history1 = History.objects.all()
    history2 = []
    for i in history1:
        if i.user == request.user:
            history2.append(i)
    # idx = pd.Index(history2)
    # print(idx.value_counts())
    param = {"history": history2}
    return render(request, 'recommenderapp/history.html', param)


# def filterMovieByGenre(request):
#     genreMovie = []
#     if request.method == "POST":
#         genre = request.POST.get("genre")
#         print(genre)
#         i = 0
#         global new_dataframe
#         for j in range(len(movies)):
#             if i == 6:
#                 break
#             # print(new_dataframe["title"][j])
#             print(movies[j]," ",new_dataframe["title"])
#             if genre in new_dataframe["genres"]:
#                 print(genre)
#                 print(new_dataframe["genres"])
#                 print("hello")
#                 temp = {}
#                 temp["image"] = fetch_image_url(new_dataframe["movie_id"][j])
#                 temp["title"] = movies[j]
#                 temp["genres"] = genre
#                 genreMovie.append(temp)
#                 i = i + 1
#     print(genreMovie)
#     param2 = {"filteredMovie": genreMovie}
#     return render(request, "recommenderapp/Movies.html", param2)
