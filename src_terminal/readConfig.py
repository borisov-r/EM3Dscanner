# this file should create XML configuration for the measurements
# Element.findall() finds only elements with a tag which are
# direct children of the current element.
# Element.find() finds the first child with a particular tag, and
# Element.text() accesses the element's text content
# Element.get() accesses the element's attributes:

import xml.etree.ElementTree as ET


def main():
    file = ET.parse('em3d.xml')
    root = file.getroot()
    for children in root:
        if "pna" in children.get('name'):
            test = children
            print "OK"

    for children in test:
        print children.tag, children.text

if __name__ == "__main__":
    main()
