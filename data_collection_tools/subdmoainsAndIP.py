# Python 3.9
import dns.resolver

# ~30 min for 100000 without requests
# takes an awfully long amount of time to get subdomains; need to improve this
def main(domain):
    dictonary(domain)

# finds domains based on pregiven txt file
def dictonary(domain):
    # open file and extract subdomains
    file = open("subdomains.txt")
    subdomains = file.read()
    subdomain = subdomains.splitlines()

    # goes through all dmoains and find matching ones based on error message
    for s in subdomain:
        # build the url
        url = s + "." + domain
        
        # if error -> no subdomain; else found subdomain with ip address/es
        try:
            result = dns.resolver.query(url, "A")
        except:
            pass
        else:
            for ipval in result:
                # for now it will print the data, eventually save it in a file or give a list back
                print(url, ipval.to_text())
