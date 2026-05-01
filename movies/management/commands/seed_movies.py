"""
Management command: python manage.py seed_movies
Populates the database with 20 sample movies for demo / testing purposes.
"""

from django.core.management.base import BaseCommand
from movies.models import Movie


SAMPLE_MOVIES = [
    {
        'title': 'The Dark Knight',
        'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
        'genre': 'action',
        'release_year': 2008,
        'director': 'Christopher Nolan',
        'actors': 'Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine',
    },
    {
        'title': 'Inception',
        'description': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
        'genre': 'sci-fi',
        'release_year': 2010,
        'director': 'Christopher Nolan',
        'actors': 'Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page, Tom Hardy',
    },
    {
        'title': 'Interstellar',
        'description': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival when Earth becomes uninhabitable.',
        'genre': 'sci-fi',
        'release_year': 2014,
        'director': 'Christopher Nolan',
        'actors': 'Matthew McConaughey, Anne Hathaway, Jessica Chastain, Michael Caine',
    },
    {
        'title': 'Pulp Fiction',
        'description': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits interweave in four tales of violence and redemption.',
        'genre': 'crime',
        'release_year': 1994,
        'director': 'Quentin Tarantino',
        'actors': 'John Travolta, Uma Thurman, Samuel L. Jackson, Bruce Willis',
    },
    {
        'title': 'The Shawshank Redemption',
        'description': 'Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.',
        'genre': 'drama',
        'release_year': 1994,
        'director': 'Frank Darabont',
        'actors': 'Tim Robbins, Morgan Freeman, Bob Gunton, William Sadler',
    },
    {
        'title': 'Forrest Gump',
        'description': 'The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.',
        'genre': 'drama',
        'release_year': 1994,
        'director': 'Robert Zemeckis',
        'actors': 'Tom Hanks, Robin Wright, Gary Sinise, Sally Field',
    },
    {
        'title': 'The Matrix',
        'description': 'When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth — the life he knows is the elaborate deception of an evil cyber-intelligence.',
        'genre': 'sci-fi',
        'release_year': 1999,
        'director': 'The Wachowskis',
        'actors': 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving',
    },
    {
        'title': 'Avengers: Endgame',
        'description': 'After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more to reverse Thanos\' actions.',
        'genre': 'action',
        'release_year': 2019,
        'director': 'Anthony Russo, Joe Russo',
        'actors': 'Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth',
    },
    {
        'title': 'The Godfather',
        'description': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
        'genre': 'crime',
        'release_year': 1972,
        'director': 'Francis Ford Coppola',
        'actors': 'Marlon Brando, Al Pacino, James Caan, Richard Castellano',
    },
    {
        'title': 'Joker',
        'description': 'In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime.',
        'genre': 'thriller',
        'release_year': 2019,
        'director': 'Todd Phillips',
        'actors': 'Joaquin Phoenix, Robert De Niro, Zazie Beetz, Frances Conroy',
    },
    {
        'title': 'Parasite',
        'description': 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.',
        'genre': 'thriller',
        'release_year': 2019,
        'director': 'Bong Joon-ho',
        'actors': 'Kang-ho Song, Sun-kyun Lee, Yeo-jeong Jo, Woo-sik Choi',
    },
    {
        'title': 'Spider-Man: No Way Home',
        'description': 'With Spider-Man\'s identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds start to appear.',
        'genre': 'action',
        'release_year': 2021,
        'director': 'Jon Watts',
        'actors': 'Tom Holland, Zendaya, Benedict Cumberbatch, Jacob Batalon',
    },
    {
        'title': 'The Lion King',
        'description': 'Lion cub and future king Simba searches for his identity. His eagerness to please others and his father Mufasa\'s tragic death complicates things.',
        'genre': 'animation',
        'release_year': 1994,
        'director': 'Roger Allers, Rob Minkoff',
        'actors': 'Matthew Broderick, Jeremy Irons, James Earl Jones, Moira Kelly',
    },
    {
        'title': 'Titanic',
        'description': 'A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.',
        'genre': 'romance',
        'release_year': 1997,
        'director': 'James Cameron',
        'actors': 'Leonardo DiCaprio, Kate Winslet, Billy Zane, Kathy Bates',
    },
    {
        'title': 'Get Out',
        'description': 'A young African-American visits his white girlfriend\'s parents for the weekend, where his simmering unease about their community grows into a terrifying reality.',
        'genre': 'horror',
        'release_year': 2017,
        'director': 'Jordan Peele',
        'actors': 'Daniel Kaluuya, Allison Williams, Bradley Whitford, Catherine Keener',
    },
    {
        'title': 'La La Land',
        'description': 'While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.',
        'genre': 'romance',
        'release_year': 2016,
        'director': 'Damien Chazelle',
        'actors': 'Ryan Gosling, Emma Stone, John Legend, J.K. Simmons',
    },
    {
        'title': 'The Prestige',
        'description': 'After a tragic accident, two stage magicians engage in a battle to create the ultimate illusion while sacrificing everything they have to outwit each other.',
        'genre': 'mystery',
        'release_year': 2006,
        'director': 'Christopher Nolan',
        'actors': 'Christian Bale, Hugh Jackman, Scarlett Johansson, Michael Caine',
    },
    {
        'title': 'Dune',
        'description': 'Paul Atreides, a brilliant and gifted young man born into a great destiny beyond his understanding, must travel to the most dangerous planet in the universe to ensure the future of his family and his people.',
        'genre': 'sci-fi',
        'release_year': 2021,
        'director': 'Denis Villeneuve',
        'actors': 'Timothée Chalamet, Rebecca Ferguson, Oscar Isaac, Zendaya',
    },
    {
        'title': 'Coco',
        'description': 'Aspiring musician Miguel, confronted with his family\'s ancestral ban on music, enters the Land of the Dead to find his great-great-grandfather, a legendary singer.',
        'genre': 'animation',
        'release_year': 2017,
        'director': 'Lee Unkrich',
        'actors': 'Anthony Gonzalez, Gael García Bernal, Benjamin Bratt, Alanna Ubach',
    },
    {
        'title': 'Oppenheimer',
        'description': 'The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II.',
        'genre': 'biography',
        'release_year': 2023,
        'director': 'Christopher Nolan',
        'actors': 'Cillian Murphy, Emily Blunt, Matt Damon, Robert Downey Jr.',
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with 20 sample movies'

    def handle(self, *args, **kwargs):
        created = 0
        skipped = 0
        for data in SAMPLE_MOVIES:
            obj, was_created = Movie.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Done! Created {created} movies. Skipped {skipped} duplicates.'
            )
        )
