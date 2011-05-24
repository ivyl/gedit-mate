#!/bin/bash

rm -r html-tidy
cd /home/atavory/.gnome2/gedit/plugins/
rm html-tidy/*.pyc 
tar czvf html-tidy-gedit-plugin.tar.gz html-tidy html-tidy.gedit-plugin 
cd /home/atavory/downloads
cp -r /home/atavory/.gnome2/gedit/plugins/html-tidy/doc html-tidy -r
mv /home/atavory/.gnome2/gedit/plugins/html-tidy-gedit-plugin.tar.gz html-tidy/
rsync html-tidy -rv atavory@www.eng.tau.ac.il:public_html/gedit-plugins/
rm html-tidy-gedit-plugin.tar.gz

