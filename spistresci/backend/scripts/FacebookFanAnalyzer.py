# -*- coding: utf-8 -*-
import json
import urllib2
import sys
from collections import Counter
reload(sys)
sys.setdefaultencoding('utf8')
###############################################################
###############################################################
#### PLEASE PASTE HERE YOUR TOKEN, YOU CAN GENERETE IT ON:
####    https://developers.facebook.com/tools/explorer
#### GENERETE AND PASTE NEW ONE, WHEN THIS WILL STOP WORKING

token = 'BAACEdEose0cBAEo2zZAbNx5ukN27SfclWyuNd9DxCtRY7ktam1vzNL3Fbt0gCbZCRrbjoB7AFNZAec9cYuVWag28arVI6oh5cLL2JqLXQgZCZAD48gs7R'

attrib_limit = 50
post_limit = 50
###############################################################
###############################################################


class FacebookFanAnalyzer(object):

    def __init__(self, fanpage_name, post_limit, attribs, attrib_limit):
        self.fanpage_name = fanpage_name
        self.post_limit = post_limit
        self.attribs = attribs
        self.attrib_limit = attrib_limit
        self.data={}

    def make_request(self, attrib):
        global token
        url = 'https://graph.facebook.com/' + self.fanpage_name + '/posts?limit=' + str(self.post_limit) + '&fields=' + attrib + '.limit('+str(self.attrib_limit)+')&access_token=' + token
        print "Requesting '" + attrib + "' data: " + url
        req = urllib2.urlopen(url)
        res = json.loads(req.read())

        if res.get('error'):
            print res['error']
            exit()

        return res

    def grep_data(self, attrib):
        res=self.make_request(attrib)
        lst=[]
        for status in res['data']:
            if status.get(attrib):
                for person in status[attrib]['data']:
                    if attrib == 'likes':
                        lst.append(person['name'])
                    elif attrib == 'comments':
                        lst.append(person['from']['name'])
        return lst


    def save_as_html(self, attribs):
        filename = self.fanpage_name + '.html'
        f = open(filename, 'w') 

        f.write(u'<html><head></head><body>')
        f.write(u'<table border="0"><tr>')
        for attrib in attribs:
            f.write(u'<td>'+attrib+'</td>')
        f.write(u'</tr>')

        for attrib in attribs:
            f.write(u'<td valign="top"><table border="1">')

            for d in self.data[attrib]:
                f.write(u'<tr><td>' + unicode(d[0]) + u'</td><td>' +unicode(d[1]) + u'</td></tr>')

            f.write(u'</table></td>')

        f.write(u'</tr></table>')
        f.write(u'</body>')
        f.close()
        print "Saved to " + filename

    def fetch_data(self, attribs):
        for attrib in attribs:
            self.data[attrib]=Counter(self.grep_data(attrib)).most_common()

def main():
    global post_limit
    global attrib_limit

    fanpage_name = sys.argv[1] 
    attribs = sys.argv[2:] 

    f = FacebookFanAnalyzer(fanpage_name, post_limit, attribs, attrib_limit)
    f.fetch_data(attribs)
    f.save_as_html(attribs)

if __name__ == '__main__':
    main()
