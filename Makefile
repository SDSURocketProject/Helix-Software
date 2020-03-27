
all: OBC-firmware documentation


documentation: ARD-headers OBC-firmware-documentation
	cd ARD && python3 genARD.py

ARD-headers:
	make -C ARD/ headers

OBC-firmware: ARD-headers
	cd Helix-OBC-Firmware && make

OBC-firmware-documentation: ARD-headers
	cd Helix-OBC-Firmware && make documentation

clean:
	cd Helix-OBC-Firmware && make clean
	cd ARD && make clean

# Function used to check variables. Use on the command line:
# make print-VARNAME
# Useful for debugging and adding features
print-%: ; @echo $*=$($*)
