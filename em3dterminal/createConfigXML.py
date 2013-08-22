import xml.etree.ElementTree as ET
from xml.dom import minidom


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def main():
    # create main component
    root = ET.Element("config")

    # create reprap configuration
    reprap = ET.SubElement(root, "reprap")
    reprap.set("firmware", "Sprinter")
    rr_port = ET.SubElement(reprap, "port")
    rr_port.text = "/dev/ttyACM0"
    rr_baud = ET.SubElement(reprap, "baud")
    rr_baud.text = "115200"
    rr_maxXYaxis = ET.SubElement(reprap, "MAX_XY_AXIS")
    rr_maxXYaxis.text = "2000"
    rr_maxZaxis = ET.SubElement(reprap, "MAX_Z_AXIS")
    rr_maxZaxis.text = "1200"

    # create pna configuration
    pna = ET.SubElement(root, "pna")
    pna.set("name", "N5230C")
    pna_ip = ET.SubElement(pna, "ip")
    pna_ip.text = "10.1.15.106"
    pna_port = ET.SubElement(pna, "port")
    pna_port.text = "5024"
    pna_calib = ET.SubElement(pna, "calib")
    pna_calib.text = "calibrationRado1.csa"

    # create atmega configuration
    atmega = ET.SubElement(root, "atmega")
    atmega.set("name", "atmega128rfa1")
    atmega_baud = ET.SubElement(atmega, "port")
    atmega_baud.text = "/dev/ttyUSB0"
    atmega_baud = ET.SubElement(atmega, "baud")
    atmega_baud.text = "9600"

    # create output file configuration
    output = ET.SubElement(root, "output")
    output_file = ET.SubElement(output, "file")
    output_file.text = "em3dterminal.out"

    # create prettified document string
    document = prettify(root)

    # write file to disk
    output_file = open("em3dterminal.xml", "w")
    output_file.write(document)
    output_file.close()

    print "Config file successfully generated."

if __name__ == "__main__":
    main()
