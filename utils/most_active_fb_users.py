import json
import urllib2
from collections import Counter

token = 'BAACEdEose0cBAC4PM7TjBRLYd7hM15tmS4NbRnLZBjqORsQlND6WQlZBHK3vI0MWZBoMBiS13Bj8VZCeI0bhv92UaJEeMwCmYELll07SfFX2p4HnOWyapZAoSbwILZBNwPo8FeElQ50BaO2sp1UviPZBDfKy0CvXsVcptCbmAzzdVVXLY1Xw0ApJZCF3K32ECviPWLHT6iwykHHEl3ZCdtDHSi1qJvsiROx2N34VKpYp2ywZDZD'
fanpage_name = 'woblink'


def search():
  req = urllib2.urlopen('https://graph.facebook.com/' + fanpage_name + '/posts?access_token=' + token + "&type=post&limit=5000")
  res = json.loads(req.read())
  users = []

  for status in res['data']:
    if status.get('likes'):
        for person in status['likes']['data']:
            users.append(person['name'])

  count = Counter(users)
  for c in count.most_common():
      print c
  
  
if __name__ == '__main__':
  search()
