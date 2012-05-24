from python_netflix.netflix import NetflixAPI
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
    season_id_found = ''
    
    the_request_url = 'catalog/titles/series/{0}/seasons'.format(show_id)
    
    print the_request_url
                   
    the_request = n_api.api_request(the_request_url, 'GET', None, 'json', False)
    
    if 'catalog_titles' in the_request:
        if 'catalog_title' in the_request['catalog_titles']:
            for catalog_entry in the_request['catalog_titles']['catalog_title']:
                season_name = catalog_entry['title']['regular']
                
                if season_name.endswith('Season {0}'.format(season_to_find)) or season_name.endswith('Series {0}'.format(season_to_find)):           
                    season_id_found = catalog_entry['id']
                                
            if season_id_found == '':                
                return 'no'
                
            else:
                the_season_request = n_api.api_request(season_id_found, 'GET', None, 'json', False)
                the_season_links = the_season_request['catalog_title']['link']
                the_season_link = 'http://www.netflix.com'
                    
                for link in the_season_links:
                    if link['title'] == 'web page':
                        the_season_link = link['href']            
                
                
                return the_season_link
                
        else:
            return 'unknown'    
                    
    else:
        return 'unknown'
        
        
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
    print 'Season found'
    build_output_html('YES', season_link, output_html_path, output_html_template)
                     
                    
