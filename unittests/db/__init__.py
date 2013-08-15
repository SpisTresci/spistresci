from sqlwrapper import SqlWrapper


def setup_package(package):
    pass

def teardown_package(package):
    SqlWrapper.getBroadEngine().execute("DROP DATABASE st_unittests")