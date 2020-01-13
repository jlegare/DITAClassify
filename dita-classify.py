import os
import os.path
import sys

import argparse
import mimetypes # libmagic is not available on macOS without installing Brew.

from lxml import etree


def classify (path_name):
    def types_of (dita_class):
        return filter (lambda s : s != "", dita_class.split (" "))

    ( mime_type, encoding ) = mimetypes.guess_type (path_name)

    if mime_type == "application/xml":
        parser = etree.XMLParser (attribute_defaults = True, dtd_validation = True)
        tree   = etree.parse (path_name, parser)
        root   = tree.getroot ()

        if "class" in root.attrib:
            types = types_of (root.attrib["class"])

            if "topic/topic" in types:
                print ("TOPIC", path_name)

            elif "map/map" in types:
                print ("MAP  ", path_name)

            else:
                print ("OTHER", path_name)

        else:
            print ("OTHER", path_name)

    else:
        print ("OTHER", path_name)


def configure (argv):
    mimetypes.init ()

    parser = argparse.ArgumentParser (description = "Classify DITA files into maps, topics, and others.")

    parser.add_argument ("-c", "--catalog",    help = "path to OASIS catalog")
    parser.add_argument ("-m", "--mime-types", help = "path to file containing additional MIME type mappings")

    parser.add_argument ("path_name", nargs = "*", help = "paths to files")

    arguments = parser.parse_args (argv)

    if arguments.catalog:
        catalog_path = os.path.abspath (arguments.catalog)

        if os.path.exists (catalog_path):
            catalogs = os.environ["XML_CATALOG_FILES"].split (" ") if "XML_CATALOG_FILES" in os.environ else [ ]
            catalogs.append (catalog_path)
            os.environ["XML_CATALOG_FILES"] = " ".join (catalogs)

        else:
            print ("ERROR: \"" + arguments.catalog + "\" not found. It will be ignored.")

    if arguments.mime_types:
        if os.path.exists (arguments.mime_types):
            mime_types = mimetypes.read_mime_types (arguments.mime_types)
            if mime_types is not None:
                for ( extension, mime_type ) in mime_types.items ():
                    mimetypes.add_type (mime_type, extension)

        else:
            print ("ERROR: \"" + arguments.mime_types + "\" not found. It will be ignored.")

    return arguments.path_name


def visit (path_name, visitor):
    for ( root, _, file_names ) in os.walk (path_name):
        for file_name in file_names:
            visitor (os.path.join (root, file_name))


if __name__ == "__main__":
    for path_name in configure (sys.argv):
        visit (path_name, classify)
