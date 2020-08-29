
all: OBC-firmware documentation

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = docs/build

documentation: ARD-headers OBC-firmware-documentation
	cd ARD && python3 genARD.py
	cd ARD && $(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

ARD-headers:
	make -C ARD/ headers

OBC-firmware: ARD-headers
	cd Helix-OBC-Firmware && make all

OBC-firmware-documentation: ARD-headers
	cd Helix-OBC-Firmware && make documentation

clean:
	cd Helix-OBC-Firmware && make clean
	cd ARD && make clean

# Function used to check variables. Use on the command line:
# make print-VARNAME
# Useful for debugging and adding features
print-%: ; @echo $*=$($*)
