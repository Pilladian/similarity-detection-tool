# Python 3.9
import dns.resolver

# ~30 min for 100000 without actuall dns requests
# takes an awfully long amount of time to get subdomains; need to improve this
def main(domain, extended_or_not):
    dic = dictonary(domain, extended_or_not)
    return dic
    
# finds domains based on pregiven txt file
def dictonary(domain, extended_or_not):
    # open file and extract subdomains
    # for extended version take the bigger file, else just 1000 file
    if extended_or_not:
        file = open("subdomains.txt")
    else:
        file = open("short_subdomains.txt")
    subdomains = file.read()
    subdomain = subdomains.splitlines()

    # create two lists (later zip them), one for url and one for ipv4
    url_list = []
    ipv4_list = []
    # goes through all domains in txt file and finds matches based on error message
    for s in subdomain:
        # build the url
        url = s + "." + domain
        
        # if error -> no subdomain; else found subdomain with ip address/es
        try:
            # here a for ipv6
            result = dns.resolver.query(url, "A")
        except:
            pass
        else:
            for ipval in result:
                # creates a list with (url, a record)
                url_list.append(url)
                ipv4_list.append(ipval.to_text())
    
    
    # getting the the ipv6 address
    # create list to save records
    ipv6_list = []
    for x in range(len(url_list)):
        try:
            # here: change to AAAA -> ipv6
            result = dns.resolver.query(url_list[x], "AAAA")
        except:
            # if error raises none ipv6 address found -> so append a none
            ipv6_list.append(None)
        else:
            for ipval in result:
                    # result found and append to list
                ipv6_list.append(ipval.to_text())
    
    # put together into one list
    alltogether = zip(url_list, ipv4_list, ipv6_list)
    return alltogether
