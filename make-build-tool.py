#!/usr/bin/env python

import sys, os, os.path, markdown, elementtree, re, shutil
from subprocess import call

def safePath(path):
  return path.replace("\\","/");

def checkPath(path):
  if not os.path.exists(path):
    os.mkdir(distpath)

dist = "./dist"
plugindist = dist + "/plugins"

if not os.path.exists(dist):
  os.mkdir(dist)

if not os.path.exists(plugindist):
  os.mkdir(plugindist)

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
      distpath = safePath(os.path.abspath(os.path.join( plugindist, folder)))

      print "converting " + folder + "/" + filename + " to html"
      html = md.convert(FILE.read())
      FILE.close()

      checkPath(distpath)

      distpath = safePath(os.path.abspath(os.path.join( distpath, newfilename)))
      FILE = open( distpath, "w" )

      FILE.write( html )
      FILE.close()

    if filename.endswith( ".js" ) \
        and not filename.endswith( ".unit.js" ):

      fullpath = safePath(os.path.abspath(os.path.join(root, filename)))
      folder = os.path.split(os.path.dirname(fullpath))[1]
      distpath = safePath(os.path.abspath(os.path.join( plugindist, folder)))
      checkPath(distpath)

      print "copying " + folder + "/" + filename + " to dist/plugins/" + folder
      shutil.copy(fullpath, distpath)
      #print "minifying " + folder + "/" + filename + " to dist/plugins/" + folder
      #call(["java", "-jar", "./build/google-compiler-20100917.jar", "--js", os.path.join(root, filename), "--compilation_level", "SIMPLE_OPTIMIZATIONS", "--js_output_file", os.path.join( distpath, filename.replace(".js", ".min.js"))])