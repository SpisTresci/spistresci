try:
  from collections import OrderedDict
except ImportError:
  from utils.compatibility import OrderedDict

try:
    import json
except ImportError:
    import simplejson as json
