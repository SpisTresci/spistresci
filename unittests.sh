#!/bin/sh
modules=${@:-unittests}
nosetests -s $modules
