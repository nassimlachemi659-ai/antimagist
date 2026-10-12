import os
import xml.etree.ElementTree as ET

appdata_mods_xml = os.path.expanduser("~/AppData/Local/Teardown/mods.xml")

def force_activate():
    if os.path.exists(appdata_mods_xml):
        tree = ET.parse(appdata_mods_xml)
        root = tree.getroot()
        
        for mod in root.findall("mod"):
            mod_id = mod.attrib.get("id", "")
            if mod_id.startswith("local-"):
                mod.set("active", "true")
                mod.set("shown", "true")
                
        tree.write(appdata_mods_xml, encoding="utf-8", xml_declaration=True)
        print("Updated mods.xml: Set active='true' and shown='true' for all local mods.")

if __name__ == "__main__":
    force_activate()
