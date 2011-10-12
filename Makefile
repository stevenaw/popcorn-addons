
PREFIX = .
BUILD_DIR = ${PREFIX}/build
DIST_DIR = ${PREFIX}/dist
PLUGINS_DIR = ${PREFIX}/plugins
PARSERS_DIR = ${PREFIX}/parsers
PLAYERS_DIR = ${PREFIX}/players
EFFECTS_DIR = $(PREFIX)/effects
MODULES_DIR = $(PREFIX)/modules

RHINO ?= java -jar ${BUILD_DIR}/js.jar

CLOSURE_COMPILER = ${BUILD_DIR}/google-compiler-20100917.jar
compile = @@${MINJAR} $(1) \
	                    --compilation_level SIMPLE_OPTIMIZATIONS \
	                    --js_output_file $(2)

# minify
MINJAR ?= java -jar ${CLOSURE_COMPILER}

${DIST_DIR}:
	@@mkdir -p ${DIST_DIR}

# plugins
PLUGINS_DIST = ${DIST_DIR}/popcorn.plugins.js
PLUGINS_MIN = ${DIST_DIR}/popcorn.plugins.min.js

# Grab all popcorn.<plugin-name>.js files from plugins dir
PLUGINS_SRC := $(filter-out %unit.js, $(shell find ${PLUGINS_DIR} -name 'popcorn.*.js' -print))

make-min: ${PLUGINS_MIN}

${PLUGINS_MIN}: ${PLUGINS_SRC} ${DIST_DIR}
	@@echo "Building" ${PLUGINS_MIN}
	@@$(call compile, $(shell for js in ${PLUGINS_SRC} ; do echo --js $$js ; done), ${PLUGINS_MIN})

setup:
	@@echo "initializing and updating submodules..."
	@@git submodule update --init

build-tool: setup ${PLUGINS_MIN}
	@@echo "Building Popcorn build tool"
	@@python make-build-tool.py

clean:
	@@echo "Removing Distribution directory" ${DIST_DIR}
	@@rm -rf ${DIST_DIR}