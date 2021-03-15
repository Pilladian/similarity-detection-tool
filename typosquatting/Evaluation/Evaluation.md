# Evaluation
For the evaluation there will be six measuring points for a domain: 

* the length of the generated domains after the similar generation
* the length of the generated domains after the typo generation
* the length of the generated domains after the similar sounding generation
* the length of the generated domains after appending all the different TLDs
* the length of the generated domains after the DNS check
* the time the DNS lookup takes for the fully generated URL

For the evaluation the following domains where taken:
sr.de,
vk.com,
zdf.de,
ard.de,
zoom.us,
live.com,
bing.com,
ebay.com,
google.com and
amazon.de
</br >For every length from two to six character at least one domain is taken.

Notes for evaluation:
*Before every DNS lookup the cache was cleared locally and the DNS server 1.1.1.1 and 1.0.0.1 where taken.*

## Results

![pdf](domains.pdf)

![pdf](time.pdf)

![pdf](typo.pdf)

## Takeaways
For now the DNS lookup time is quite high (see chart 2.1). In addition to that the lookup time for roughly the same amount of domains differs(e.g. ard.de and zdf.de). Since the cache was cleared locally, this could be due to a cache by the DNS server itself or other components. </br >
Also the generated domains varies a lot. Especially this can be seen with the four character long domains in chart 1.2. Furthermore it can not be said that a domain with a higher character number has also a lot more generated domains. This depends a lot by the characters itself. A domain with a lot of matches in similar sound file and similar file will have more generated domains than one without. This can be seen in chart 1.2.</br >
Another aspect that needs a closer look is the typosquatting miss typing number. Here the generated domains with two typos are almost four times higher than the one with one typo(see chart 3.1). So it needs  to be considered  how useful it is to increase the number of the miss clicks, since  the probability of a victim miss clicking  more than once are probably quite low. Probably it will lower each time a typo increases.</br >
More over from the generated domains to the domains with a TLD the number increases a lot. This is due to the fact that when combining the TLDs with the generated domains the number for this is given by multiplying the TLDs and domains. So only removing one TLD will result for example for google.com 205 less domains. So maybe it makes sense to reduce for certain situations the TLDs. For example for a domain that is from Germany (TLD is .de) it could make sense to remove other countries TLDs, since probably the chance for a person accidentally typing .ru or .jp are lower than for .net or .com.