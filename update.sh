#!/bin/sh

cd lac 
python3 lac_html.py
cd ../cssejhu
./Download.py
cd ../us
./states.py
cd ../cal
./counties.py
cd ..
git add *


