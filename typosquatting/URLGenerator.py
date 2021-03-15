# Python 3.9
import re
import dns.resolver


class Generator:

    def __init__(self):
        self.path = 'typosquatting/'

    def search(self, domain):
        '''
        Finds for a given domain if a dns lookup is successful.
        Returns True if it found one; Return False if it couldn't find one.
        '''
        # if error -> no domain; else found subdomain with ip address/es
        try:
            # dns lookup for ipv4
            result = dns.resolver.resolve(domain, "A")
        except:
            # if not found return false
            return False
        else:
            # if lookup works return True
            return True

    def generator(self, flag_a, flag_b, characters_domain, data, iteration, next):
        '''
        flag_a: set when finding a character in the entire line
        flag_b: set when only the first character from the data line is needed
        character_domain: domain where character should be exchanged
        data: the data with what it should be changed
        iteration: either select how many iteration the function should do or -1 for as many as possible
        next: at what point the character_domain should start replacing the characters with the data
        returns the generated urls
        '''
        if (flag_a == 0 and flag_b == 0) or (flag_a == 1 and flag_b == 1):
            raise Exception("No flag or both in generator() are set. Need to set flags correctly. See generator.__doc__ for more info.")
        
        urls = []
        # go into the characters from the given domain and check against the data lines
        for n in range(next, len(characters_domain)):
            for i in range(0, len(data)):
                x = data[i].find(characters_domain[n])
                # found one; -1 then none found
                if (flag_a and x >= 0) or (flag_b and x == 0):
                    # get the line from the data and separate the characters
                    replace = data[i]
                    replace = re.split(",", replace)
                    # go through the characters and find different then original; then replace and append to urls
                    for g in range(0, len(replace)):
                        if replace[g] != characters_domain[n]:
                            temp_list = characters_domain.copy()
                            temp_list[n] = replace[g]
                            temp_url = []
                            if iteration > 0:
                                temp_url = self.generator(flag_a, flag_b, temp_list, data, iteration-1, n+1)
                            elif iteration  == -1:
                                iteration = len(temp_list) - n
                                temp_url = self.generator(flag_a, flag_b, temp_list, data, iteration, n+1)
                            temp_list = [''.join(temp_list[::])]
                            urls.extend(temp_list)
                            urls.extend(temp_url)
        return urls
    
    def open_file(self, file_name):
        '''
        file_name: the file name of the file that should be opened; the file needs to be in the typosquatting folder
        opens the file; deletes the first line for the comment; separates the file by newlines
        returns the data in a list separated by newlines
        '''
        # open file_name
        hijacking = open(f'{self.path}'+file_name, "r")
        read = hijacking.read()
        # split the file by new lines and get rude of first line with the comment
        newline = re.split("\n", read)
        newline.pop(0)
        
        return newline

    def generate(self, domain, typo_mistakes):
        '''
        given a domain finds typosquatting domains or similar looking domains via a dns lookup
        domain: full domain with tld e.g. example.com
        typo_mistakes: for how many mistakes it should generate domains
        returns a list with the domains it found
        '''
        # remove tld and extract characters
        domain_split = re.split("\.", domain)
        domainWithoutTLD = domain_split.pop(0)
        tld = "." + domain_split[0]
        characters_domain = list(domainWithoutTLD)
        #-----------------------------------------------------------------------------
        # generate second-level domain with similar.txt:
        data_hijacking = self.open_file('similar.txt')
        final_urls = self.generator(True, False, characters_domain, data_hijacking, -1, 0)
        
        #-----------------------------------------------------------------------------
        # generate second-level domain with typo.txt:
        data_miss_click = self.open_file('typo.txt')
        temp_url = self.generator(False, True, characters_domain, data_miss_click, typo_mistakes-1, 0)
        final_urls.extend(temp_url)
        
        #-----------------------------------------------------------------------------
        # generate second-level domain with similar_sound.txt:
        data_similar_sound = self.open_file('similar_sound.txt')
        temp_url = self.generator(True, False, characters_domain, data_similar_sound, -1, 0)
        final_urls.extend(temp_url)
        
        #------------------------------------------------------------------------------
        # generate with all the tlds and second-level domain full urls
        urls_with_tld = []

        # open file common_tld.txt
        common_tld = open(f'{self.path}common_tld.txt', "r")
        read = common_tld.read()
        # split the file by new lines and get rude of first line with the comment
        data_tld = re.split("\n", read)
        data_tld.pop(0)
      
        # check if original tld is in data_tld
        if read.find(tld) == -1:
            data_tld.extend(tld)
        
        # generate the url
        for domains in final_urls:
            for tld in data_tld:
                urls_with_tld.append(domains + tld)
        # check if the url exists
        actual_domains = []
        for domain in urls_with_tld:
            if self.search(domain):
                actual_domains.append(domain)
                
        return actual_domains
