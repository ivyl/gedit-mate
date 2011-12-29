#!/bin/sh
# Kill all runing instances if exists
#killall gedit

PREFIX=$HOME/.local/share/gedit

# Register mime types
sudo cp mime/*.xml /usr/share/mime/packages
# Copy language definitions
sudo cp lang-specs/*.lang /usr/share/gtksourceview-3.0/language-specs/
# Update mime type database
sudo update-mime-database /usr/share/mime
# Copy gedit start script
sudo cp bin/g /usr/bin/g

# Copy gedit facilities
mkdir -p $PREFIX
mkdir -p $PREFIX/snippets
mkdir -p $PREFIX/plugins
mkdir -p $PREFIX/styles

cp snippets/* $PREFIX/snippets/
cp -R plugins/* $PREFIX/plugins/
cp styles/* $PREFIX/styles/

# Create link in .config (since some distributions still uses this)
mkdir -p $HOME/.config
ln -s $HOME/.local/share/gedit $HOME/.config/
