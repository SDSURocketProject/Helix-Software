ARD Scripts Architecture
========================

In general the ARD scripts work by loading in the JSON config files, located
at ARD/config/ by default, verifying that they are correctly formatted,
generating the C/C++ source code, generating latex, calling xelatex, and
generating the binary memory files for the extension boards. The "main" function
that shows all of the steps is called genARD in the file genARD.
