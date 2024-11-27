#!/usr/bin/env python3

import requests
import random
import argparse
import re
import sys
import time

# List of genres and subjects for random selection
default_genres_subjects = [
    'literature', 'novel', 'poem', 'fantasy', 'science_fiction', 'mystery', 'romance', 'horror', 'thriller',
    'western', 'biography', 'history', 'self_help', 'travel', 'true_crime', 'biology', 'chemistry', 'physics',
    'astronomy', 'earth_science', 'environmental_science', 'computer_science', 'engineering', 'medicine', 'ancient_history',
    'medieval_history', 'modern_history', 'archaeology', 'art_history', 'economic_history', 'political_history', 'social_history',
    'metaphysics', 'epistemology', 'ethics', 'logic', 'aesthetics', 'philosophy_of_science', 'philosophy_of_mind',
    'clinical_psychology', 'cognitive_psychology', 'developmental_psychology', 'social_psychology', 'neuropsychology',
    'clinical_psychiatry', 'forensic_psychiatry', 'child_psychiatry', 'geriatric_psychiatry', 'organic_chemistry',
    'inorganic_chemistry', 'physical_chemistry', 'biochemistry', 'botany', 'zoology', 'microbiology', 'genetics',
    'classical_mechanics', 'quantum_mechanics', 'thermodynamics', 'electromagnetism', 'algebra', 'calculus', 'geometry', 'statistics'
    'anthropology', 'sociology', 'paleontology', 'linguistics', 'mythology', 'numismatics', 'seismology', 'meteorology', 
    'crystallography', 'petrology', 'selenology', 'histology', 'cryogenics', 'entomology', 'protozoology', 'virology', 
    'bacteriology', 'cytology', 'immunology', 'hermeneutics', 'patristics', 'textology', 'syntax', 'semantics', 'phonology',
    'phonetics', 'philology', 'cartography', 'epigraphy', 'heraldry', 'lexicography', 'chronology', 'onomastics', 'aetiology',
    'graphology', 'apiculture', 'aquaculture', 'pisciculture', 'horticulture', 'herpetology', 'ichthyology', 'ornithology', 'mammalogy',
    'helminthology', 'dipterology', 'acarology', 'zoology', 'botany', 'ornithology'
]

# Function to build the query string
def build_query_string(title=None, genre=None, anything=None, author=None, subject=None, start_date=None, end_date=None):
    query = ['mediatype:texts', 'language:(english)']  # Add default language: English
    
    # Select a random genre or subject if no criteria are provided
    if not title and not genre and not anything and not author and not subject and not start_date:
        default_choice = random.choice(default_genres_subjects)
        query.append(f'({default_choice})')
    
    if title:
        query.append(f'title:({title})')
    
    if genre:
        query.append(f'genre:({genre})')
        
    if anything:
        query.append(f'({anything})')

    if author:
        query.append(f'creator:({author})')

    if subject:
        query.append(f'subject:({subject})')

    if start_date and end_date:
        query.append(f'date:[{start_date}-01-01 TO {end_date}-12-31]')
    elif start_date:
        query.append(f'date:[{start_date}-01-01 TO {start_date}-12-31]')

    query_string = " AND ".join(query)
    return query_string

# Function to parse parameters
def parse_parameters(params):
    # Initialize all parameters as None
    title, genre, anything, author, subject, date = None, None, None, None, None, None
    
    # Parse provided parameters
    for param in params:
        if param.startswith('t:'):
            title = param[2:]
        elif param.startswith('g:'):
            genre = param[2:]
        elif param.startswith('x:'):
            anything = param[2:]
        elif param.startswith('a:'):
            author = param[2:]
        elif param.startswith('s:'):
            subject = param[2:]
        elif param.startswith('d:'):
            date = param[2:]
    
    return title, genre, anything, author, subject, date

# Function to get random book
def get_random_book(query_string, retry_limit=5):
    attempt = 0
    while attempt < retry_limit:
        url = f"https://archive.org/advancedsearch.php?q={query_string}&fl[]=identifier&fl[]=title&fl[]=creator&rows=50&page=1&output=json"
        print(f"Query URL: {url}")  # Debugging print statement

        try:
            response = requests.get(url)
            if response.status_code == 200:
                books = response.json().get("response", {}).get("docs", [])
                if books:
                    return random.choice(books)
            elif response.status_code == 403:
                print("403 Forbidden. Retrying...")
        except Exception as e:
            print(f"Error: {e}. Retrying...")

        attempt += 1
        time.sleep(1)  # Sleep between retries
    raise Exception("Failed to fetch data after multiple attempts.")

# Function to get random text segment
def get_random_text_segment(book, retry_limit=5):
    attempt = 0
    while attempt < retry_limit:
        metadata_url = f"https://archive.org/metadata/{book['identifier']}"
        response = requests.get(metadata_url)
        if response.status_code != 200:
            print(f"Failed to fetch metadata: {response.status_code}. Retrying...")
            attempt += 1
            time.sleep(1)
            continue

        metadata = response.json()
        files = metadata.get("files", [])
        txt_files = [file for file in files if file.get("name", "").endswith(".txt")]

        if not txt_files:
            print("No text file available for this book. Retrying...")
            attempt += 1
            time.sleep(1)
            continue

        text_url = f"https://archive.org/download/{book['identifier']}/{txt_files[0]['name']}"
        response = requests.get(text_url)
        if response.status_code != 200:
            print(f"Failed to fetch book content: {response.status_code}. Retrying...")
            attempt += 1
            time.sleep(1)
            continue

        text = response.text
        words = re.findall(r'\S+', text)  # Match non-whitespace sequences to preserve punctuation
        num_words = 200  # Default to 100 words if not specified
        if len(words) < num_words:
            print("The book doesn't contain enough words. Retrying...")
            attempt += 1
            time.sleep(1)
            continue

        start = random.randint(0, len(words) - num_words)
        segment = words[start:start + num_words]

        end_index = start + num_words
        while end_index < len(words) and not words[end_index].endswith('.'):
            segment.append(words[end_index])
            end_index += 1

        author = book.get('creator', 'Unknown Author')
        return book['title'], author, ' '.join(segment)
    raise Exception("Failed to fetch valid text segment after multiple attempts.")

# Function to save output to file
def save_to_file(content, filename="LoomFinder_samples.txt"):
    with open(filename, "a") as file:
        file.write(content + "\n\n")

# Help Menu
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''LoomFinder: A versatile text searching tool for Archive.org.
Imagine entering a library containing over 28 million documents, you can see books everywhere around you,
however you feel that the most inspiring books are in that particular direction, so you pick one up and
read a random chapter. This is how LoomFinder works. Have a nice journey!''',
        epilog='''
**Example usage:**

LoomFinder g:adventure a:Tolkien d:1940-1950

**Parameters:**

* t:title           The title of the book or text.
* g:genre           The genre of the book or text.
* x:anything        The general attribute of the book or text.
* a:author          The author of the book or text.
* s:subject         The subject of the book or text.
* d:date            The date or date range of the book or text.

**Combining parameters:**

You can omit any parameter by not including it in the command.
For example, if you want to search only by genre and author, use:

LoomFinder g:adventure a:Tolkien

**Listing genres and subjects:**

If you need a list of genres or subjects for inspiration, please type:

LoomFinder --list-genres
LoomFinder --list-subjects
''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('params', nargs='*', help='Search parameters: [t:title] [g:genre] [x:anything] [a:author] [s:subject] [d:date]')
    parser.add_argument('--save', action='store_true', help='Save the output to a file')
    parser.add_argument('--list-genres', nargs='?', const=True, help='List available genres or subgenres of a specific genre')
    parser.add_argument('--list-subjects', nargs='?', const=True, help='List available subjects or specific subfields')

    args = parser.parse_args()
    params = args.params

    genres = {
        "g:genre": {
            "Fiction": ["Fantasy", "Science Fiction", "Mystery", "Romance", "Horror", "Thriller/Suspense", "Western", "Literary Fiction"],
            "Nonfiction": ["Biography/Autobiography", "History", "Self-Help", "Travel", "True Crime"]
        },
        "s:subject": {
            "Fantasy/Sci-Fi": ["Dark Fantasy", "Fairy Tales", "Space Opera", "Cyberpunk", "Dystopian", "Alternate History"],
            "Classic Literature": ["Detective Fiction", "Hard-Boiled", "Historical Romance", "Contemporary Romance", "Paranormal Romance", "Romantic Comedy", "Gothic Horror", "Psychological Horror", "Supernatural Horror", "Crime Thriller", "Classic Literature", "Modernist Literature", "Postmodern Literature"]
        }
    }

    # List genres or subjects if requested
    if args.list_genres:
        if args.list_genres is True:
            print("Available genres and subjects:")
            for category, subcategories in genres.items():
                print(f"Try with {category}:")
                for subcategory, subgenres in subcategories.items():
                    print(f"- {subcategory}: {', '.join(subgenres)}")
        else:
            print(f"Available subgenres for {args.list_genres}: {', '.join(genres.get(args.list_genres, {}).get(args.list_genres, []))}")
        sys.exit(0)

    subjects = {
        "Scientific": ["Biology", "Chemistry", "Physics", "Astronomy", "Earth Sciences", "Environmental Science", "Computer Science", "Engineering", "Medicine"],
        "Historical": ["Ancient History", "Medieval History", "Modern History", "Archaeology", "Art History", "Economic History", "Political History", "Social History"],
        "Philosophy": ["Metaphysics", "Epistemology", "Ethics", "Logic", "Aesthetics", "Philosophy of Science", "Philosophy of Mind"],
        "Psychology": ["Clinical Psychology", "Cognitive Psychology", "Developmental Psychology", "Social Psychology", "Neuropsychology"],
        "Psychiatry": ["Clinical Psychiatry", "Forensic Psychiatry", "Child and Adolescent Psychiatry", "Geriatric Psychiatry"],
        "Chemistry": ["Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry", "Biochemistry"],
        "Biology": ["Botany", "Zoology", "Microbiology", "Genetics"],
        "Physics": ["Classical Mechanics", "Quantum Mechanics", "Thermodynamics", "Electromagnetism"],
        "Math": ["Algebra", "Calculus", "Geometry", "Statistics"],
        "Mediums": ["Scholarly Journals", "Trade Journals", "Magazines", "Newspapers", "Historical Journals", "Microfilm"]
    }

    if args.list_subjects:
        if args.list_subjects is True:
            print("Available subjects:")
            for subject, subfields in subjects.items():
                print(f"{subject}: {', '.join(subfields)}")
        else:
            print(f"Available subfields for {args.list_subjects}: {', '.join(subjects.get(args.list_subjects, []))}")
        sys.exit(0)

    # Parse parameters
    title, genre, anything, author, subject, date = parse_parameters(params)

    # Parse the date argument
    start_date = end_date = None
    if date:
        if '-' in date:
            start_date, end_date = date.split('-')
            start_date += "-01-01"
            end_date += "-12-31"
        else:
            start_date = date + "-01-01"
            end_date = date + "-12-31"

    query_string = build_query_string(title=title, genre=genre, anything=anything, author=author, subject=subject, start_date=start_date, end_date=end_date)
    print(f"Query String: {query_string}")  # Debugging print statement

    try:
        book = get_random_book(query_string)
        title, author, text_segment = get_random_text_segment(book)
        output = f"Book Title: {title}\nAuthor: {author}\nRandom Text Segment: {text_segment}"
        print(output)

        if args.save:
            save_to_file(output)
            print("Output saved to file.")

    except Exception as e:
        print(e)


        #Author: Daniel Forster Levene: 
        #Date: November 25, 2024 Version: 1.3.1
        #Contact: cdan_crystalblue01@outlook.com
