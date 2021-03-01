# Similarity Detection

In this project we created a tool that is able to detect phishing websites. It
takes a domain as input and now scans the internet for domains that look similar
to the given one. For that we use a process that is called `Typosquatting`.
If there really exist some of those websites the second component of the tool
comes in, the `Website Comparison Tool`. Now the target website that was given
is compared to the generated ones, found earlier. At the end the tool states a
similarity score how suspicious the compared website is. With our tool companies
can check for malicious websites, that try to impersonate them.

## Typosquatting
`TODO: Sasha`

## Website Comparison Tool
Given two URLs the tool will look at different features of the websites trying
to compare them. For each feature it calculates a similarity percentage which
are then used to set a score for the specific feature. The sum of all feature
scores is the final similarity score that states how suspicious a website looks
like.


### Features
- Content
    - remove HTML markup
    - Similarity Percentage: line overlaps on both websites

- Domain
    - remove common parts like [.de, .com, http, https, etc]
    - Similarity Percentage: word overlaps on both domains

- Links
    - collect all hrefs in both websites (html-tag: href)
    - loop through all of them to compare everyone to everyone
    - Similarity Percentage: average word overlaps

- Image-URLs
    - collect all image-links in both websites (html-tag: src)
    - loop through all links to compare everyone to everyone
    - Similarity Percentage: average word overlaps

- Images
    - create screenshot of both websites and compare them
    - use different metrics for comparing (MSE, SSIM, SIM)
      - ***MSE***: compare each pixel of the one image to the corresponding pixel
          of the other image
      - ***SSIM***: same as MSE but with bigger kernel size
      - ***SIM***: take difference of both images in embedding space

## Installation
- clone repository
- run `virtualenv -p python3 similarity-detection-tool` to create the virtual environment
- run `cd similarity-detection-tool && source bin/activate` to attach to the virtualenv
- run `chmod +x requirements/requirements.sh && sudo requirements/requirements.sh` to install required packages
- run `pip3 install -r requirements/requirements.txt` to install required python modules

## Usage

#### Command
`python3 main.py <domain>`
Note that the input must only be a domain name not the whole URL. That means that
you should use `google.com` instead of `https://google.com`

### Output
By default the tool will log the outcome of the comparing in the `logs` directory
in the specific domain directory. E.g. `logs/google.com`. With logging enabled it
will also create a `results.txt` containing all tested URLs and their similarity
scores.

## Documentation
The tool is split into three parts. First we have the Typosquatting that generates
new domains. Second there is the Website Comparison that compares the generated
domains with the given one. The `main.py` combines both parts.
Documentation:
  - [Main](https://github.com/Pilladian/similarity-detection-tool/blob/main/docs/main_file.md)
  - Typosquatting `TODO: Sasha`
  - [Website Comparison](https://github.com/Pilladian/similarity-detection-tool/blob/main/docs/Comparer_Class.md)
