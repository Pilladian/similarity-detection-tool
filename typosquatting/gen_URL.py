# Python 3.9
import re
import dns.resolver


def search(domain):
    # if error -> no subdomain; else found subdomain with ip address/es
    try:
        # dns lookup for ipv4
        result = dns.resolver.resolve(domain, "A")
    except:
        # if not found return false
        return False
    else:
        # if lookup workes return True
        return True


# generates for now just one typo
def main(domain):
    # remove tld and extract characters
    domain_split = re.split("\.", domain)
    domainWithoutTLD = domain_split.pop(0)
    tld = "." + domain_split[0]
    characters_domain = list(domainWithoutTLD)
    
    # save to this list all typosquatting domains
    urls = []
    
    # generate domains with hijacking.txt:
    # open file hijacking.txt
    hijacking = open("typosquatting/hijacking.txt", "r")
    read = hijacking.read()
    # split the file by new lines and get rude of first line with the comment
    newline = re.split("\n", read)
    newline.pop(0)
    
    # go into the characters from the domain and check against the hijacking lines & find in the line one character
    for n in range(0, len(characters_domain)):
        for i in range(0, len(newline)):
            x = newline[i].find(characters_domain[n])
            # found one; -1 then none found
            if x >= 0:
                # get the line and separate the characters
                replace = newline[i]
                replace = re.split(",", replace)
                # go through the characters and find different then original; then replace and append to urls
                for g in range(0, len(replace)):
                    if replace[g] != characters_domain[n]:
                        temp_list = characters_domain.copy()
                        temp_list[n] = replace[g]
                        temp_list = [''.join(temp_list[::])]
                        urls.append(temp_list)
                        
    # generate domains with miss_click.txt:
    # open file miss_click.txt
    miss_click = open("typosquatting/miss_click.txt", "r")
    read = miss_click.read()
    # split the file by new lines and get rude of first line with the comment
    newline = re.split("\n", read)
    newline.pop(0)
        
    # go into the characters from the domain and check against the hijacking lines & find in the line one character
    for n in range(0, len(characters_domain)):
        for i in range(0, len(newline)):
            x = newline[i].find(characters_domain[n])
            # found one; -1 then none found
            if x == 0:
                # get the line and separate the characters
                replace = newline[i]
                replace = re.split(",", replace)
                # go through the characters and find different then original; then replace and append to urls
                for g in range(0, len(replace)):
                    if replace[g] != characters_domain[n]:
                        temp_list = characters_domain.copy()
                        temp_list[n] = replace[g]
                        temp_list = [''.join(temp_list[::])]
                        urls.append(temp_list)
                        
    # generate with all the tlds and generated urls full urls
    urls_with_tld = []
    
    # open file common_tld.txt
    common_tld = open("typosquatting/common_tld.txt", "r")
    read = common_tld.read()
    # split the file by new lines and get rude of first line with the comment
    newline = re.split("\n", read)
    newline.pop(0)
    
    # check if original tld is in common tlds
    if read.find(tld) == -1:
        newline.append(tld)
    
    # generate the domains
    for domains in urls:
        for tld in newline:
            urls_with_tld.append(domains[0] + tld)
    
    # check if the domain exists
    actual_domains = []
    for domain in urls_with_tld:
        if search(domain):
            actual_domains.append(domain)
    
    return actual_domains
