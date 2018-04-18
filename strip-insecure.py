#! /usr/bin/env python
# Identifies insecure source links in entries in the files/repositories.xml
# and deletes them.
#
# Insecure links have the form: git://github.com/...
#
# Usage: strip-insecure.py repositories.xml >repositories-secure.xml
#        The default file of repositories.xml will be selected if called
#        without a parameter
#
# Copyright 2018 Paul Jewell <paul@teulu.org>
#
#  Distributed under the terms of the GNU GPL version 3 or later

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree
import sys
from sys import argv

# Process the command line
repositoryFile = argv[1]

OutputFile = "repositories-secure.xml"    
RepositoryList = etree.parse(repositoryFile)

repos = RepositoryList.findall('repo')

for repo in repos:
    sources = repo.findall('source')
    num_sources = len(sources)

    for source in sources:
        if source.text.startswith("git:"):
            if num_sources > 1:
                repo.remove(source)
            else: # We have a problem - only one source and it's insecure
                name = repo.find('name').text
                print(f"Warning: In repo: {name} - Only one insecure source")
                # Change the entry fro "git://..." to "git@github" if github repository
                # otherwise issue warning and don't change it
                if source.text.startswith("git://github.com"):
                    source.text ="git+ssh://git@" + source.text[6:]
                else:
                    print(f"Not changing source line for repo: {name}")
                                              
RepositoryList.write(OutputFile, encoding="utf-8", xml_declaration=True)

