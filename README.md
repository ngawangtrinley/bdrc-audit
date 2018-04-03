# bdrc-audit
First version of an archive auditing tool for BDRC, built with 

## Get the standalone desktop app
* Mac - [bdrc-audit01](https://github.com/ngawangtrinley/bdrc-audit/releases/download/v01/bdrc-audit.zip)
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

* ", ": use a comma followed by a space to separate filter keywords

    archive, images 
...will match both **archive** and **images**

* "*": * replaces any string of characters

    arch
... will match **arch**ive, **arch**itecture and **arch**ery

* "?": ? stands for one or no character

    image?
... will match both **image** and **image**s



## To Do
* order files by name/size
* audit number of files per folder
* audit folder/file names
* audit biblio-sheets
* Pillow integration
* audit image metadata
* generate archive and web bundles
* sync images to the server when ready