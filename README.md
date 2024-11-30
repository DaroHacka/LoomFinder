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

Version 1.4.0 is way more stable than the previous one, and by simply modifying the rows in rows=1000&page=1 
from 50 to 1000, the rate of success has increased noticeably.

You can now save the author of your query. LoomFinder will ask you if you want to save the author or pass. 
The advantage is that each time you save a new author to your text file, your list of authors will grow. Then 
you can run loomfinder prose, and a random selection will be made from your text file and sent as a new query 
to the Internet Archive.

At the end of each query, LoomFinder will ask if you want to save the author, and you can either press 'y', 'n',
or wait ten seconds after which the program will finalize. However, you may want to change the ten seconds to 
sixty seconds if you want more time to evaluate whether the author is worth saving. Alternatively, if you are 
more interested in having a more sprightly tool, so you can make many queries at once, you can leave it as is.

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
* prose             :loomfinder prose -> randomly select an author
                    from a saved list when running with the prose parameter.

**Combining parameters:**

You can omit any parameter by not including it in the command.
For example, if you want to search only by genre and author, use:

loomfinder g:adventure a:Tolkien

**Listing genres and subjects:**

If you need a list of genres or subjects for inspiration, please type:

loomfinder --list-genres
loomfinder --list-subjects

---------------------------
November 30, 2024 v. 1.4.0

1. **Modifications to Archive.org Query URL**: Adjusted the query URL to fetch more results by modifying the parameter to `rows=1000&page=1`, giving us a better chance of getting relevant results and greatly increasing the rate of success.

2. **Added New Literature Genres**: Expanded the list of literature genres to include more options. However the non-fiction subjects outnumber the literature genres almost five times so I thought of a weighted random selection.

3. **Weighted Random Selection**: Implemented a weighted random selection giving literature genres an 80% chance more of being selected and other subjects a 20% chance. This rate can be changed any time, and genres and subjects added or removed.

4. **Saving Author Names**: Added functionality to prompt you to save the author's name to a text file at the end of each execution. The User can either change the name of the file or directory by modifying the code. However to not place the user in the position of having to necessarily make a choice I included a 10 sec. timer after which the terminal ends program.

5. **Handled Timeout for User Input**: Ensured the program correctly handles a 10-second timer for user input on whether to save the author's name.

6. **Fetching Authors from Saved List**: Implemented a flag to randomly select an author from the saved list when running with the `prose` parameter. (loomfinder prose)

7. **Included Saved Authors in Default Search**: Adjusted the default search to include saved authors. More chances in the future when many authors are added to the list. The User can add manually authors to the list if they wish.

8. **Debugging and Fixes**:
   - **Addressed Duplication and Placement Issues**: Ensured function definitions were outside of any `try` blocks and corrected duplicated definitions.
   
   - **Ensured Proper Execution Flow**: Fixed issues where the program continued executing additional queries after a valid result was fetched.

9. **Enhancements**:
   - **Allowing `yes/no` and `y/n` Inputs**: Updated the prompt to accept both full words (`yes`, `no`) and their shorter versions (`y`, `n`).

--------------------------
November 27, 2024 Updated help menu formatting and added more genres to the --list-genres menu for inspiration. Use loomfinder --list-genres or loomfinder --list-subjects to print lists and customize queries. Use t:title, g:genre, a:author, s:subject, and d:date to specify fields.

November 26, 2024 Final version of LoomFinder. Implemented three new features for better randomization: t:title, g:genre, x:anything, a:author, s:subject, d:date. Removed need for empty quotation marks. Added a help section (loomfinder --help) and set default language to English.

November 25, 2024 Resolved issues with year queries and search parameters. Changed program name from BookieMcRandom to ProsePicker+. Implemented null fields to avoid errors. Added features to handle date ranges and improved randomization. Next steps include implementing language and location criteria.

November 24, 2024 Summary
I created BookieMcRandom, soon to be renamed ProsePickerPlus. It randomly selects and displays text excerpts from over 28 million texts on Archive.orgdirectly to your terminal, allowing users to specify genre, author, and publication date to narrow down the randomization. This tool simplifies exploring Archive.orgdocuments, displaying book titles and authors after a snippet is shown.
