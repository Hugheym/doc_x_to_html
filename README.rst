Doc(X)ToHTML
============

Simple utility to convert multiple .doc or docx files to html files.

Unfortunately you need Libreoffice installed and callable through the
command-line via soffice to deal with .doc files.

You can install libreoffice on your system if not already installed

on Debian/Ubuntu with

::

    sudo apt-get install libreoffice

Or Fedora with

::

    sudo yum install libreoffice

Once properly installed you can convert all .doc and .docx files in the
source directory to html files in the target directory using the
command:

::

    doc_x_to_html [source_dir] [target_dir] 
