#!/usr/bin/env python

import sys, os, os.path, markdown, elementtree, re, shutil
from subprocess import call

dist = "./dist"
plugindist = dist + "/plugins"
parserdist = dist + "/parsers"
playerdist = dist + "/players"
moduledist = dist + "/modules"
effectdist = dist + "/effects"

manifestText = "{"

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

def process( root, filename, dist, m ):
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
    return ""

  if filename.endswith( ".js" ) \
      and not filename.endswith( ".unit.js" ) \
      and not filename.endswith( ".player.api.js" ):

    fullpath = safePath( os.path.abspath( os.path.join( root, filename ) ) )
    folder = os.path.split( os.path.dirname( fullpath ) )[ 1 ]
    distpath = safePath( os.path.abspath( os.path.join( dist, folder ) ) )
    checkPath( distpath )

    shutil.copy( fullpath, distpath )
    return '    "' + folder + '/' + filename + '",\n'

print "Building dist/plugins ..."
manifestText = manifestText + '\n  "plugins": [\n'
for root, dirs, filenames in os.walk( "./plugins" ):
  for filename in filenames:
    sys.stdout.flush()
    sys.stderr.flush()

    text = process( root, filename, plugindist, manifestText )
    if ( text ):
      manifestText = manifestText + text

print "Building dist/parsers/ ..."
manifestText = manifestText[:len( manifestText ) - 2 ]  + '\n  ],\n  "parsers": [\n'
for root, dirs, filenames in os.walk( "./parsers" ):
  for filename in filenames:
    sys.stdout.flush()
    sys.stderr.flush()

    text = process( root, filename, parserdist, manifestText )
    if ( text ):
      manifestText = manifestText + text

print "Building dist/players/ ..."
manifestText = manifestText[:len( manifestText ) - 2 ]  + '\n  ],\n  "players": [\n'
for root, dirs, filenames in os.walk( "./players" ):
  for filename in filenames:
    sys.stdout.flush()
    sys.stderr.flush()

    text = process( root, filename, playerdist, manifestText )
    if ( text ):
      manifestText = manifestText + text

print "Building dist/modules/ ..."
manifestText = manifestText[:len( manifestText ) - 2 ]  + '\n  ],\n  "modules": [\n'
for root, dirs, filenames in os.walk( "./modules" ):
  for filename in filenames:
    sys.stdout.flush()
    sys.stderr.flush()

    text = process( root, filename, moduledist, manifestText )
    if ( text ):
      manifestText = manifestText + text

print "Building dist/effects/ ..."
manifestText = manifestText[:len( manifestText ) - 2 ]  + '\n  ], \n  "effects": [\n'
for root, dirs, filenames in os.walk( "./effects" ):
  for filename in filenames:
    sys.stdout.flush()
    sys.stderr.flush()

    text = process( root, filename, effectdist, manifestText )
    if ( text ):
      manifestText = manifestText + text

manifestText = manifestText[:len( manifestText ) - 2 ]  + '\n  ]\n}'

if os.path.isfile( "./manifest.json" ):
  os.remove( "./manifest.json" )

print "writing new manifest.json"
manifest = open( "./manifest.json", "w" )
manifest.write( manifestText )
manifest.close()