#!/usr/bin/env python3

import requests
import random
import argparse
import re
import sys
import time
import signal

class TimeoutExpired(Exception):
    pass

def input_with_timeout(prompt, timeout):
    def handler(signum, frame):
        raise TimeoutExpired

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)
    try:
        return input(prompt)
    except TimeoutExpired:
        print("\nNo response received. Program will end now.")
    finally:
        signal.alarm(0)

# List of genres and subjects for random selection
literature_genres = [
    'literature', 'novel', 'poem', 'fantasy', 'science_fiction', 'mystery', 'romance', 'horror', 'thriller', 'western',
    'historical_fiction', 'magical_realism', 'satire', 'adventure', 'young_adult', 'graphic_novels', 'urban_fantasy',
    'epic_fantasy', 'dystopian', 'steampunk', 'detective_fiction', 'psychological_thriller', 'paranormal_romance',
    'space_opera', 'cyberpunk'
]

other_subjects = [
    'biography', 'history', 'self_help', 'travel', 'true_crime', 'biology', 'chemistry', 'physics',
    'astronomy', 'earth_science', 'environmental_science', 'computer_science', 'engineering', 'medicine', 'ancient_history',
    'medieval_history', 'modern_history', 'archaeology', 'art_history', 'economic_history', 'political_history', 'social_history',
    'metaphysics', 'epistemology', 'ethics', 'logic', 'aesthetics', 'philosophy_of_science', 'philosophy_of_mind',
    'clinical_psychology', 'cognitive_psychology', 'developmental_psychology', 'social_psychology', 'neuropsychology',
    'clinical_psychiatry', 'forensic_psychiatry', 'child_psychiatry', 'geriatric_psychiatry', 'organic_chemistry',
    'inorganic_chemistry', 'physical_chemistry', 'biochemistry', 'botany', 'zoology', 'microbiology', 'genetics',
    'classical_mechanics', 'quantum_mechanics', 'thermodynamics', 'electromagnetism', 'algebra', 'calculus', 'geometry', 'statistics',
    'anthropology', 'sociology', 'paleontology', 'linguistics', 'mythology', 'numismatics', 'seismology', 'meteorology', 
    'crystallography', 'petrology', 'selenology', 'histology', 'cryogenics', 'entomology', 'protozoology', 'virology', 
    'bacteriology', 'cytology', 'immunology', 'hermeneutics', 'patristics', 'textology', 'syntax', 'semantics', 'phonology',
    'phonetics', 'philology', 'cartography', 'epigraphy', 'heraldry', 'lexicography', 'chronology', 'onomastics', 'aetiology',
    'graphology', 'apiculture', 'aquaculture', 'pisciculture', 'horticulture', 'herpetology', 'ichthyology', 'ornithology', 'mammalogy',
    'helminthology', 'dipterology', 'acarology'
]

default_genres_subjects = literature_genres + other_subjects

# Function to build the query string
def build_query_string(title=None, genre=None, anything=None, author=None, subject=None, start_date=None, end_date=None):
    query = ['mediatype:texts', 'language:(english)']  # Add default language: English
    
    # Select a random genre or subject if no criteria are provided
    if not title and not genre and not anything and not author and not subject and not start_date:
        default_choice = get_weighted_random_choice()
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
        url = f"https://archive.org/advancedsearch.php?q={query_string}&fl[]=identifier&fl[]=title&fl[]=creator&rows=1000&page=1&output=json"
        print(f"Query URL: {url}")  # Debugging print statement

        try:
            response = requests.get(url)
            if response.status_code == 200:
                books = response.json().get("response", {}).get("docs", [])
                if books:
                    return random.choice(books)  # Break out of the loop if a book is found
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
        num_words = 200  # Default to 200 words if not specified
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
        return book['title'], author, ' '.join(segment)  # Break out of the loop if a valid segment is found
    raise Exception("Failed to fetch valid text segment after multiple attempts.")

# Function to save output to file
def save_to_file(content, filename="loomfinder_samples.txt"):
    with open(filename, "a") as file:
        file.write(content + "\n\n")

# Function to save author to file
def save_author(author, filename="Authors_list.txt"):
    with open(filename, "a") as file:
        file.write(author + "\n")

# Function to get a random author from the saved list
def get_random_saved_author(filename="Authors_list.txt"):
    try:
        with open(filename, "r") as file:
            authors = file.readlines()
        return random.choice(authors).strip() if authors else None
    except FileNotFoundError:
        return None

# Function to build weighted random choice
def get_weighted_random_choice():
    weights = [0.8 if genre in literature_genres else 0.2 for genre in default_genres_subjects]
    return random.choices(default_genres_subjects, weights=weights, k=1)[0]

# Main script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''LoomFinder: A versatile text searching tool for Archive.org.
Imagine entering a library containing over 28 million documents, you can see books everywhere around you,
however you feel that the most inspiring books are in that particular direction, so you pick one up and
read a random chapter. This is how loomfinder works. Have a nice journey!''',
        epilog='''
**Example usage:**

loomfinder g:adventure a:Tolkien d:1940-1950

**Parameters:**

* t:title           The title of the book or text.
* g:genre           The genre of the book or text.
* x:anything        The general attribute of the book or text.
* a:author          The author of the book or text.
* s:subject         The subject of the book or text.
* d:date            The date or date range of the book or text.
* prose             :loomfinder prose -> randomly select an author from a saved list when running with the prose parameter.

**Combining parameters:**

You can omit any parameter by not including it in the command.
For example, if you want to search only by genre and author, use:

loomfinder g:adventure a:Tolkien

**Listing genres and subjects:**

If you need a list of genres or subjects for inspiration, please type:

loomfinder --list-genres
loomfinder --list-subjects
''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('params', nargs='*', help='Search parameters: [t:title] [g:genre] [x:anything] [a:author] [s:subject] [d:date]')
    parser.add_argument('--save', action='store_true', help='Save the output to a file')
    parser.add_argument('--list-genres', nargs='?', const=True, help='List available genres or subgenres of a specific genre')
    parser.add_argument('--list-subjects', nargs='?', const=True, help='List available subjects or specific subfields')

    args = parser.parse_args()
    params = args.params

    # Handling the prose parameter
    if 'prose' in params:
        author = get_random_saved_author()
        if not author:
            print("No authors available in the saved list.")
            sys.exit(0)
        
        # Update the query to use the random saved author
        query_string = build_query_string(author=author)
        print(f"Query String: {query_string}")  # Debugging print statement

        try:
            book = get_random_book(query_string)
            title, author, text_segment = get_random_text_segment(book)
            output = f"Book Title: {title}\nAuthor: {author}\nRandom Text Segment: {text_segment}"
            print(output)

        except Exception as e:
            print(e)

    else:
        # Existing logic for parsing parameters and building query
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

        # Add authors from the saved list to default genres
        saved_authors = []
        try:
            with open("Authors_list.txt", "r") as file:
                saved_authors = [author.strip() for author in file.readlines()]
        except FileNotFoundError:
            pass

        if saved_authors:
            default_genres_subjects += saved_authors

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
            
            # Prompt to save author at the end
            try:
                save_author_choice = input_with_timeout("Do you want to save the author's name? (yes/no): ", 10)
                if save_author_choice and save_author_choice.lower() in ["yes", "y"]:
                    save_author(author)
                    print("Author's name saved.")
                elif save_author_choice and save_author_choice.lower() in ["no", "n"]:
                    print("Author's name not saved.")
            except TimeoutExpired:
                pass

        except Exception as e:
            print(e)

        #Author: Daniel Forster Levene: 
        #Date: November 25, 2024 Version: 1.4.1
        #Contact: cdan_crystalblue01@outlook.com
