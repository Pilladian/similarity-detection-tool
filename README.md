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
    - use different metrics for comparing (MSE, SSIM, SIM)
    - `TODO` collect images and compare them
    - `TODO` take screenshot of websites and compare them
    - `TODO` combine `compare_image.py` and `compare_html.py`
    
## Typosquatting

To find cloned websites that are used for phishing, we also focused on typosquatting.
This is a procedure where similar looking letters are swapped in the url to cause the victim to think everything is correct.
We also collected some use-cases where the victim miss clicks on the keyboard. 
Furthermore, we wrote a script that is able to check if the website exists to perform a similarity check on them using the above described objectives.


