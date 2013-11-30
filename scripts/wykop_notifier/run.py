# -*- coding: utf-8 -*-
import wykop
import time
try: import simplejson as json
except ImportError: import json

class AttrDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

def _parse_json(data):
    result = json.loads(data, object_hook=lambda x: AttrDict(x))
    return result

def main():
    APPKEY=""
    SECRETKEY=""
    LOGIN = ''
    PASS = ''

    DRY_RUN = True

    data = {
        "service_count": "48",
        "book_count": "ponad 50 tys.",
        "free_ebook_count":"ok 10 tys",
        "raw_entry_link":"http://www.wykop.pl/link/1757346/tu-bedzie-link/"
    }

    api = wykop.WykopAPI(APPKEY, SECRETKEY)
    api.authenticate(LOGIN, password = PASS)

    with open("messages.json") as f:
        content = f.read()
        jsn = _parse_json(content)

        for item in jsn:
            for msg in item['msgs']:

                for key, val in data.items():
                    msg = msg.replace("{%s}"%key, val)

                if msg != item['msgs'][0]:
                    time.sleep(msg.count(' '))

                if not DRY_RUN:
                    api.send_message(item['nick'], msg)
                #else:
                #    api.send_message("lenka21", msg)

                print "%(login)s > %(nick)s: %(msg)s" % {"login":LOGIN, "nick": item['nick'], "msg":msg}

            print u'Użytkownik %s otrzymał wiadomość.\n' % item['nick']


    print u"Koniec wysyłania :)"


if __name__ == '__main__':
    main()
