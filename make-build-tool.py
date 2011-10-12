#!/usr/bin/env python

import sys, os, os.path, markdown, elementtree, re

def safePath(path):
  return path.replace("\\","/");

dist = "./dist"

if not os.path.exists(dist):
  os.mkdir(dist)

for root, dirs, filenames in os.walk("./plugins"):
  for filename in filenames:
    sys.stdout.flush()
    sys.stderr.flush()

    if filename.endswith(".md"):
      md = markdown.Markdown()
      fullpath = safePath(os.path.abspath(os.path.join(root, filename)))
      FILE = open(fullpath, "r")

      html = md.convert(FILE.read())
      FILE.close()

      newfilename = filename.replace( ".md", ".html" )
      folder = os.path.split(os.path.dirname(fullpath))[1]
      distpath = safePath(os.path.abspath(os.path.join( dist, folder)))

      if not os.path.exists(distpath):
        os.mkdir(distpath)

      distpath = safePath(os.path.abspath(os.path.join( distpath, newfilename)))
      FILE = open( distpath, "w" )

      FILE.write( html )
      FILE.close()