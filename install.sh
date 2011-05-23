#!/bin/sh
# Kill all runing instances if exists
#killall gedit

# Register mime types
sudo cp mime/*.xml /usr/share/mime/packages
# Copy language definitions
sudo cp lang-specs/*.lang /usr/share/gtksourceview-3.0/language-specs/
# Update mime type database
sudo update-mime-database /usr/share/mime
# Copy gedit start script
sudo cp -s bin/g /usr/bin/g

# Copy gedit facilities
if [ ! -d $HOME/.config/gedit ]
then
mkdir -p ~/.config/gedit
fi
# Copy Snippets
if [ ! -d $HOME/.config/gedit/snippets ]
then
mkdir -p ~/.config/gedit/snippets
fi
cp snippets/* ~/.config/gedit/snippets/

# Copy Plugins
if [ ! -d $HOME/.config/gedit/plugins ]
then
mkdir -p ~/.config/gedit/plugins
fi
cp -R plugins/* ~/.config/gedit/plugins

# Copy Styles
if [ ! -d $HOME/.config/gedit/styles ]
then
mkdir -p ~/.config/gedit/styles
fi
cp styles/* ~/.config/gedit/styles
