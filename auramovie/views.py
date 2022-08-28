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

url = "https://movie-database-alternative.p.rapidapi.com/"
headers = {
	"X-RapidAPI-Key": "f59ae81d3dmshc148ac01d774d09p1c39eajsndb8945646dbc",
	"X-RapidAPI-Host": "movie-database-alternative.p.rapidapi.com"
}

def index(request):
    #template = loader.get_template('index.html')
    #return HttpResponse(template.render())
    return render(request, "index.html")

def practise(request):
    return render(request, "practise.html")

async def get_movie_info(filename_path):
    '''
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
    totalruntime = 0
    with open(filename_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0] == '':
                break
            if row[0] == 'Const':
                continue
            if row[0] == 'tvSeries':
                continue
            querystring = {"r":"json","i":row[0]}
            response = requests.request("GET", url, headers=headers, params=querystring)
            movies_dict['posters'].append(response.json()['Poster'])
            movies_dict['lists'].append(row[3])
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
    #return movies_dict
    '''
    print("Inside get_movie_info")
    await asyncio.sleep(10)
    print("After Sleep")
    return redirect('/practise')
    return HttpResponse("Finished Loading")

async def get_csv_file(request):
    if request.method == 'POST' and request.FILES['csvfile']:
       
        myfile = request.FILES['csvfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        filename_path = fs.path(filename)
        #movies_dict = get_movie_info(filename_path)
        loop = asyncio.get_event_loop()
        loop.create_task(get_movie_info(filename_path))
        '''
        img_path = fs.path("movie_1.jpg")
        print(img_path)
        movies_name_poster = zip(movies_dict['lists'],movies_dict["posters"])
        context = {'movies': movies_dict, 'img_path': img_path, 
        'movies_name_poster':movies_name_poster}
        #return render(request, "list_movies.html", context)
        '''
        return HttpResponse("Waiting")
    return HttpResponse("Waiting")

def wait_page(request):
    return render(request, "wait.html")


  