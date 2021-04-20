import os
import discord
import requests
import json
from tmdbv3api import TMDb
from tmdbv3api import Movie
from tmdbv3api import TV
import neverSleep
neverSleep.awake("https://remibot.qfu10.repl.co", False)

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def ani(q, author):
    query = '''
    query ($search: String) { # Define which variables will be used in the query (id)
    Media (search: $search, type: ANIME) { # Insert our variables into the query arguments (search)
        title {
        romaji
        }
        type
        format
        episodes
        status
        genres
        description
        coverImage{
            medium
        }
        siteUrl
    }
    }
    '''
    # Define our query variables and values that will be used in the query request
    variables = {
        'search': q
    }
    url = 'https://graphql.anilist.co'
    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = json.loads(response.text)
    if data["data"]["Media"] == None:
        error = discord.Embed(
            title="Anime not found"
        )
        error.set_image(url = "https://media1.tenor.com/images/0c143322f7e7d772353a965720338aa4/tenor.gif?itemid=19978494")
        return error
    title = data["data"]["Media"]["title"]["romaji"]
    para = remove_html_tags(data["data"]["Media"]["description"])
    type_ = data["data"]["Media"]["type"]
    format_ = data["data"]["Media"]["format"]
    episodes = str(data["data"]["Media"]["episodes"])
    status = data["data"]["Media"]["status"]
    genres=""
    for element in data["data"]["Media"]["genres"]:
        genres +=element + ' '
    cover_image= data["data"]["Media"]["coverImage"]["medium"]
    url = data["data"]["Media"]["siteUrl"]


    content = "\n" + para + "\n\n"
    stats = "Type: " + type_ + "\nFormat: " + format_ + "\nEpisodes: " + episodes + "\nStatus: " + status + "\nGenres: " + genres
            
    embed = discord.Embed(
        title=title,
        url=url,
        description = content,
        color = discord.Colour.red()
    )
    embed.add_field(name="Information", value = stats, inline = False)
    embed.set_thumbnail(url=cover_image)
    embed.set_footer(icon_url=author.avatar_url, text=f"Requested by {author.name}")
    return embed    

def manga(q, author):
    query = '''
    query ($search: String) { # Define which variables will be used in the query (id)
    Media (search: $search, type: MANGA) { # Insert our variables into the query arguments (search)
        title {
        romaji
        }
        type
        format
        chapters
        volumes
        status
        genres
        description
        coverImage{
            medium
        }
        siteUrl
    }
    }
    '''
    # Define our query variables and values that will be used in the query request
    variables = {
        'search': q
    }
    url = 'https://graphql.anilist.co'
    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = json.loads(response.text)
    if data["data"]["Media"] == None:
        error = discord.Embed(
            title="Manga not found"
        )
        error.set_image(url = "https://media1.tenor.com/images/0c143322f7e7d772353a965720338aa4/tenor.gif?itemid=19978494")
        return error
    title = data["data"]["Media"]["title"]["romaji"]
    para = remove_html_tags(data["data"]["Media"]["description"])
    type_ = data["data"]["Media"]["type"]
    format_ = data["data"]["Media"]["format"]
    chapters = str(data["data"]["Media"]["chapters"])
    volumes = str(data["data"]["Media"]["volumes"])
    status = data["data"]["Media"]["status"]
    genres=""
    for element in data["data"]["Media"]["genres"]:
        genres +=element + ' '
    cover_image= data["data"]["Media"]["coverImage"]["medium"]
    url = data["data"]["Media"]["siteUrl"]


    content = "\n" + para + "\n\n"
    stats = "Type: " + type_ + "\nFormat: " + format_ + "\nChapters: " + chapters + "\nVolumes: " + volumes + "\nStatus: " + status + "\nGenres: " + genres
            
    embed = discord.Embed(
        title=title,
        url=url,
        description = content,
        color = discord.Colour.blue()
    )
    embed.add_field(name="Information", value = stats, inline = False)
    embed.set_thumbnail(url=cover_image)
    embed.set_footer(icon_url=author.avatar_url, text=f"Requested by {author.name}")
    return embed

def mov(q, author):
    tmdb = TMDb()
    key= os.environ['api_key']
    tmdb.api_key = key
    tmdb.language="en"
    movie = Movie()
    search = movie.search(q)
    if len(search) == 0:
        error = discord.Embed(
            title="Movie not found"
        )
        error.set_image(url = "https://media1.tenor.com/images/0c143322f7e7d772353a965720338aa4/tenor.gif?itemid=19978494")
        return error
    id_ = search[0].id
    url = "https://api.themoviedb.org/3/movie/" + str(id_) + "?api_key=" + key +"&language=en-US"
    response = requests.get(url)
    data = response.json()
    title = data["title"]
    para = data["overview"]
    status = data["status"]
    rating = data["vote_average"]
    date = data["release_date"]
    genres=""
    for element in data["genres"]:
        genres +=element["name"] + ' '
    cover_image = "https://www.themoviedb.org/t/p/w1280" +  data["poster_path"]
    url = "https://www.themoviedb.org/movie/" + str(id_)
    content = "\n" + para + "\n\n"
    stats = "Status: " + status + "\nRating: " + str(rating) + "\nRelease Date: " + str(date) + "\nGenres: " + genres
    embed = discord.Embed(
        title=title,
        url=url,
        description = content,
        color = discord.Colour.green()
    )
    embed.add_field(name="Information", value = stats, inline = False)
    embed.set_thumbnail(url=cover_image)
    embed.set_footer(icon_url=author.avatar_url, text=f"Requested by {author.name}")
    return embed


def tv(q, author):
    tmdb = TMDb()
    key= os.environ['api_key']
    tmdb.api_key = key
    tmdb.language="en"
    tv = TV()
    search = tv.search(q)
    if len(search) == 0:
        error = discord.Embed(
            title="TV Show not found"
        )
        error.set_image(url = "https://media1.tenor.com/images/0c143322f7e7d772353a965720338aa4/tenor.gif?itemid=19978494")
        return error
    
    id_ = search[0].id
    url = "https://api.themoviedb.org/3/tv/" + str(id_) + "?api_key=" + key +"&language=en-US"
    response = requests.get(url)
    data = response.json()
    title = data["name"]
    para = data["overview"]
    status = data["status"]
    rating = data["vote_average"]
    episodes = data["number_of_episodes"]
    seasons =  data["number_of_seasons"]
    genres=""
    for element in data["genres"]:
        genres +=element["name"] + ' '
    cover_image = "https://www.themoviedb.org/t/p/w1280" +  data["poster_path"]
    url = "https://www.themoviedb.org/tv/" + str(id_)
    content = "\n" + para + "\n\n"
    stats = "Status: " + status + "\nRating: " + str(rating) + "\nSeasons: " + str(seasons) + "\nEpisdoes: " + str(episodes) +  "\nGenres: " + genres
    embed = discord.Embed(
        title=title,
        url=url,
        description = content,
        color = discord.Colour.gold()
    )
    embed.add_field(name="Information", value = stats, inline = False)
    embed.set_thumbnail(url=cover_image)
    embed.set_footer(icon_url=author.avatar_url, text=f"Requested by {author.name}")
    return embed

def book(q, auth):
  response = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + q)
  data = json.loads(response.text)
  if data["totalItems"] == 0:
        error = discord.Embed(
            title="Book not found"
        )
        error.set_image(url = "https://media1.tenor.com/images/0c143322f7e7d772353a965720338aa4/tenor.gif?itemid=19978494")
        return error
  title = data["items"][0]["volumeInfo"]["title"]
  para = data["items"][0]["volumeInfo"]["description"]
  if len(para) > 750:
      para = para[:750] + "..."
  date_ = data["items"][0]["volumeInfo"]["publishedDate"]
  authorlst = data["items"][0]["volumeInfo"]["authors"]
  author=""
  for element in authorlst:
      author +=element + ", "
  id_ = data["items"][0]["id"]
  cover_image = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
  url = "http://books.google.com/books?id=" + id_
  categorylst = data["items"][0]["volumeInfo"]["categories"]
  categories=""
  for element in categorylst:
      categories += element + " " 
  content = "\n" + para + "\n\n"
  stats = "Author: " + author + "\nPublishing Date: " + date_ + "\nCategories: " + categories
  embed = discord.Embed(
    title=title,
    url = url,
    description = content
  )
  embed.add_field(name="Information", value = stats, inline = False)
  embed.set_thumbnail(url=cover_image)
  embed.set_footer(icon_url=auth.avatar_url, text=f"Requested by {auth.name}")
  return embed    

def hel(author):
    embed = discord.Embed(
        title="Help Page",
        description = "List of available commands"
    )
    embed.add_field(name="Anime", value="r!anime <query>", inline=False)
    embed.add_field(name="Manga", value="r!manga <query>", inline=False)
    embed.add_field(name="TV Show", value="r!tv <query>", inline=False)
    embed.add_field(name="Movie", value="r!movie <query>", inline=False)
    embed.add_field(name="Book", value="r!book <query>", inline=False)
    embed.set_footer(icon_url=author.avatar_url, text=f"Requested by {author.name}")
    return embed
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content    
    
    if msg.startswith('r!help'):
        await message.channel.send(embed = hel(message.author))
    lst = msg.split()
    if len(lst) == 0:
      return
    prefix=lst.pop(0)
    q = ' '.join(lst)        
    
    if prefix == "r!anime":
        await message.channel.send(embed = ani(q, message.author))
    elif prefix == "r!manga":
        await message.channel.send(embed = manga(q, message.author))
    elif prefix == "r!movie":
        await message.channel.send(embed = mov(q, message.author))
    elif prefix == "r!tv":
        await message.channel.send(embed = tv(q, message.author))
    elif prefix == "r!book" or prefix == "r!books":
        await message.channel.send(embed = book(q, message.author))
    

client.run(os.environ['TOKEN'])
