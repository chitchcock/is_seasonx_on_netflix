from netflix import NetflixAPI
import datetime

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

def find_season_link(n_api, show_id, season_to_find):
    #initialize the season found string to determine if we find it during our loop
    season_link_found = ''
    
    the_request_url = 'catalog/titles/series/{0}'.format(show_id)
    
    params = {'v': '2.0', 'expand': '@episodes'}               
    the_request = n_api.api_request(the_request_url, 'GET', params)

    if 'catalog_title' in the_request:
        if 'episodes' in the_request['catalog_title']:
            for episode_entry in the_request['catalog_title']['episodes']:
                if 'season_number' in episode_entry:
                    if episode_entry['season_number'] == season_to_find:
                        season_link_found = 'http://movies.netflix.com/WiMovie/{0}'.format(show_id)
                        break   
        else:
            print 'no episodes'
                                              
                                
    if season_link_found == '':                
        return 'no'
                
    else:
        return season_link_found
        
        
def build_output_html(the_season_text, the_season_link, output_html_path, output_html_template_path):

    output_html_template_file = open(output_html_template_path, 'r')
    output_html_template = output_html_template_file.read()
    output_html_file = open(output_html_path, 'w')
    output_html_text = output_html_template.format(season_url = the_season_link, 
                                                   season_result = the_season_text, 
                                                   date_updated = datetime.datetime.today())
    output_html_file.write(output_html_text)
    output_html_file.close()



n = NetflixAPI(api_key = api_key, api_secret = api_secret, callback_url = callback_url)

season_link = find_season_link(n, show_id, season_to_find)

if season_link == 'unknown':
    print 'Season can''t be found'
    build_output_html('UNKNOWN', '', output_html_path, output_html_template)
    
elif season_link == 'no':
    print 'Season not found'
    build_output_html('NO', '', output_html_path, output_html_template)
    
else:
    print 'Season {0} found - {1}'.format(season_to_find, season_link)
    build_output_html('YES', season_link, output_html_path, output_html_template)
                     
                    
