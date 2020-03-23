
all: OBC-firmware documentation


documentation: OBC-firmware-documentation
	cd ARD && make	

OBC-firmware:
	cd Helix-OBC-Firmware && make

OBC-firmware-documentation:
	cd Helix-OBC-Firmware && make documentation

clean:
	cd Helix-OBC-Firmware && make clean
	cd ARD && make clean

# Function used to check variables. Use on the command line:
# make print-VARNAME
# Useful for debugging and adding features
print-%: ; @echo $*=$($*)
