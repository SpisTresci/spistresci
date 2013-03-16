#!/bin/sh
modules=${@:-unittests}
nosetests  $modules
