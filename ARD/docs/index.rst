.. ARD documentation master file, created by
   sphinx-quickstart on Sat Aug 29 09:14:06 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the documentation for the ARD scripts!
=================================================

The origin goal of the Avionics Reference Document (ARD) scripts was to use
some configuration files to generate a single PDF file that could serve as
a reference for non-avionics members. Havings just a few configuration files
meant that updating the whole ARD pdf would be relatively easy, although this
flexibility also lead to the ARD scripts to taking on more goals. At this
point the ARD scripts use the config files to generate C/C++ source code, binary
memory files for extension boards, as well as the ARD itself.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   architecture
   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
