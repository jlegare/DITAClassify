import os
import os.path
import sys

import argparse

from lxml import etree


def classify (path_name):
    print ("   ", path_name)


def configure (argv):
    parser = argparse.ArgumentParser (description = "Classify DITA files into maps, topics, and others.")

    parser.add_argument ("path_name", nargs = "*", help = "paths to files")
    parser.add_argument ("-c", "--catalog",        help = "path to OASIS catalog")

    arguments = parser.parse_args (argv)

    if arguments.catalog:
        catalogs = os.environ["XML_CATALOG_FILES"].split (" ") if "XML_CATALOG_FILES" in os.environ else [ ]
        catalogs.append (os.path.abspath (arguments.catalog))
        os.environ["XML_CATALOG_FILES"] = " ".join (catalogs)

    return arguments.path_name


def visit (path_name, visitor):
    for ( root, _, file_names ) in os.walk (path_name):
        for file_name in file_names:
            visitor (os.path.join (root, file_name))


if __name__ == "__main__":
    for path_name in configure (sys.argv):
        visit (path_name, classify)
