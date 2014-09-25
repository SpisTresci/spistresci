#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/../..
behave spistresci/behave/features/search
behave spistresci/behave/features/home_page
