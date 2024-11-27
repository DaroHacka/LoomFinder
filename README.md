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
November 27, 2024
I needed to make a final adjustment to the help menu formatting and add more referential material to the --list-genres menu to help users who might experience a sudden lack of inspiration. By typing --list-genres, they can see a rich list of genres to customize their queries.
Here’s how it works:
If you don't know what to type, use the following commands:
loomfinder --list-genres
or
loomfinder --list-subjects
A list will be printed, and you can use it in your query like this:
loomfinder g:genre (one of the genres listed)
or
loomfinder s:subject (one of the subject listed)
The code will then randomize the book or document, and randomize the extracted text. The text will be displayed on the screen along with the title and author (if available). If you like the displayed snippet and want another random excerpt from that book, change the parameters to t:title. If the title is too generic, you can add a:author. The text will then be derived directly from that specific book. If you decide to read the book, you can connect to Internet Archive and download it.

November 26, 2024
Finally, this is the last about BookieMcRandom, aka ProsePicker+, aka loomfinder. This is the final version of my program, loomfinder—a name I chose by combining one of my favorite films, Flight of the Navigator, which I believe influenced my mindset at a very early stage, and the LucasArts game. There will be no further upgrades, hopefully. 
However, I made some modifications and I think it's better now, no need to add anything else.
From time to time, I may want to randomize some Internet Archive queries just for fun. I have one final idea to perfect the randomization process, which involves selecting from a file filled with authors' names that cohesively belong to the literary world and applying one of those to the query automatically. You create your own selection of authors to have a more literature-consistent application. This method might solve the localization problem, as the Archive doesn’t localize books. By dividing authors into nationalities, we can achieve a more cultivated randomization. I could keep both programs—loomfinder for a wilder randomization, and ProsePicker+ for selecting literary prose and poems. There’s no need to add authors manually, as there are many databases available online.
However, I implemented loomfinder by adding three new features:
The idea of adding quotation marks to send a null field to the query on Internet Archive (see previous post) was inelegant. This method required placing empty quotation marks "" in place of an omitted criterion. For example: loomfinder "" "Haruki Murakami" 1980-1990, where the empty "" is in place of genre but to state a null field is necessary to maintain the structure intact. I solved this issue with a more elegant solution by attributing a letter to each of these categories: t:title, g:genre, a:author, s:subject, d:date, so that the code understands what is what. This way, there's no need to write an empty ""—when the script sees that one of those t, g, x, a, s, d is missing, it sends a null value automatically. 
Now you can type: 

loomfinder d:1990-2000
loomfinder t:"Norwegian Wood" 
loomfinder g:mistery d:1880-1900
loomfinder x:literature

As you can see, I added three categories: t:title x:anything and s:subject. Sometimes we may want to randomize from a specific book, or we may want to address the randomization by adding a subject or just anything containing that word or couple of words. With the old solution, if I wanted to print only the subject, since there are five categories now, I had to manually add 4 empty "" like this: 
loomfinder "" "" "" s:"historical journals" "" 
Now you can type: 

loomfinder s:epistolary
loomfinder x:history
Finally, I added a help section to serve as a reminder on how to use it, by somply typing 
loomfinder --help every time you need help. 

I also added some samples to make a more inspired randomization. You can also print a list of detailed genres, subgenres, and subjects. You have to do it manually, pick what inspires you, and insert it in the query as shown from the screenshots below.
So that's about all. I also set the default language to English to avoid getting results in all kinds of languages when no parameters are typed in, ensuring 100% randomization by only typing: 
loomfinder
I also addressed some errors in the script and added 50 more words to the printed out query. And that's about all I believe.
--------------------------

note: A user who tested this code found that running it without any parameters, simply by typing loomfinder, resulted in a catalog of Power Plant Engineering entries and nothing else. I checked it myself by looking at my screenshots and trying again in the terminal. He was right. After some thought, I realized that I needed to randomize the default search within the script. By adding a comprehensive list of topics, genres, and formats, the script can now generate a randomized query when no specific criteria are provided, avoiding the issue of returning only Power Plant Engineering results. So I substituted the Pastebin link with version 1.3.1. Also, by modifying the script yourself, you can add as many other objects as you want to better randomize the default query.
edit: What I thought was g:genre was actually "search anything." However, I fixed it. Now, g:genre is truly the genre criterion for the search, while the x:anything criterion is useful because it allows for a general search. It’s like saying "find anything at all containing this word." This could be a single word in the title, a format, or a genre in a broad sense. Previously, x:anything was labeled as g:genre incorrectly, basically it was g:anything. With this correction, g:genre is now correctly identifying literary genres, which is great.

November 25, 2024
I solved two main problems with this new version of the script. The first issue was that I could only query a specific year or no time reference at all. The problem was that Archive. org requires specifying the month and day as well, so I integrated this into the code. There’s no need to type it on the command line. For example, as shown in the images below, you can run:
ProsePicker+ novel "Charles Dickens" 1840-1870
The script will then add "1840-01-01 TO 1870-12-31". This resolves the issue and is crucial for randomization; it doesn't make much sense to randomize within a single year without any other option.
The second issue was with the search parameters. Oh, by the way, I changed the program's name from BookieMcRandom to ProsePicker+. 
The format used to run the program is:
ProsePicker+ genre author date
These occupy position 1, position 2, and position 3, respectively. However, if I didn't want to specify a genre, an error occurred which I didn't quite understand: the author inherited position 1 and it was mistakenly searched as the genre, and the date inherited position 2 and it was searched as the creator. Similarly, if I didn't want to specify the author, the date inherited position 2. I discovered this by mere chance because one of the titles had the same years I had set.
So, I came up with the idea to send a null field that simply contains a null value but ensures the structure doesn't collapse on itself. As with SubtitlesSmoothie, I used quotation marks, I am starting to think they are always the problem or the solution! 
For example, if I wanted to omit the author and leave the rest, the syntax would be:
ProsePicker+ romance "" 1800-1820
If I wanted to omit the genre and the year but not the author, the syntax would be:
ProsePicker+ "" "Stephen King" ""
Now, I can randomize in almost any way. I need to implement language criteria, which is easy but I have no time this week, and location support, for which I still need to figure out how Archive defines location, whether it's the place where the author is from or where the book was first published.
When a text shows many typos, it's often because the original document that the Archive database converts from PDF scans to text files is either very old or very faded. In such cases, even when reading the original scan, you might struggle to read it with your own eyes. the OCR software, which relies on visual clarity to accurately convert images of text into digital text, might misinterpret the text. But that happens very seldom.

November 24, 2024
I created BookieMcRandom, but I might rename it to ProsePickerPlus when I release a more stable version. BookieMcRandom is designed to randomly select and display text excerpts from books and documents hosted on Archive. org directly to your terminal. At the moment Archive. org houses over 28 million texts, that means this script can randomize on over 28 million texts. However it allows users to specify various parameters such as genre, author, and publication date to narrow down the randomization. Instead of randomizing 28 million objects, you simply decrease the probability. In fact it can also perform a broad search if no parameters are provided.
This tool is particularly useful for exploring Archive. org documents, increasing the chances of reading excerpts from books you might otherwise never have the chance to read. Imagine stepping into a library, grabbing a book at random, and reading an unexpected passage. Since the title of the book is provided after you run the program, you can go directly to Archive. org and pick up that exactly same book if you feel inspired and you want to read it. Sometimes, you simply want to enjoy random snippets of historical and literary works, so this program is perfect for that purpose. As shown in the screenshots below, you can also print an extract directly from a specific author and their works, which is pretty neat - in that case is less of a randomizer and more of an extrapolation tool. The advantage is that you only have to type BookieMcRandom in your terminal, and in less than five seconds, you’ll see the text appear on your display. Otherwise, you have to connect to Archive. org, manually and randomly select a book, fold through the pages, and pick a paragraph.
In part, this is to honor Archive. org, which has helped me in my research with countless documents over the years. It's also something I always wanted but never put thought on it. Today, I had some spare time and spent all afternoon and evening trying to make it work. 
However, there are still some minor issues and implementations I need to solve. I couldn't get it to work exactly as I wanted mainly because I don't fully understand how all the parameters in advanced search work on Archive. org. For example, if I set a range of years, like 1810-1820, it doesn't work at the moment. I can only specify individual years such as 1956 or 1816. I would prefer to have a range of years rather than a single year, so you can say randomize between 1900-1905. So I need to look into that. However, you can randomize one year or omit the year entirely and by adding the genre and the author, the script will pick something up.
Aside from the date range issue, the two main problems at the moment are with books that don't have a .txt version. For each book stored on Archive. org, there are different formats: PDF, EPUB, DJVU, DAISY, TXT, and HTML. I opted for TXT because it's faster to compute and by the way the majority of them have a txt file available. I also need to try HTML and see if it's faster, so I need to code in a way that if a TXT version isn't available, it tries HTML, then EPUB, then PDF and so forth. This should reduce the error messages when no .txt file for that randomization is found. Currently, if no txt files are found, the script repeats until it works by checking other book selections. I implemented this because I often received "not found" errors after running BookieMcRandom on terminal, so no need to type that manually each time. Just give me the answer when you get it done! 

Initially, the script displayed extracts in various languages such as French, Indonesian, Chinese, Arabic, German, etc. but I wanted it to print the extract in English by default and in any other language if specified in the format: 
BookieMcRandom genre author year language 
But it didn't work. However, since the genre is written in English (e.g., drama, adventure, comedy, history, romance, novel, poems), the results are mostly in English. This can still be improved.
I also tried to implement the length of the printed message by allowing users to specify the word count directly when running the program. For example: 
BookieMcRandom genre author year 300words 
It should print 300 words. By default I set to pint out 100 words, but I can modify the script if I want more or fewer words. However, I still need to implement this functionality so that I can increase or decrease directly on command line.
I also want to add other search criteria such as where the book was originally printed. For example, randomizing English texts written in France, Germany, Russia, Greece, and so forth.
If I wanted to, I could set a cron job in bash to send me a daily randomization via email or to my phone. Additionally, if I had a website, I could add a randomization to one corner of the page that updates every time the page is refreshed so that a quotation is displayed.

Here is a list of all the issues I encountered >>>>>

### Summary of All Issues Encountered:
1. **Initial Criteria Matching and Search Issues:**
   - Parameters like genre, author, date, words, and language weren't always working correctly.
   - Length specification (e.g., "200words") needed to be properly implemented.
   - Default language needed to be set to English.
   - Selecting random text segments from books required improvement.
2. **Error Handling with HTTP Status Codes:**
   - Handling various HTTP status codes like 200 (OK) and 403 (Forbidden).
   - Parsing and handling JSON responses from the API.
3. **Optional Arguments:**
   - Ensuring the script could handle optional arguments for genre, author, and date without causing errors.
4. **Generating General Queries:**
   - Handling cases where no parameters were provided to perform a generalized search.
5. **Filtering for Text Content:**
   - Ensuring the search was limited to text content (`mediatype:texts`) to avoid non-text results like images, videos, or software.
6. **Retry Mechanism:**
   - Implementing a retry mechanism to handle errors like 403 Forbidden and missing text files, and ensuring the script restarts the entire process to select new books upon failure.
7. **Date Range Handling:**
   - Correctly parsing and handling date ranges (e.g., "1810-1820") as well as single years.
8. **Including Book Title in Output:**
   - Ensuring the book title was included in the output along with the random text segment.
9. **Running Script as Executable:**
   - Issues with making the script executable and ensuring the shebang line was correctly recognized.
   - Misinterpretation of the script as a shell script instead of a Python script.
10. **Fixing Syntax Error Near Unexpected Token:**
    - Resolving syntax errors due to trailing commas and ensuring correct function definitions.
11. **Ensuring Randomization:**
    - Confirming the script restarts from the beginning to select new books on retry, improving the chances of success.
12. **Removing Parameters and Starting Anew:**
    - Language and number of words parameters were removed because they did not work as intended.
    - Specifying a genre in English returns text in English, while specifying a genre in another language, such as "aventure" in French, returns text in that language.
13. **Adding Punctuation:**
    - Included punctuation in the text segments to improve readability
