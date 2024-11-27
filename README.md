# LoomFinder
LoomFinder is a Python program that retrieves random snippets from books hosted on the Internet Archive, offering users a chance to discover new reads effortlessly.

wget https://raw.githubusercontent.com/DaroHacka/LoomFinder/main/loomfinder.py

Make the file executable:
sudo chmod +x loomfinder.py

Move it to a directory in your PATH:
sudo mv loomfinder.py /usr/local/bin/loomfinder

Run loomfinder:
loomfinder

loomfinder --help
usage: loomfinder [-h] [--save] [--list-genres [LIST_GENRES]] [--list-subjects [LIST_SUBJECTS]] [params ...]

loomfinder: A versatile text searching tool for Archive.org.
Imagine entering a library containing over 28 million documents, you can see books everywhere around you,
however you feel that the most inspiring books are in that particular direction, so you pick one up and
read a random chapter. This is how loomfinder works. Have a nice journey!

positional arguments:
  params                Search parameters: [t:title] [g:genre] [x:anything] [a:author] [s:subject] [d:date]

options:
  -h, --help            show this help message and exit
  --save                Save the output to a file
  --list-genres [LIST_GENRES]
                        List available genres or subgenres of a specific genre
  --list-subjects [LIST_SUBJECTS]
                        List available subjects or specific subfields

**Example usage:**

loomfinder g:adventure a:Tolkien d:1940-1950

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

loomfinder g:adventure a:Tolkien

**Listing genres and subjects:**

If you need a list of genres or subjects for inspiration, please type:

loomfinder --list-genres
loomfinder --list-subjects

--------------------------
November 27, 2024 Updated help menu formatting and added more genres to the --list-genres menu for inspiration. Use loomfinder --list-genres or loomfinder --list-subjects to print lists and customize queries. Use t:title, g:genre, a:author, s:subject, and d:date to specify fields.

November 26, 2024 Final version of LoomFinder. Implemented three new features for better randomization: t:title, g:genre, x:anything, a:author, s:subject, d:date. Removed need for empty quotation marks. Added a help section (loomfinder --help) and set default language to English.

November 25, 2024 Resolved issues with year queries and search parameters. Changed program name from BookieMcRandom to ProsePicker+. Implemented null fields to avoid errors. Added features to handle date ranges and improved randomization. Next steps include implementing language and location criteria.

November 24, 2024 Summary
I created BookieMcRandom, soon to be renamed ProsePickerPlus. It randomly selects and displays text excerpts from over 28 million texts on Archive.orgdirectly to your terminal, allowing users to specify genre, author, and publication date to narrow down the randomization. This tool simplifies exploring Archive.orgdocuments, displaying book titles and authors after a snippet is shown.

Initial Criteria Matching and Search Issues:
Parameters like genre, author, date, words, and language weren't always working correctly.
Length specification (e.g., "200words") needed to be properly implemented.
Default language needed to be set to English.
Selecting random text segments from books required improvement.
Error Handling with HTTP Status Codes:
Handling various HTTP status codes like 200 (OK) and 403 (Forbidden).
Parsing and handling JSON responses from the API.
Optional Arguments:
Ensuring the script could handle optional arguments for genre, author, and date without causing errors.
Generating General Queries:
Handling cases where no parameters were provided to perform a generalized search.
Filtering for Text Content:
Ensuring the search was limited to text content (mediatype:texts) to avoid non-text results like images, videos, or software.
Retry Mechanism:
Implementing a retry mechanism to handle errors like 403 Forbidden and missing text files, and ensuring the script restarts the entire process to select new books upon failure.
Date Range Handling:
Correctly parsing and handling date ranges (e.g., "1810-1820") as well as single years.
Including Book Title in Output:
Ensuring the book title was included in the output along with the random text segment.
Running Script as Executable:
Issues with making the script executable and ensuring the shebang line was correctly recognized.
Misinterpretation of the script as a shell script instead of a Python script.
Fixing Syntax Error Near Unexpected Token:
Resolving syntax errors due to trailing commas and ensuring correct function definitions.
Ensuring Randomization:
Confirming the script restarts from the beginning to select new books on retry, improving the chances of success.
Removing Parameters and Starting Anew:
Language and number of words parameters were removed because they did not work as intended.
Specifying a genre in English returns text in English, while specifying a genre in another language, such as "aventure" in French, returns text in that language.
Adding Punctuation:
Included punctuation in the text segments to improve readability
