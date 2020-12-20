# Python 3.9
import dns.resolver

def main(domain)
    # if error -> no subdomain; else found subdomain with ip address/es
    try:
        # dns looup for ipv4
        result = dns.resolver.query(domain, "A")
    except:
        # if not found return false
        return False
    else:
        # if lookup workes return True
        return True
