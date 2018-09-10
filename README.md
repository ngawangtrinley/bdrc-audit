# bdrc-audit
First version of an archive auditing tool for BDRC

![image](https://user-images.githubusercontent.com/17675331/39052432-843cd138-44de-11e8-8968-840055bf58d0.png)

## Get the standalone desktop app
* Mac - [bdrc-audit01](https://github.com/ngawangtrinley/bdrc-audit/releases/download/v01.1/bdrc-audit.zip) (zip file)
* Windows - coming soon
* Linux - coming soon

## Features
* count images in archive/images folders in folders such as: /Documents/W3G012/archive/01/image01.jpg
* open item with a double click
* save search result as a table in Excel-csv format

## Usage
1. Select folder to audit
2. type **archive**, **images**, or **archive, images**
3. change the folder level to see the content of child folders

## Filter with wildcards

", ": use a **comma followed by a space** to separate filter keywords

    archive, images 
...will match both **archive** and **images**

"*": **\*** stands for any character or string of characters

    arch*
... will match **arch**ive, **arch**itecture and **arch**ery

"?": **?** stands for one or no character

    image?
...will match both **image** and **image**s



## To Do
* order files by name/size
* audit number of files per folder
* audit folder/file names
* check that the image number matches the number in the biblio-sheet 
* audit biblio-sheets
* Pillow integration
* audit image metadata
* generate archive and web bundles
* sync images to the server when ready


### Building from source

To build the project from source, get [PyInstaller](http://pyinstaller.readthedocs.io/en/stable/installation.html) on your machine and use the following command:

    pyinstaller -w -F bdrc-audit.py --icon=rc/icon-windowed.icns

In order to support **retina** display on Mac, locate the *Info.plist* directory in the *bdrc-audit.app* bundle and add the following string/key pair at the end of the list:

    <string>NSHighResolutionCapable</string>
    <key>True</key>
