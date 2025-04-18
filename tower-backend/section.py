import numpy as np
import json
import math
from utils import normalizeTowerDataKeys


class Section:

    def __init__(self, towerData, elementSections=None, sectionLibrary=None):
        self.towerData = towerData
        self.elementSections = elementSections or {}
        self.sectionLibrary = sectionLibrary or {}
        self._validateInputs()

    def _validateInputs(self):
        requiredKeys = ["tower_base_width", "top_width", "height", "variable_segments", "constant_segments"]
        for key in requiredKeys:
            if key not in self.towerData:
                raise ValueError(f"Missing required parameter: {key}")

    DEFAULT_ELEMENT_PROPERTIES = {
        "secction_type": "round",
        "cross_area": 1222.6,
        "projected_width": 0.0508,
        "density": 7850,
        "young_modulus": 200000,
        "moment_of_inertia": 275000.0
    }

    def getSectionProps(self, sectionType, sectionName):
        if sectionType not in self.sectionLibrary:
            return self.DEFAULT_ELEMENT_PROPERTIES
        for entry in self.sectionLibrary[sectionType]:
            if entry["name"] == sectionName:
                return entry
        return self.DEFAULT_ELEMENT_PROPERTIES

    def midpoint(self, p1, p2):
        return [
            round((p1[0] + p2[0]) / 2, 3),
            round((p1[1] + p2[1]) / 2, 3),
            round((p1[2] + p2[2]) / 2, 3),
        ]



    def getCoordinates(self):
        baseWidth = self.towerData["tower_base_width"]
        topWidth = self.towerData["top_width"]
        totalHeight = self.towerData["height"]
        variableSegments = self.towerData["variable_segments"]
        constantSegments = self.towerData["constant_segments"]

        segmentHeight = totalHeight / (variableSegments + constantSegments)
        taperDelta = (baseWidth - topWidth) / 2
        alpha = np.arctan(taperDelta / (variableSegments * segmentHeight))

        currentBase = baseWidth
        coordinatesList = []
        secction_init_x = 0.0
        secction_init_y = 0.0
        secction_init_z = 0.0

        zinitial = np.sin(np.deg2rad(60))*baseWidth

        for i in range(variableSegments):
            sectionNumber = i + 1
            segmentDelta = np.tan(alpha) * segmentHeight
            phi = np.arctan(segmentHeight / (currentBase - segmentDelta))
            gHeight = np.tan(phi) * (currentBase / 2)
            deltaG = gHeight * np.tan(alpha)

            localCoords = {
                'section': sectionNumber,
                'a': [round(0.0 + secction_init_x, 3), round(0.0 + secction_init_y, 3), round(secction_init_z, 3)],
                'b': [round(currentBase + secction_init_x, 3), round(0.0 + secction_init_y, 3), round(secction_init_z, 3)],
                'c': [round(segmentDelta + secction_init_x, 3), round(segmentHeight + secction_init_y, 3), round(segmentDelta + secction_init_z, 3)],
                'd': [round((currentBase - segmentDelta) + secction_init_x, 3), round(segmentHeight + secction_init_y, 3), round(segmentDelta + secction_init_z, 3)],
                'e': [round(deltaG + secction_init_x, 3), round(gHeight + secction_init_y, 3), round(deltaG + secction_init_z, 3)],
                'f': [round((currentBase - deltaG) + secction_init_x, 3), round(gHeight + secction_init_y, 3), round(deltaG + secction_init_z, 3)],
                'g': [round((currentBase / 2) + secction_init_x, 3), round(gHeight + secction_init_y, 3), round(deltaG + secction_init_z, 3)],
                'h': [round((currentBase / 2) + secction_init_x, 3), round(0.0 + secction_init_y, 3), round(zinitial - secction_init_z, 3)],
                'l': [round((currentBase / 2) + secction_init_x, 3), round(segmentHeight + secction_init_y, 3), round((zinitial - segmentDelta) - secction_init_z, 3)],
                'm': [round((currentBase / 2) + secction_init_x, 3), round(gHeight + secction_init_y, 3), round((zinitial - deltaG) - secction_init_z, 3)],
            }

            # ✅ Now calculate midpoints n and o
            localCoords['n'] = self.midpoint(localCoords['e'], localCoords['m'])
            localCoords['o'] = self.midpoint(localCoords['m'], localCoords['f'])

            coordinatesList.append(localCoords)
            currentBase -= segmentDelta * 2
            secction_init_x += segmentDelta
            secction_init_y += segmentHeight
            secction_init_z += segmentDelta


        for i in range(constantSegments):
            sectionNumber += 1
            localCoords = {
                'section': sectionNumber,

                #this are the coord to make the 2D tower section  

                'a': [round(0.0 + secction_init_x, 3), round(0.0 + secction_init_y, 3), round(secction_init_z, 3)],
                'b': [round(currentBase + secction_init_x, 3), round(0.0 + secction_init_y, 3), round(secction_init_z, 3)],
                'c': [round(secction_init_x, 3), round(segmentHeight + secction_init_y, 3),round(secction_init_z, 3)],
                'd': [round(currentBase + secction_init_x, 3), round(segmentHeight + secction_init_y, 3),round(secction_init_z, 3)],
                'e': [round(secction_init_x, 3), round((segmentHeight / 2) + secction_init_y, 3),round(secction_init_z, 3)],
                'f': [round(currentBase + secction_init_x, 3), round((segmentHeight / 2) + secction_init_y, 3),round(secction_init_z, 3)],
                'g': [round((currentBase / 2) + secction_init_x, 3), round((segmentHeight / 2) + secction_init_y, 3),round(secction_init_z, 3)],

                # Add this nodes to make the 3d tower section tiangle cross section node corresponding to the 3rd leg of the tower

                'h': [round((currentBase / 2)+ secction_init_x,3), round(0.0 + secction_init_y, 3), round(zinitial-secction_init_z , 3)],
                'l': [round((currentBase / 2)+ secction_init_x,3), round(segmentHeight + secction_init_y, 3), round(zinitial-secction_init_z , 3)],
                'm': [round((currentBase / 2)+ secction_init_x,3), round((segmentHeight / 2) + secction_init_y, 3), round(zinitial-secction_init_z , 3)],
            }

            # ✅ Now calculate n and o
            n = self.midpoint(localCoords['e'], localCoords['m'])
            o = self.midpoint(localCoords['m'], localCoords['f'])

            # ✅ Add them to localCoords
            localCoords['n'] = n
            localCoords['o'] = o

            coordinatesList.append(localCoords)
            secction_init_y += round(segmentHeight, 3)

        return coordinatesList

    def getElements(self):
        coordinatesList = self.getCoordinates()
        elementList = []

        for i, coords in enumerate(coordinatesList):
            sectionNumber = str(coords["section"])
            assignedGroup = self.elementSections.get(sectionNumber, {})

            def buildElement(name, node_i, node_j):
                group = name[0]  # M, D, or C
                assigned = assignedGroup.get(group)
                if assigned:
                    sectionType = "round" if assigned.startswith("RD") else "angular"
                    props = self.getSectionProps(sectionType, assigned)
                    secType = sectionType
                else:
                    props = self.DEFAULT_ELEMENT_PROPERTIES
                    secType = props["secction_type"]

                length = round(self.elementLength(node_i, node_j), 3)

                return {
                    "element": name,
                    "node_i": node_i,
                    "node_j": node_j,
                    "length": length,
                    "secction_type": secType,
                    "cross_area": props["cross_area"],
                    "projected_width": props["projected_width"],
                    "projected_area": round(props["projected_width"] * length, 3)
                }

            elements = [
                buildElement("M1", coords['a'], coords['e']),
                buildElement("M2", coords['e'], coords['c']),
                buildElement("M3", coords['b'], coords['f']),
                buildElement("M4", coords['f'], coords['d']),
                buildElement("D1", coords['a'], coords['g']),
                buildElement("D2", coords['g'], coords['d']),
                buildElement("D3", coords['g'], coords['b']),
                buildElement("D4", coords['g'], coords['c']),
                buildElement("C1", coords['g'], coords['e']),
                buildElement("C2", coords['g'], coords['f']),
                buildElement("T1", coords['h'], coords['m']),
                buildElement("T2", coords['m'], coords['l']),
                buildElement("S1", coords['m'], coords['n']),
                buildElement("S2", coords['m'], coords['o']),
                buildElement("S3", coords['n'], coords['e']),
                buildElement("S4", coords['o'], coords['f']),
                buildElement("D1", coords['n'], coords['a']),
                buildElement("D2", coords['n'], coords['h']),   
                buildElement("D3", coords['n'], coords['l']),
                buildElement("D4", coords['n'], coords['c']),
                buildElement("D5", coords['o'], coords['h']),
                buildElement("D6", coords['o'], coords['b']),
                buildElement("D7", coords['o'], coords['d']),
                buildElement("D8", coords['o'], coords['l']),
            ]


            elementList.append({
                "section": coords["section"],
                "elements": elements
            })

        return elementList

    def elementLength(self, node_i, node_j):
        return math.sqrt(
            (node_j[0] - node_i[0]) ** 2 +
            (node_j[1] - node_i[1]) ** 2 +
            (node_j[2] - node_i[2]) ** 2
        )

    def toJson(self, indent=4):
        return json.dumps({ 'coordinates': self.getCoordinates(), 'elements': self.getElements() }, indent=indent)

    def saveToFile(self, filename: str):
        with open(filename, 'w') as f:
            json.dump({ 'coordinates': self.getCoordinates(), 'elements': self.getElements() }, f, indent=4)
        print(f"✅ Saved tower sections to {filename}")
