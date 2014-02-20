is_seasonx_on_netflix
=====================

# Introduction
A script to that uses the Netflix API to determine if a particular season of a particular show is available for streaming

# Setup
The script uses [python-netflix](https://github.com/michaelhelmick/python-netflix), which in turn needs requests.  You can install both via pop:
  pip install requests==0.13.0
  pip install python-netflix
  
As noted in the script, the script expects two different scripts containing the variables needed to run the script:

```
# Keep 'netflix_api_settings.py' in the same directory as this
# script. It should the information needed to authenticate with
# the netflix API -- like the following:
# api_key='some_key',
# api_secret='some_secret',
# callback_url='http://www.isbreakingbadseason4onnetflix.com/'
from netflix_api_settings import api_key, api_secret, callback_url

# Keep 'local_settings.py' in the same directory as this
# script. It should contain information to control the show to look
# up and how to build the output -- like the following:
#show_id = '70143836'
#season_to_find = 4
#output_html_path = 'status.html'
#output_html_template = 'html/template.html'
from local_settings import show_id, season_to_find, output_html_path, output_html_template
```

(Insert description of these variables)

# Using the Script
