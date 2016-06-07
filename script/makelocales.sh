#!/bin/bash
# Regenerate locale files of all installed Django Apps.
# The change is revertet if only one line was changed in a file.
# This happens if the only change is the update of the Creation-Date.
# This script is part of pyOphase https://github.com/d120/pyophase
exitcode=0

set -e

rootdir=$( pwd | sed -e 's/pyophase.*//')'pyophase/'
dirstolook=$( find $rootdir -iname '*.po' )

for cdir in $dirstolook
do
  app=$( echo $cdir| sed -e 's/.*pyophase\///'| cut -d '/' -f1 )
  cd $rootdir$app
  echo "Compiling messages for $app"
  $rootdir/manage.py makemessages
  state=$( git diff --shortstat locale/en/LC_MESSAGES/django.po )
  if [ "$state" == " 1 file changed, 1 insertion(+), 1 deletion(-)" ]; then
    git checkout locale/en/LC_MESSAGES/django.po
  else
    exitcode=1
  fi
done

exit $exitcode
