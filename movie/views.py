from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
from collections import defaultdict

from .models import Movie

# create your views here

def home(request):
    
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies})


def about(request):
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})


def statistics_view(request):
    # Configuración de matplotlib para renderizado en un archivo
    matplotlib.use('Agg')
    
    # Obtener todas las películas
    all_movies = Movie.objects.all()
    
    # Diccionarios para almacenar las cantidades por año y por género
    movie_counts_by_year = {}
    movie_counts_by_genre = defaultdict(int)
    
    # Contar películas por año y género
    for movie in all_movies:
        # Conteo por año
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1
        
        # Conteo por género
        genre = movie.genre.split(",")[0].strip() if movie.genre else "Unknown"
        movie_counts_by_genre[genre] += 1

    # --------------- Gráfica de películas por año ---------------
    # Ancho de las barras
    bar_width = 0.5
    # Posiciones de las barras
    bar_positions = range(len(movie_counts_by_year))
    # Crear la gráfica de barras para películas por año
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    
    # Guardar la gráfica en un objeto BytesIO
    buffer_year = io.BytesIO()
    plt.savefig(buffer_year, format='png')
    buffer_year.seek(0)
    plt.close()
    
    # Convertir la gráfica a base64
    image_year_png = buffer_year.getvalue()
    buffer_year.close()
    graphic_year = base64.b64encode(image_year_png).decode('utf-8')
    
    # --------------- Gráfica de películas por género ---------------
    # Crear la gráfica de barras para películas por género
    genres = list(movie_counts_by_genre.keys())
    counts = list(movie_counts_by_genre.values())
    
    plt.bar(genres, counts, color='skyblue')
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.3)
    
    # Guardar la gráfica en otro objeto BytesIO
    buffer_genre = io.BytesIO()
    plt.savefig(buffer_genre, format='png')
    buffer_genre.seek(0)
    plt.close()
    
    # Convertir la gráfica a base64
    image_genre_png = buffer_genre.getvalue()
    buffer_genre.close()
    graphic_genre = base64.b64encode(image_genre_png).decode('utf-8')
    
    # Renderizar ambas gráficas en la plantilla statistics.html
    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre
    })
