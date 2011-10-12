
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

# modules
MODULES_DIST = ${DIST_DIR}/popcorn.modules.js
MODULES_MIN = ${DIST_DIR}/popcorn.modules.min.js

# plugins
PLUGINS_DIST = ${DIST_DIR}/popcorn.plugins.js
PLUGINS_MIN = ${DIST_DIR}/popcorn.plugins.min.js

# plugins
PARSERS_DIST = ${DIST_DIR}/popcorn.parsers.js
PARSERS_MIN = ${DIST_DIR}/popcorn.parsers.min.js

# players
PLAYERS_DIST = ${DIST_DIR}/popcorn.players.js
PLAYERS_MIN = ${DIST_DIR}/popcorn.players.min.js

# effects
EFFECTS_DIST = $(DIST_DIR)/popcorn.effects.js
EFFECTS_MIN = $(DIST_DIR)/popcorn.effects.min.js

# Grab all popcorn.<plugin-name>.js files from plugins dir
PLUGINS_SRC := $(filter-out %unit.js, $(shell find ${PLUGINS_DIR} -name 'popcorn.*.js' -print))

# Grab all popcorn.<plugin-name>.js files from parsers dir
PARSERS_SRC := $(filter-out %unit.js, $(shell find ${PARSERS_DIR} -name 'popcorn.*.js' -print))

# Grab all popcorn.<player-name>.js files from players dir
PLAYERS_SRC := $(filter-out %unit.js, $(shell find ${PLAYERS_DIR} -name 'popcorn.*.js' -print))

# Grab all popcorn.<effect-name>.js files from effects dir
EFFECTS_SRC := $(filter-out %unit.js, $(shell find $(EFFECTS_DIR) -name 'popcorn.*.js' -print))

# Grab all popcorn.<Module-name>.js files from modules dir
MODULES_SRC := $(filter-out %unit.js, $(shell find $(MODULES_DIR) -name 'popcorn.*.js' -print))

# Grab all popcorn.<plugin-name>.unit.js files from plugins dir
PLUGINS_UNIT := $(shell find ${PLUGINS_DIR} -name 'popcorn.*.unit.js' -print)

# Grab all popcorn.<parser-name>.unit.js files from parsers dir
PARSERS_UNIT := $(shell find ${PARSERS_DIR} -name 'popcorn.*.unit.js' -print)

# Grab all popcorn.<player-name>.unit.js files from players dir
PLAYERS_UNIT := $(shell find ${PLAYERS_DIR} -name 'popcorn.*.unit.js' -print)

# Grab all popcorn.<effects>.unit.js files from effects dir
EFFECTS_UNIT := $(shell find $(EFFECTS_DIR) -name 'popcorn.*.unit.js' -print)

# Grab all popcorn.<module-name>.unit.js files from modules dir
MODULES_UNIT := $(shell find $(MODULES_DIR) -name 'popcorn.*.unit.js' -print)

make-min: ${MODULES_MIN} ${PLUGINS_MIN} ${PARSERS_MIN} ${PLAYERS_MIN} $(EFFECTS_MIN)

${MODULES_MIN}: ${MODULES_DIST}
	@@echo "Building" ${MODULES_MIN}
	@@$(call compile, $(shell for js in ${MODULES_SRC} ; do echo --js $$js ; done), ${MODULES_MIN})

${MODULES_DIST}: ${MODULES_SRC} ${DIST_DIR}
	@@echo "Building ${MODULES_DIST}"
	@@cat ${MODULES_SRC} > ${MODULES_DIST}

${PLUGINS_MIN}: ${PLUGINS_DIST}
	@@echo "Building" ${PLUGINS_MIN}
	@@$(call compile, $(shell for js in ${PLUGINS_SRC} ; do echo --js $$js ; done), ${PLUGINS_MIN})

${PLUGINS_DIST}: ${PLUGINS_SRC} ${DIST_DIR}
	@@echo "Building ${PLUGINS_DIST}"
	@@cat ${PLUGINS_SRC} > ${PLUGINS_DIST}

${PARSERS_MIN}: ${PARSERS_DIST}
	@@echo "Building" ${PARSERS_MIN}
	@@$(call compile, $(shell for js in ${PARSERS_SRC} ; do echo --js $$js ; done), ${PARSERS_MIN})

${PARSERS_DIST}: ${PARSERS_SRC} ${DIST_DIR}
	@@echo "Building ${PARSERS_DIST}"
	@@cat ${PARSERS_SRC} > ${PARSERS_DIST}

${PLAYERS_MIN}: ${PLAYERS_DIST}
	@@echo "Building" ${PLAYERS_MIN}
	@@$(call compile, $(shell for js in ${PLAYERS_SRC} ; do echo --js $$js ; done), ${PLAYERS_MIN})

${PLAYERS_DIST}: ${PLAYERS_SRC} ${DIST_DIR}
	@@echo "Building ${PLAYERS_DIST}"
	@@cat ${PLAYERS_SRC} > ${PLAYERS_DIST}

$(EFFECTS_MIN): $(EFFECTS_DIST)
	@@echo "Building" $(EFFECTS_MIN)
	@@$(call compile, $(shell for js in $(EFFECTS_SRC) ; do echo --js $$js ; done), $(EFFECTS_MIN))

$(EFFECTS_DIST): $(EFFECTS_SRC) $(DIST_DIR)
	@@echo "Building $(EFFECTS_DIST)"
	@@cat $(EFFECTS_SRC) > $(EFFECTS_DIST)

setup:
	@@echo "initializing and updating submodules..."
	@@git submodule update --init

build-tool: setup
	@@echo "Building Popcorn build tool"
	@@python make-build-tool.py

clean:
	@@echo "Removing Distribution directory" ${DIST_DIR}
	@@rm -rf ${DIST_DIR}