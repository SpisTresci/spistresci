#!/bin/sh
modules=${@:-unittests}
nosetests -v  $modules
