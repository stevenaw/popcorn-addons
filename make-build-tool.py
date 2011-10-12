#!/usr/bin/env python

import sys, os, os.path, markdown, elementtree, re, shutil

def safePath(path):
  return path.replace("\\","/");

def checkPath(path):
  if not os.path.exists(path):
    os.mkdir(distpath)

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
      newfilename = filename.replace( ".md", ".html" )
      folder = os.path.split(os.path.dirname(fullpath))[1]
      distpath = safePath(os.path.abspath(os.path.join( dist, folder)))

      print "converting " + folder + "/" + filename + " to html"
      html = md.convert(FILE.read())
      FILE.close()

      checkPath(distpath)

      distpath = safePath(os.path.abspath(os.path.join( distpath, newfilename)))
      FILE = open( distpath, "w" )

      FILE.write( html )
      FILE.close()

    if filename.endswith(".html") and not filename.endswith(".unit.html"):
      fullpath = safePath(os.path.abspath(os.path.join(root, filename)))
      folder = os.path.split(os.path.dirname(fullpath))[1]
      distpath = safePath(os.path.abspath(os.path.join( dist, folder)))
      checkPath(distpath)

      print "copying " + folder + "/" + filename + " to dist/" + folder
      shutil.copy(fullpath, distpath)