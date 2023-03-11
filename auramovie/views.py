from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
import csv
import requests
import json
import time
import asyncio
from django.shortcuts import redirect
import threading

url = "https://movie-database-alternative.p.rapidapi.com/"
headers = {
	"X-RapidAPI-Key": "f59ae81d3dmshc148ac01d774d09p1c39eajsndb8945646dbc",
	"X-RapidAPI-Host": "movie-database-alternative.p.rapidapi.com"
}

filename = ''

def index(request):
    return render(request, "index.html")

def practise(request):
    return render(request, "practise.html")

def get_movie_info(filename_path):
    movies_dict = {}
    movies_dict['totalruntime'] = 0
    movies_dict['totalmovies'] = 0
    movies_dict['posters'] = []
    movies_dict['lists'] = []
    movies_dict['totalruntime_days'] = 0
    movies_dict['nineandabove'] = 0
    movies_dict['eightandabove'] = 0
    movies_dict['sevenandabove'] = 0
    movie_poster = {}
    response_thread = []
    request_thread = []
    totalruntime = 0
    best_five_rated = []
    movie_rating = {}
    unsorted_movie_list = []
    movie_count = 0
    with open(filename_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row == []:
                return 0
            if row[0] == '':
                break
            if row[0] == 'Const':
                continue
            if 'tv' in row[5] or 'video' in row[5]:
                continue
            
            print("Row 7 :"+ row[7])
            totalruntime = totalruntime + int(row[7])
            if float(row[6]) > 9:
                movies_dict['nineandabove'] += 1
            if float(row[6]) >= 8 and float(row[6]) < 9:
                movies_dict['eightandabove'] += 1
            if float(row[6]) >= 7 and float(row[6]) < 8:
                movies_dict['sevenandabove'] += 1

            movie_count += 1
            unsorted_movie_list.append(row)

        movies_dict['totalruntime_hours'] = int(totalruntime/60)
        movies_dict['totalruntime_days'] = int(movies_dict['totalruntime_hours']/24)
        movies_dict['totalmovies'] = movie_count

        sorted_movie_list = sorted(unsorted_movie_list, reverse=True,
                            key=lambda unsorted_movie_list:unsorted_movie_list[6])

        def get_from_movie_api(movie_list):
            querystring = {"r":"json","i":movie_list[0]}
            # Get the info from Rapid API
            response = requests.request("GET", url, headers=headers, params=querystring)
            response_thread.append((movie_list,response))
            movies_dict['lists'].append(movie_list[3])

        for best_movie in sorted_movie_list[:5]:
            # Start a thread for each request to Movie DB
            each_request = threading.Thread(target=get_from_movie_api, args=(best_movie,))
            each_request.setDaemon(True)
            request_thread.append(each_request)
            each_request.start()
            # Rapid API Server does not handle the API request fast due to DDOS safetly.
            # Thats the reason this delay.
            time.sleep(0.2)
        
        # Wait for each request to join.
        for each_request in request_thread:
            each_request.join()
        
        for row, response in response_thread:
            movies_dict['posters'].append(response.json()['Poster'])
            #movies_dict['lists'].append(row[3])
            if row[0] == '':
                break
            '''
            totalruntime = totalruntime + int(row[7])
            if float(row[6]) > 9:
                movies_dict['nineandabove'] += 1
            if float(row[6]) >= 8 and float(row[6]) < 9:
                movies_dict['eightandabove'] += 1
            if float(row[6]) >= 7 and float(row[6]) < 8:
                movies_dict['eightandabove'] += 1
            
    movies_dict['totalruntime_hours'] = int(totalruntime/60)
    movies_dict['totalruntime_days'] = int(movies_dict['totalruntime_hours']/24)
    movies_dict['totalmovies'] = len(movies_dict['lists'])
    '''
    return movies_dict

def get_csv_file(request):
    filename_path = request.session.get('0')
    error_context = None
    try:
        movies_dict = get_movie_info(filename_path)
    except UnicodeDecodeError:
        error_context = {'error_type': 1}
        return render(request, "error.html", error_context)
    if movies_dict == 0:
        error_context = {'error_type': 2}
        return render(request, "error.html", error_context)
    movies_name_poster = zip(movies_dict['lists'],movies_dict["posters"])
    context = {'movies': movies_dict, 'movies_name_poster':movies_name_poster}
    return render(request, "list_movies.html", context)

def wait_page(request):
    if request.method == 'POST' and request.FILES['csvfile']:
        myfile = request.FILES['csvfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        filename_path = fs.path(filename)
        request.session['0'] = filename_path
    return render(request, "wait.html")

def handler404(request, exception):
    error_context = {'error_type': 3}
    return render(request, "404.html", error_context)
    
def handler500(request):
    error_context = {'error_type': 3}
    return render(request, "404.html", error_context)

# Things to do.
# Improve the Stats table look. 
# Add the Heads so that google can catch it. 
# Upload in google cloud. 
# Netflix support. 
# Check on how to add ad sense to this site. 
 