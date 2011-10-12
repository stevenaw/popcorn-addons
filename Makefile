
${SUBMODULES}:
	@@echo "initializing and updating submodules..."

build-tool: ${SUBMODULES}
	@@echo "Building Popcorn build tool"
	@@python make-build-tool.py
