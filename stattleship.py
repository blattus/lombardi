'''

stattleship.py

Taken from python v3 branch of the stattleship python SDK, which is provided under the MIT license
Code: https://github.com/stattleship/stattleship-python/blob/Stattleship-python(v3)/stattlepy/Stattleship_API.py
Source License: https://github.com/stattleship/stattleship-python/blob/master/LICENSE

'''

import requests
import json

class Stattleship(object):
        
        # function to set the token
        def set_token(self, pro_token):        
                if pro_token is None or not isinstance(pro_token,str):
                         warnings.warn('Stattleship API token must be provided in order to access the Stattleship API.')
                else:
                        global token
                        token = pro_token
                
        ### function to get the results for them Stattleship API
        def ss_get_results(self,**kwargs):

                # initial defaults for all variables
                sport = "hockey"
                league = "nhl"
                ep = "teams"
                query = list()
                version = 1
                walk = False
                page = 1
                verbose = True
                param = {}
                
                # loop through inputs and 
                for key, value in kwargs.items():
                        if str(key) == 'sport':
                                sport = value
                        elif str(key) == 'league':
                                league = value
                        elif str(key) == 'ep':
                                ep = value
                        elif str(key) == 'version':
                                version = value
                        elif str(key) == 'walk':
                                walk = value
                        elif str(key) == 'page':
                                page = value 
                        elif str(key) == 'verbose':
                                verbose = value
                        else:
                                param[key] = value
                
                
                if(verbose):
                    print('Making Initial API Request')
                    
                ###NOTE WALK IS NOT YET SUPPORTED
                        
                tmp = self.query_api(sport, league, ep, param, version, walk, page, verbose, token )
               
                response = list()
               
                response.append(tmp)       
               
                return(response)
            
        def query_api(self, sport, league, ep, param, version, walk, page, verbose, token):
        
                ### make sure that the sport, league and ep are all lower case
                sport = sport.lower()
                league = league.lower()
                ep = ep.lower()        
                
                url = 'https://api.stattleship.com/%s/%s/%s' % (sport, league, ep)
                
                if page >= 1 and isinstance(page, int):
                        param['page'] = page
                
                headers = {
                        'Authorization': 'Token token=%s' %token,
                        'Accept':'application/vnd.stattleship.com; version=%s' %version,
                        'Content-Type':'application/json'        
                }
                
                res = requests.get(url,params=param, headers = headers)
                
                print(res)
                print(res.url)
                
                content = res.json()
                
                return(content)
        
        
