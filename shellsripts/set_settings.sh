#!/bin/bash

#### Print total arguments and their values
#echo "Total Arguments:" $#
#echo "All Arguments values:" $@
#
#### Command arguments can be accessed as
#echo "First->"  $1
#echo "Second->" $2
#
## You can also access all arguments in an array and use them in a script.
#args=("$@")
#echo "First->"  ${args[0]}
#echo "Second->" ${args[1]}

shopt -s extglob

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  case $1 in
  [Dd]ev*)
    sed -i 's/config.settings.prod/config.settings.dev/' ../manage.py
#    cat ../requirements/dev.txt
  ;;
  [Pp]rod*)
    sed -i 's/config.settings.dev/config.settings.prod/' ../manage.py
#    cat ../requirements/prod.txt
  ;;
  esac
elif [[ "$OSTYPE" == "darwin"* ]]; then
  case $1 in
    [Dd]ev*)
      sed -i "" 's/config.settings.prod/config.settings.dev/' ../manage.py
  #    cat ../requirements/dev.txt
    ;;
    [Pp]rod*)
      sed -i "" 's/config.settings.dev/config.settings.prod/' ../manage.py
  #    cat ../requirements/prod.txt
    ;;
  esac
fi