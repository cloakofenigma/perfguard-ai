"""
Movie Database for Sample Application
Contains detailed information about 15 movies
"""

MOVIES = [
    {
        "id": 1,
        "title": "Drishyam",
        "year": 2013,
        "language": "Malayalam",
        "rating": 8.6,
        "runtime": "160 min",
        "thumbnail": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9e/DrishyamMovie.jpg/250px-DrishyamMovie.jpg",
        "poster": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9e/DrishyamMovie.jpg/250px-DrishyamMovie.jpg",
        "genre": ["Crime", "Drama", "Thriller"],
        "director": "Jeethu Joseph",
        "cast": ["Mohanlal", "Meena", "Ansiba Hassan", "Esther Anil", "Asha Sarath"],
        "plot": "A man goes to extreme lengths to save his family from punishment after the family commits an accidental crime. With a mix of suspense and family drama, the film explores how far a parent will go to protect their loved ones.",
        "crew": {
            "director": "Jeethu Joseph",
            "writer": "Jeethu Joseph",
            "producer": "Antony Perumbavoor",
            "music": "Vinu Thomas, Anil Johnson",
            "cinematography": "Sujith Vaassudev"
        },
        "box_office": "$5.5 million"
    },
    {
        "id": 2,
        "title": "Punjabi House",
        "year": 1998,
        "language": "Malayalam",
        "rating": 8.1,
        "runtime": "146 min",
        "thumbnail": "https://m.media-amazon.com/images/M/MV5BNDFhMmVlZGEtMmI5Ni00ZGQ5LThmNmQtOTJjZTQxNDg5MDMyXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
        "poster": "https://img-mm.manoramaonline.com/content/dam/mm/mo/movies/movie-news/images/2023/9/25/punjabi-house.jpg",
        "genre": ["Comedy", "Drama"],
        "director": "Rafi Mecartin",
        "cast": ["Dileep", "Mohini", "Lal", "Cochin Haneefa", "Harisree Ashokan"],
        "plot": "A young man pretending to be a Punjabi to get a visa finds himself in a series of hilarious situations while living with a Punjabi family. A classic comedy that explores cultural differences with warmth and humor.",
        "crew": {
            "director": "Rafi Mecartin",
            "writer": "Rafi Mecartin",
            "producer": "Menaka Suresh",
            "music": "S. P. Venkatesh",
            "cinematography": "Anandakuttan"
        },
        "box_office": "$2.1 million"
    },
    {
        "id": 3,
        "title": "Manichithrathazhu",
        "year": 1993,
        "language": "Malayalam",
        "rating": 8.7,
        "runtime": "169 min",
        "thumbnail": "https://upload.wikimedia.org/wikipedia/en/4/43/Manichitrathazhu.jpg",
        "poster": "https://i.ytimg.com/vi/40DnL80mUU0/maxresdefault.jpg",
        "genre": ["Horror", "Psychological", "Thriller"],
        "director": "Fazil",
        "cast": ["Mohanlal", "Suresh Gopi", "Shobana", "Nedumudi Venu", "Innocent"],
        "plot": "A young woman's arrival at her husband's ancestral home triggers mysterious events. A psychiatrist friend must unravel the truth behind the haunting. A masterpiece that blends psychology with supernatural elements.",
        "crew": {
            "director": "Fazil",
            "writer": "Madhu Muttam",
            "producer": "Swargachitra Appachan",
            "music": "M. G. Radhakrishnan",
            "cinematography": "Anandakuttan"
        },
        "box_office": "$3.2 million"
    },
    {
        "id": 4,
        "title": "Sandesham",
        "year": 1991,
        "language": "Malayalam",
        "rating": 8.4,
        "runtime": "140 min",
        "thumbnail": "https://upload.wikimedia.org/wikipedia/en/b/be/Sandhesam_film_poster.jpg",
        "poster": "https://i.ytimg.com/vi/eOXKtsgttTA/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBPmQc1WXS6_pXZJ4zrGpVncqgF5g",
        "genre": ["Comedy", "Political", "Satire"],
        "director": "Sathyan Anthikad",
        "cast": ["Sreenivasan", "Jayaram", "Thilakan", "Kaviyoor Ponnamma", "Maathu"],
        "plot": "Two brothers with opposing political ideologies clash in their household, creating chaos in the family. A brilliant political satire that humorously explores Kerala's political landscape through family dynamics.",
        "crew": {
            "director": "Sathyan Anthikad",
            "writer": "Sreenivasan",
            "producer": "Joy Thomas",
            "music": "Johnson",
            "cinematography": "Vipin Mohan"
        },
        "box_office": "$1.8 million"
    },
    {
        "id": 5,
        "title": "Spadikam",
        "year": 1995,
        "language": "Malayalam",
        "rating": 8.5,
        "runtime": "155 min",
        "thumbnail": "https://m.media-amazon.com/images/M/MV5BNmFiZWM0YjUtZjAzNS00NDJmLThkNjUtZjRiNDM4ZTMxYzY3XkEyXkFqcGc@._V1_.jpg",
        "poster": "https://img.nowrunning.com/content/movie/2015/Spadikam/bg_spadikam.jpg",
        "genre": ["Action", "Drama"],
        "director": "Bhadran",
        "cast": ["Mohanlal", "Thilakan", "Urvashi", "Spadikam George", "KPAC Lalitha"],
        "plot": "A young man's quest for his father's lost sword becomes a journey of self-discovery and redemption. The film explores father-son relationships with intense action and emotional depth.",
        "crew": {
            "director": "Bhadran",
            "writer": "Bhadran",
            "producer": "R. Mohan",
            "music": "A. R. Rahman",
            "cinematography": "Vipin Mohan"
        },
        "box_office": "$4.2 million"
    },
    {
        "id": 6,
        "title": "Anniyan",
        "year": 2005,
        "language": "Tamil",
        "rating": 8.3,
        "runtime": "181 min",
        "thumbnail": "https://static.toiimg.com/photo/msid-61318981/61318981.jpg",
        "poster": "https://mir-s3-cdn-cf.behance.net/project_modules/hd_webp/9a9cee214878939.67605fe3f08be.png",
        "genre": ["Action", "Psychological", "Thriller"],
        "director": "S. Shankar",
        "cast": ["Vikram", "Sadha", "Prakash Raj", "Vivek", "Nedumudi Venu"],
        "plot": "A law-abiding lawyer with dissociative identity disorder becomes a vigilante who punishes those who break the law. A gripping psychological thriller with social commentary and spectacular action sequences.",
        "crew": {
            "director": "S. Shankar",
            "writer": "Sujatha Rangarajan, S. Shankar",
            "producer": "V. Ravichandran",
            "music": "Harris Jayaraj",
            "cinematography": "Ravi Varman"
        },
        "box_office": "$15 million"
    },
    {
        "id": 7,
        "title": "Maharaja",
        "year": 2024,
        "language": "Tamil",
        "rating": 8.7,
        "runtime": "141 min",
        "thumbnail": "https://upload.wikimedia.org/wikipedia/en/thumb/8/82/Maharaja_2024_film_poster.jpg/250px-Maharaja_2024_film_poster.jpg",
        "poster": "https://images.fandango.com/ImageRenderer/500/0/redesign/static/img/default_poster--dark-mode.png/0/images/masterrepository/Fandango/236587/maharaja-250x376.jpg",
        "genre": ["Action", "Thriller", "Drama"],
        "director": "Nithilan Swaminathan",
        "cast": ["Vijay Sethupathi", "Anurag Kashyap", "Mamta Mohandas", "Natarajan Subramaniam", "Abhirami"],
        "plot": "A barber's search for his stolen dustbin unfolds into a riveting tale of revenge and redemption. The non-linear narrative keeps audiences guessing until the powerful climax.",
        "crew": {
            "director": "Nithilan Swaminathan",
            "writer": "Nithilan Swaminathan",
            "producer": "Sudhan Sundaram, Jagadish Palanisamy",
            "music": "B. Ajaneesh Loknath",
            "cinematography": "Dinesh Purushothaman"
        },
        "box_office": "$35 million"
    },
    {
        "id": 8,
        "title": "3 Idiots",
        "year": 2009,
        "language": "Hindi",
        "rating": 8.4,
        "runtime": "170 min",
        "thumbnail": "https://upload.wikimedia.org/wikipedia/en/d/df/3_idiots_poster.jpg",
        "poster": "https://upload.wikimedia.org/wikipedia/en/d/df/3_idiots_poster.jpg",
        "genre": ["Comedy", "Drama"],
        "director": "Rajkumar Hirani",
        "cast": ["Aamir Khan", "R. Madhavan", "Sharman Joshi", "Kareena Kapoor", "Boman Irani"],
        "plot": "Two friends search for their long-lost companion while reminiscing about their college days. A heartwarming comedy that critiques the education system while celebrating friendship and pursuing one's passion.",
        "crew": {
            "director": "Rajkumar Hirani",
            "writer": "Abhijat Joshi, Rajkumar Hirani",
            "producer": "Vidhu Vinod Chopra",
            "music": "Shantanu Moitra",
            "cinematography": "C. K. Muraleedharan"
        },
        "box_office": "$90 million"
    },
    {
        "id": 9,
        "title": "Ratchasan",
        "year": 2018,
        "language": "Tamil",
        "rating": 8.3,
        "runtime": "170 min",
        "thumbnail": "https://m.media-amazon.com/images/M/MV5BNTI2YjJmZWYtYjEzZC00MTY5LWI0MzItOWU4OGI0NDBkMmE4XkEyXkFqcGc@._V1_.jpg",
        "poster": "https://m.media-amazon.com/images/M/MV5BMjMzZmY2N2MtYWYwMy00ZTE3LWI2ZDQtMTg1MGViNWYxYmU4XkEyXkFqcGc@._V1_.jpg",
        "genre": ["Crime", "Thriller", "Mystery"],
        "director": "Ram Kumar",
        "cast": ["Vishnu Vishal", "Amala Paul", "Radha Ravi", "Saravanan", "Vinodhini Vaidyanathan"],
        "plot": "An aspiring filmmaker turned cop hunts a psychopathic serial killer targeting schoolgirls. A gripping psychological thriller with edge-of-the-seat suspense and intelligent screenplay.",
        "crew": {
            "director": "Ram Kumar",
            "writer": "Ram Kumar",
            "producer": "G. Dilli Babu",
            "music": "Ghibran",
            "cinematography": "P. V. Sankar"
        },
        "box_office": "$12 million"
    },
    {
        "id": 10,
        "title": "Baahubali: The Beginning",
        "year": 2015,
        "language": "Telugu/Tamil",
        "rating": 8.0,
        "runtime": "159 min",
        "thumbnail": "https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p11546593_p_v8_af.jpg",
        "poster": "https://mir-s3-cdn-cf.behance.net/project_modules/1400/9e081727685123.56369171b80b1.jpg",
        "genre": ["Action", "Adventure", "Fantasy"],
        "director": "S. S. Rajamouli",
        "cast": ["Prabhas", "Rana Daggubati", "Anushka Shetty", "Tamannaah", "Ramya Krishna"],
        "plot": "A young man learns about his royal lineage and destiny while battling for the throne of an ancient kingdom. An epic saga with breathtaking visuals and legendary battle sequences.",
        "crew": {
            "director": "S. S. Rajamouli",
            "writer": "Vijayendra Prasad, S. S. Rajamouli",
            "producer": "Shobu Yarlagadda, Prasad Devineni",
            "music": "M. M. Keeravani",
            "cinematography": "K. K. Senthil Kumar"
        },
        "box_office": "$650 million"
    },
    {
        "id": 11,
        "title": "John Wick",
        "year": 2014,
        "language": "English",
        "rating": 7.4,
        "runtime": "101 min",
        "thumbnail": "https://upload.wikimedia.org/wikipedia/en/9/98/John_Wick_TeaserPoster.jpg",
        "poster": "https://upload.wikimedia.org/wikipedia/en/9/98/John_Wick_TeaserPoster.jpg",
        "genre": ["Action", "Thriller"],
        "director": "Chad Stahelski",
        "cast": ["Keanu Reeves", "Michael Nyqvist", "Alfie Allen", "Willem Dafoe", "Ian McShane"],
        "plot": "A retired hitman seeks vengeance against the men who killed his dog, a final gift from his deceased wife. Stylish action choreography and world-building establish a unique crime universe.",
        "crew": {
            "director": "Chad Stahelski",
            "writer": "Derek Kolstad",
            "producer": "Basil Iwanyk, David Leitch",
            "music": "Tyler Bates, Joel J. Richard",
            "cinematography": "Jonathan Sela"
        },
        "box_office": "$88.8 million"
    },
    {
        "id": 12,
        "title": "The Dark Knight",
        "year": 2008,
        "language": "English",
        "rating": 9.0,
        "runtime": "152 min",
        "thumbnail": "https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg",
        "poster": "https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg",
        "genre": ["Action", "Crime", "Drama"],
        "director": "Christopher Nolan",
        "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart", "Michael Caine", "Gary Oldman"],
        "plot": "Batman faces his greatest challenge when the Joker emerges, plunging Gotham into anarchy. A dark, philosophical take on heroism featuring Heath Ledger's iconic performance as the Joker.",
        "crew": {
            "director": "Christopher Nolan",
            "writer": "Jonathan Nolan, Christopher Nolan",
            "producer": "Emma Thomas, Charles Roven",
            "music": "Hans Zimmer, James Newton Howard",
            "cinematography": "Wally Pfister"
        },
        "box_office": "$1.005 billion"
    },
    {
        "id": 13,
        "title": "The Dark Knight Rises",
        "year": 2012,
        "language": "English",
        "rating": 8.4,
        "runtime": "164 min",
        "thumbnail": "https://upload.wikimedia.org/wikipedia/en/8/83/Dark_knight_rises_poster.jpg",
        "poster": "https://upload.wikimedia.org/wikipedia/en/8/83/Dark_knight_rises_poster.jpg",
        "genre": ["Action", "Drama", "Thriller"],
        "director": "Christopher Nolan",
        "cast": ["Christian Bale", "Tom Hardy", "Anne Hathaway", "Gary Oldman", "Marion Cotillard"],
        "plot": "Eight years after the Joker's rampage, Batman must save Gotham from the terrorist Bane. The epic conclusion to Nolan's trilogy explores themes of redemption and sacrifice.",
        "crew": {
            "director": "Christopher Nolan",
            "writer": "Jonathan Nolan, Christopher Nolan",
            "producer": "Emma Thomas, Christopher Nolan",
            "music": "Hans Zimmer",
            "cinematography": "Wally Pfister"
        },
        "box_office": "$1.081 billion"
    },
    {
        "id": 14,
        "title": "Batman Begins",
        "year": 2005,
        "language": "English",
        "rating": 8.2,
        "runtime": "140 min",
        "thumbnail": "https://upload.wikimedia.org/wikipedia/en/a/af/Batman_Begins_Poster.jpg",
        "poster": "https://upload.wikimedia.org/wikipedia/en/a/af/Batman_Begins_Poster.jpg",
        "genre": ["Action", "Crime", "Drama"],
        "director": "Christopher Nolan",
        "cast": ["Christian Bale", "Michael Caine", "Liam Neeson", "Katie Holmes", "Gary Oldman"],
        "plot": "Bruce Wayne's journey from trauma to becoming Batman, Gotham's dark protector. A grounded origin story that explores fear, justice, and the making of a hero.",
        "crew": {
            "director": "Christopher Nolan",
            "writer": "Christopher Nolan, David S. Goyer",
            "producer": "Larry J. Franco, Charles Roven",
            "music": "Hans Zimmer, James Newton Howard",
            "cinematography": "Wally Pfister"
        },
        "box_office": "$375 million"
    },
    {
        "id": 15,
        "title": "Avengers: Infinity War",
        "year": 2018,
        "language": "English",
        "rating": 8.4,
        "runtime": "149 min",
        "thumbnail": "https://upload.wikimedia.org/wikipedia/en/4/4d/Avengers_Infinity_War_poster.jpg",
        "poster": "https://upload.wikimedia.org/wikipedia/en/4/4d/Avengers_Infinity_War_poster.jpg",
        "genre": ["Action", "Adventure", "Sci-Fi"],
        "director": "Anthony Russo, Joe Russo",
        "cast": ["Robert Downey Jr.", "Chris Hemsworth", "Mark Ruffalo", "Chris Evans", "Scarlett Johansson"],
        "plot": "The Avengers and their allies must stop Thanos from collecting all six Infinity Stones and wiping out half of all life. An epic crossover event with stunning action and emotional stakes.",
        "crew": {
            "director": "Anthony Russo, Joe Russo",
            "writer": "Christopher Markus, Stephen McFeely",
            "producer": "Kevin Feige",
            "music": "Alan Silvestri",
            "cinematography": "Trent Opaloch"
        },
        "box_office": "$2.048 billion"
    }
]


def get_all_movies():
    """Return all movies"""
    return MOVIES


def get_movie_by_id(movie_id):
    """Get movie by ID"""
    for movie in MOVIES:
        if movie["id"] == movie_id:
            return movie
    return None


def search_movies(query):
    """Search movies by title"""
    query = query.lower()
    return [m for m in MOVIES if query in m["title"].lower()]


def get_top_rated_movies(limit=10):
    """Get top rated movies"""
    sorted_movies = sorted(MOVIES, key=lambda x: x["rating"], reverse=True)
    return sorted_movies[:limit]
