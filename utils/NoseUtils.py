import nose

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

