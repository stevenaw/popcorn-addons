#!/usr/bin/env python

import sys, os, os.path, markdown, elementtree, re, shutil
from subprocess import call

dist = "./dist"
plugindist = dist + "/plugins"
parserdist = dist + "/parsers"
playerdist = dist + "/players"
moduledist = dist + "/modules"
effectdist = dist + "/effects"

if not os.path.exists( dist ):
  os.mkdir( dist )

if not os.path.exists( parserdist ):
  os.mkdir( parserdist )

if not os.path.exists( plugindist ):
  os.mkdir( plugindist )

if not os.path.exists( playerdist ):
  os.mkdir( playerdist )

if not os.path.exists( moduledist ):
  os.mkdir( moduledist )

if not os.path.exists( effectdist ):
  os.mkdir( effectdist )

def safePath( path ):
  return path.replace( "\\", "/" );

def checkPath( path ):
  if not os.path.exists( path ):
    os.mkdir( path )

def process( root, filename, dist ):
  if filename.endswith( ".md" ):
    md = markdown.Markdown()
    fullpath = safePath( os.path.abspath( os.path.join( root, filename )))
    FILE = open( fullpath, "r" )
    newfilename = filename.replace( ".md", ".html" )
    folder = os.path.split( os.path.dirname( fullpath ) )[ 1 ]
    distpath = safePath( os.path.abspath( os.path.join( dist, folder ) ) )

    html = md.convert( FILE.read() )
    FILE.close()

    checkPath( distpath )

    distpath = safePath( os.path.abspath( os.path.join( distpath, newfilename ) ) )
    FILE = open( distpath, "w" )

    FILE.write( html )
    FILE.close()

  if filename.endswith( ".js" ) \
      and not filename.endswith( ".unit.js" ):

    fullpath = safePath( os.path.abspath( os.path.join( root, filename ) ) )
    folder = os.path.split( os.path.dirname( fullpath ) )[ 1 ]
    distpath = safePath( os.path.abspath( os.path.join( dist, folder ) ) )
    checkPath( distpath )

    shutil.copy( fullpath, distpath )

print "Building dist/plugins ..."
for root, dirs, filenames in os.walk( "./plugins" ):
  for filename in filenames:
    sys.stdout.flush()
    sys.stderr.flush()

    process( root, filename, plugindist )

print "Building dist/parsers/ ..."
for root, dirs, filenames in os.walk( "./parsers" ):
  for filename in filenames:
    sys.stdout.flush()
    sys.stderr.flush()

    process( root, filename, parserdist )

print "Building dist/players/ ..."
for root, dirs, filenames in os.walk( "./players" ):
  for filename in filenames:
    sys.stdout.flush()
    sys.stderr.flush()

    process( root, filename, playerdist )

print "Building dist/modules/ ..."
for root, dirs, filenames in os.walk( "./modules" ):
  for filename in filenames:
    sys.stdout.flush()
    sys.stderr.flush()

    process( root, filename, moduledist )

print "Building dist/effects/ ..."
for root, dirs, filenames in os.walk( "./effects" ):
  for filename in filenames:
    sys.stdout.flush()
    sys.stderr.flush()

    process( root, filename, effectdist )