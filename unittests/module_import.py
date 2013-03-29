import nose
import sys
import inspect

from utils import NoseUtils



#Tests if all our modules provides correct api to import from it

class TestModuleImport():

    def assertModuleMember(self, module, member):
        for (name, obj) in inspect.getmembers(module):
                if name == member:
                    assert True
                    break
        else:
            assert False, '%s missing in module %s' % (member, module)

    @NoseUtils.skipBecause('''This was test to check if everything was correct after old refactor. 
    It is not necessary after new refactor (T168). 
    However I strongly recommend writing new version of this tests checking if all imports works correct now''')
    def test_wolnelektury(self):
        import wolnelektury 
        self.assertModuleMember(wolnelektury,'fetch')

    @NoseUtils.skip
    def test_Virtualo(self):
        import virtualo
        self.assertModuleMember(virtualo, 'Virtualo')
        self.assertModuleMember(virtualo.Virtualo, 'fetchData')
        self.assertModuleMember(virtualo.Virtualo, 'parse')

    @NoseUtils.skip
    def test_Nexto(self):
        import nexto
        self.assertModuleMember(nexto, 'Nexto')
        self.assertModuleMember(nexto.Nexto, 'fetchData')
        self.assertModuleMember(nexto.Nexto, 'parse')

    @NoseUtils.skip
    def test_Koobe(self):
        import koobe
        self.assertModuleMember(koobe, 'Koobe')
        self.assertModuleMember(koobe.Koobe, 'fetchData')
        self.assertModuleMember(koobe.Koobe, 'parse')

    @NoseUtils.skip
    def test_DobryEbook(self):
        import dobryebook
        self.assertModuleMember(dobryebook, 'DobryEbook')
        self.assertModuleMember(dobryebook.DobryEbook, 'fetchData')
        self.assertModuleMember(dobryebook.DobryEbook, 'parse')

    @NoseUtils.skip
    def test_Helion(self):
        import helion
        self.assertModuleMember(helion, 'Helion')
        self.assertModuleMember(helion.Helion, 'fetchData')
        self.assertModuleMember(helion.Helion, 'parse')

    @NoseUtils.skip
    def test_generic(self):
        import generic
        self.assertModuleMember(generic,'GenericConnector')
        self.assertModuleMember(generic,'XMLConnector')

