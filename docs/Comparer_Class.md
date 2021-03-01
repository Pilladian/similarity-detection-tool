# webcomp/Comparer.py

Method: `__init__(self)`
- initializes new instance of class Comparer
- logging is disabled by default

Method: `disable_logging(self)`
- disables logging

Method: `enable_logging(self, p)`
- p represents the path were the log files will be stored

Method: `set_parameter(self, url1, url2)`
- prepare instance for comparing url1 and url2

Method: `log(self, similarity_values, similarity_points, thresholds)`
- similarity_values are the percentages of each test
- similarity_points are the corresponding points this percentage scores
- thresholds are the baseline values
- stores information in `<logging_path>/<domain_name>.log`

Method: `compare_websites(self)`
- compares set url1 and url2
  - content
  - domains
  - links
  - image sources
  - website screenshots
- calculates final similarity score

Function: `_compare_content(url1, url2)`
- returns similarity percentage for content

Function: `_compare_domains(url1, url2)`
- returns similarity percentage for domains

Function: `_compare_links(url1, url2)`
- returns similarity percentage for links

Function: `_compare_image_sources(url1, url2)`
- returns average similarity percentage for content

Function: `_compare_screenshots(url1, url2)`
- uses three different measurements for difference / similarity
- returns average similarity percentage for content
