OS=$(shell uname -s)
LLVM_VERSION=$(shell llvm-config --version | cut -d . -f 1,2)
OUTPUT_FILE="../libs/numpy_weld_convertor"

ifndef EXEC
  EXEC=python
endif

PYTHON_HEADER_INCLUDE = $(shell $(EXEC)-config --includes)
NUMPY_HEADER_INCLUDE = -I$(shell $(EXEC) -c "import numpy; print(numpy.get_include())" 2>/dev/null)

PYTHON_LDFLAGS=-L$(shell $(EXEC) -c "from distutils import sysconfig; print(sysconfig.get_config_var('LIBDIR'))" 2>/dev/null) $(shell $(EXEC)-config --libs)

ifeq (${NUMPY_HEADER_INCLUDE}, -I)
  $(error Error: NumPy installation not found)
endif

ifeq (${OS}, Darwin)
  # OS X
  CLANG ?= clang
  CLANGPP ?= clang++
  FLAGS=-march=native -O3 -flto
  DFLAGS=-dynamiclib
  DYLIB_SUFFIX=.dylib
  PYTHON_INCLUDES=${PYTHON_HEADER_INCLUDE} ${NUMPY_HEADER_INCLUDE}
else ifeq (${OS}, Linux)
  # Linux
  CLANG ?= clang
  CLANGPP ?= clang++
  FLAGS=-mavx2 -fuse-ld=gold -flto
  DFLAGS=-shared -fPIC
  DYLIB_SUFFIX=.so
  PYTHON_INCLUDES=${PYTHON_HEADER_INCLUDE} ${NUMPY_HEADER_INCLUDE}
else
  $(error Unsupported platform: ${OS})
endif

convertor:
	${CLANG} ${DFLAGS} -w -march=native $(PYTHON_LDFLAGS) numpy.cpp -o ${OUTPUT_FILE}${DYLIB_SUFFIX}  ${PYTHON_INCLUDES}

clean:
	rm -rf run ${OUTPUT_FILE}${DYLIB_SUFFIX} *.pyc
