import xml.etree.ElementTree as ET


def main():
    # create main component
    root = ET.Element("config")

    # create pna configuration
    pna = ET.SubElement(root, "pna")
    pna.set("name", "N5230C")
    ip = ET.SubElement(pna, "ip")
    ip.text = "10.1.15.106"
    port = ET.SubElement(pna, "port")
    port.text = "5024"
    calib = ET.SubElement(pna, "calib")
    calib.text = "calibrationRado1.csa"

    # create atmega configuration
    atmega = ET.SubElement(root, "atmega")
    baud = ET.SubElement(atmega, "port")
    baud.text = "/dev/ttyACM0"
    atmega.set("name", "atmega128rfa1")
    baud = ET.SubElement(atmega, "baud")
    baud.text = "9600"

    tree = ET.ElementTree(root)
    tree.write("em3da.xml")

    f = open("em3da.xml", 'a')
    f.write("\n")
    f.close()

    print "Config file successfully generated."

if __name__ == "__main__":
    main()
