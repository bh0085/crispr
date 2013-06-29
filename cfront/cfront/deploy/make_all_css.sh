#!/usr/bin/env bash

set -eux
cd "`dirname $0`" 
echo "Compiling .less"
../public/compile-less.sh
echo "Done compiling less, switched back to" `pwd`.
echo
echo "All done!"
echo
exit 0