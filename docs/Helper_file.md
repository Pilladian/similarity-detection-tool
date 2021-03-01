# webcomp/Helper.py

Function: `crawl_website(url)`
- crawls given url
- removes html markup to only access content (lines of the website)
- returns empty list if an error occurs or the list of lines

Function: `remove_html(lines)`
- returns list of lines where all html markups have been removed

Function: `get_domain_components(url)`
- returns list of components of the domain
- common parts are removed to avoid similarity

Function: `get_image_components(url)`
- returns list of components of the image source

Function: `get_percentage_similarity(l1, l2)`
- returns percentage of similarity of the two given lists

Function: `get_hrefs(url)`
- crawls given url
- extracts hrefs
- returns empty list if an error occurs or the list of hrefs

Function: `get_image_urls(url)`
- crawls given url
- extracts image src
- returns empty list if an error occurs or the list of sources

Function: `create_screenshots(urls)`
- uses headless chrome-driver to create a screenhot of the given websites
- stores them temporally for comparing

Function: `mse(img1, img2)`
- compares both images pixel by pixel
- returns similarity percentage

Function: `sim(path1, path2)`
- compares both images by calculating the distance in the embedded space
- returns similarity percentage

Function: `scale(i1, i2)`
- scales i2 to fit i1
- returns both images that are not of the same shape

Function: `calculate_points(percentage, threshold, max_points, percentage_steps)`
- percentage is the current similarity percentage of the test
- threshold is the baseline for the test
- max_points are the maximum amount of points a website can score for this test
- percentage_steps is the step size for calculating partial points
- returns calculated points for specific test

Function: `decode(cont)`
- cont is the content of a html website that has been crawled
- returns decoded website
