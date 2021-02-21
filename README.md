# Website Comparer

In this project we created a tool for comparing websites based on different objectives.
Therefore, we implemented the following features

## Features
- Content
    - removed HTML markup
    - count line overlaps of both websites
    
- Domain
    - remove common parts like [.de, .com, http, https, etc]
    - count word overlaps of both domains
    
- Hrefs
    - collect all hrefs in both websites
    - loop through all hrefs to compare everyone to everyone
    - count word overlaps for them to calculate an average
  
- Image-URLs
    - collect all image-links in both websites
    - loop through all links to compare everyone to everyone
    - count word overlaps for them to calculate an average
    
- Images
    - create screenshot of both websites and compare them
    - use different metrics for comparing (MSE, SSIM, SIM)
    
## Typosquatting

To find cloned websites that are used for phishing, we also focused on typosquatting.
This is a procedure where similar looking letters are swapped in the url to cause the victim to think everything is correct.
We also collected some use-cases where the victim miss clicks on the keyboard. 
Furthermore, we wrote a script that is able to check if the website exists to perform a similarity check on them using the above described objectives.

## Installation
- clone repository
- run `chmod +x requirements.sh && sudo ./requirements.sh` to install required packages
- run `pip3 install -r requirements.txt` to install required python modules

## Usage

#### Command 
`python3 <url> <url> [-l | --log] [-s | --screen]`

#### Arguments
url : common url of type http://example.com or https://sub.example.com:1234

[ -l | --log ] : enables logging mode -> prints output and stores outcome to compare.log

[ -s | --screen ] : enables image comparing, since this is only usable on desktop machines

