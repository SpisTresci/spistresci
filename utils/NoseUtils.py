import nose
import urllib2
import Rpdb

class debug(Rpdb.debug):
    def __call__(self, test):
        def wrapped(*args, **kwargs):
            Rpdb.debug._break(self.remote, self.unencrypted)
            test(*args, **kwargs)
        return nose.tools.make_decorator(test)(wrapped)

def skip(test):
    def newtest(*args, **kwargs):
        print 'Skipping test %s' % test.__name__
        raise nose.SkipTest
    newtest = nose.tools.make_decorator(test)(newtest)
    return newtest

def skipBecause(reason=''):
    def decorate(test):
        def newtest(*args, **kwargs):
            print 'Skipping test %s, reason: %s' % (test.__name__, reason)
            raise nose.SkipTest(reason)
        newtest = nose.tools.make_decorator(test)(newtest)
        return newtest
    return decorate

def skipIf(condition=True, reason=''):
    def decorate(test):
        def newtest(*args, **kwargs):
            if condition:
                print 'Skipping test %s, reason: %s' % (test.__name__, reason)
                raise nose.SkipTest(reason)
            else:
                test(*args, **kwargs)
        newtest = nose.tools.make_decorator(test)(newtest)
        return newtest
    return decorate


g_network_available = True
g_network_set = False

def network_available_for_tests():
    global g_network_set
    global g_network_available
    if g_network_set:
        return g_network_available
    try:
        urllib2.urlopen('http://www.google.com')
    except urllib2.URLError:
        g_network_available = False
    else:
        g_network_available = True
    finally:
        g_network_set = True
    return g_network_available



def neq_(a, b, msg=None):
    """Shorthand for 'assert a == b, "%r != %r" % (a, b)
    """
    assert a != b, msg or "%r == %r" % (a, b)
