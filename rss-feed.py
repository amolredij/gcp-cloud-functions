def get_feed(request):
    """
    Simple cloud functions pass through proxy to allow CORS reqeust from localhost
    basic template taken from https://cloud.google.com/functions/docs/writing/http
    pass RSS URL in qury param ?url=rss feed url
    returns 200 for valid RSS URL, 400 for bad URLs or 
    the http status as returned by the RSS feed URL

    https://github.com/amolredij/gcp-cloud-functions

    """
    # For more information about CORS and CORS preflight requests, see
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request
    # for more information.

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/rss+xml'
    }
    
    import requests
    
    # check if URL is passed otherwise use default        
    req_args = request.args
    if req_args and 'url' in req_args:
        rss_url = req_args['url']
    else:
        # Some default RSS Feed
        rss_url = 'http://feeds.feedburner.com/autonews/BreakingNews' 

    #get rss feed data
    r_headers = {'accept': 'application/rss+xml'}
    try:
        r = requests.get(rss_url,headers=r_headers)
    except:
        return ('Invalid URL, URL = '+ rss_url,400, headers)

    #return ('Goodbye Cruel World!*** TYPE** ' + r.headers['Content-Type'] + '** conent **' + str(r.content), 200, headers)
    if str(r.status_code) == '200' and ('RSS' in r.headers['Content-Type'].upper() or 'XML' in r.headers['Content-Type'].upper()) :
        return (r.content, 200, headers)
    elif str(r.status_code) == '200':
        return ('Not an RSS feed, Content type = ' + r.headers['Content-Type'], 400, headers)
    else:
        return ('Unexpected error - reponse ' + str(r.status_code),r.status_code, headers)

    
