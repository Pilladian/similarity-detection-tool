# Documentation
Generally all informations in the URLGenerator.py about a function can be looked up with with the following command: `print(<function_name>.__doc__)`. This will explain what each value of a function is for and what the function will return.

## Change data:
### 1.1 Adding a new file for replacing the characters in the domain:
1. Add the new file in typosquatting folder.
2. Add the data to the file. The first line is reserved for a comment. If you put there some data it will be purged. When putting the characters in a line be aware of the format; no spaces and separated by a comma. E.g this works: `a,b,c`. E.g these do not work: `a, c, b` or `a,b,c,` or `a,b,c⎵`.
3. Add the following two line to the URLGenerator.py after line **108**:<br />
`new_data = self.open_file('<Name of the txt file in the folder>')`<br />
`temp_url = self.generator(<Flag_A>, <Flag_B>, characters_domain, data, <iteration>, 0)` <br />
`final_urls.extend(temp_url)` 
	* 	`Flag_A`: Is set when the function should find a character in the **entire line** of the data and then start replacing by the other characters in the line 
	*	`Flag_B`: Is set when **only the first character** from the data line is equal and then it will start replacing by the other characters in the line
	* `iteration`: Is the number of iteration it should do after the first replacement is finished. When all the function should iterate over all characters then set this value to -1.

### 1.2 Add or delete data from txt files in typosquatting folder:
* For typo.txt:
	* Newline: When a new line is added, the generator function will try to find a match for **only** the first character of the new line and then start replacing the character of the match found in the domain by all the other character in the line where it found it.
	* Adding to an existing line: When the first character from the line is equal to the character from the domain it will be replaced by the other character of the line including the newly added one. So it matter where you put the new character. If you put it on first position this is the character that will be compared and and everything after that will be replaced.
* For similar.txt and similar_sound.txt:
	* Newline: When adding a new line then **all** character you add, will be checked to the characters of the domain and then replaced by all of the others character in the added new line.
	* Adding to an existing line: When adding one or several new characters to an already existing line, then in the generator function it will compare for this new character, as well replace it when finding another character from the line.
* For the commen_tld.txt: Adding data works by adding a new line and then adding the new tld with a dot in front of it. E.g. ".net". Deleting a tdl works by just deleting the line (including the newline) where the tld is in.

## Increase typos:

Can be changed via the command input values. If you want as many typo-domain generations as possible set the value to -2.


# Making sense of the functions:

* `search(self, domain)`: For checking if a domain exists or not it will be done via a dns lookup. This is a simple but still one of the fastest solution and a process that is done almost every time a domain is accessed. E.g. when accessing a domains via a http requests then it would need to do anyways the dns lookup, so we can cut all the other useless traffic and choose the first one in the process in finding a domain anyway. The functions looks up addresses for ipv4 addresses which is the most dominant ip version. Even most times when ipv6 is implemented a support for ipv4 is still there. If over the course of time this assumption changes or ipv6 is needed for some other reason this can be done by exchanging the following line `result = dns.resolver.resolve(domain, "A")` to `result = dns.resolver.resolve(domain, "AAAA")`(here AAAA is the record for ipv6). It would be even more time consuming to check for ipv4 and ipv6 (roughly doubling the time, since two requests for every single domain), so only the more dominant ip versions was chosen.

* `generator(self, flag_a, flag_b, characters_domain, data, iteration, next)`: This extra function is especially important for several typos functionality/similar domain generation, since this is done recursively.

* `open_file(self, file_name)`: This function was created for making the same process of opening a file more attractive and easy in the code. Also when future files for more domain generations will be added this function makes it easier to only add a single line instead of four.

* `generate(self, domain, typo_mistakes)`: This is more or less the main function of the URLGenerator.py. From here everything will start. Call all the other functions and eventually return the generated URLs that have a dns record.

# Improvements & Ideas for the future: 
Even tough the domain is checked via a dns lookup the program still takes a large amount of time for figuring out the domains(as can be seen in the evaluation). Considering the timing of this project it was not able to implement a better function for that. The probably easiest solution would be trying to thread the dns lookup or even faster via asynchronous dns resolver.<br />
Future work can also concentrate on different typosquatting mistakes. This project only touches the idea of mistakes based on similar sounding letters. This would require a deepen knowledge in language science. Also like missing a letter (e.g. instead of google.com googl.com), adding an addition letter (e.g. instead of google.com gooogle.com) or exchanging two letters (e.g. instead of instagram.com intsagram.com) could be another interesting field to explore. Another typosquatting idea would be to consider commonly mistakes people make, like "fair" and "fare" or "forth" and "fourth". In addition to that the project focuses mainly on the english language and the english keyboard. Here can be another approach to generate even more domains. Generally here needs to be taken in account if it is worth the effort to generate all these additional domains. <br />
In addition to the similar looking domains, which is implemented, another approach could be appending some word to a domain (e.g. instead of finance.com thefinance.com) also known as "Combosquatting", a "Doppelganger Domain", where the dot of the subdomain is missing (e.g. instead of cloud.example.com to cloudexample.com) or adding in a domain a dot (e.g. instead of facebook.com face.book.com).	
