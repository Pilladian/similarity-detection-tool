# main.py

Function: `_help()`
- does not take arguments
- prints usage of tool
- returns 0 as it quits the program

Function: `main`
- calls `_help()` if amount of given arguments is not equal 1
- stores given target_domain
- queries target_url
- generates domains that could be malicious (`LINK TO URLGENERATOR GOES HERE`)
- compares given domain with generated ones (`LINK TO COMPARER GOES HERE`)
- if enabled: logs the output
- stores final results in `results.txt`
