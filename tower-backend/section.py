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

        for i in range(variableSegments):
            sectionNumber = i + 1
            segmentDelta = np.tan(alpha) * segmentHeight
            phi = np.arctan(segmentHeight / (currentBase - segmentDelta))
            gHeight = np.tan(phi) * (currentBase / 2)
            deltaG = gHeight * np.tan(alpha)

            localCoords = {
                'section': sectionNumber,
                'a': [round(0.0 + secction_init_x, 3), round(0.0 + secction_init_y, 3)],
                'b': [round(currentBase + secction_init_x, 3), round(0.0 + secction_init_y, 3)],
                'c': [round(segmentDelta + secction_init_x, 3), round(segmentHeight + secction_init_y, 3)],
                'd': [round((currentBase - segmentDelta) + secction_init_x, 3), round(segmentHeight + secction_init_y, 3)],
                'e': [round(deltaG + secction_init_x, 3), round(gHeight + secction_init_y, 3)],
                'f': [round((currentBase - deltaG) + secction_init_x, 3), round(gHeight + secction_init_y, 3)],
                'g': [round((currentBase / 2) + secction_init_x, 3), round(gHeight + secction_init_y, 3)],
            }

            coordinatesList.append(localCoords)
            currentBase -= segmentDelta * 2
            secction_init_x += round(segmentDelta, 3)
            secction_init_y += round(segmentHeight, 3)

        for i in range(constantSegments):
            sectionNumber += 1
            localCoords = {
                'section': sectionNumber,
                'a': [round(0.0 + secction_init_x, 3), round(0.0 + secction_init_y, 3)],
                'b': [round(currentBase + secction_init_x, 3), round(0.0 + secction_init_y, 3)],
                'c': [round(secction_init_x, 3), round(segmentHeight + secction_init_y, 3)],
                'd': [round(currentBase + secction_init_x, 3), round(segmentHeight + secction_init_y, 3)],
                'e': [round(secction_init_x, 3), round((segmentHeight/2) + secction_init_y, 3)],
                'f': [round(currentBase + secction_init_x, 3), round((segmentHeight/2) + secction_init_y, 3)],
                'g': [round((currentBase / 2) + secction_init_x, 3), round((segmentHeight/2) + secction_init_y, 3)],
            }

            coordinatesList.append(localCoords)
            secction_init_y += round(segmentHeight, 3)

        return coordinatesList

    def getElements(self):
        coordinatesList = self.getCoordinates()
        elementList = []

        for i, coords in enumerate(coordinatesList):
            sectionNumber = str(coords["section"])
            assignedElements = self.elementSections.get(sectionNumber, {})

            def buildElement(name, node_i, node_j):
                assigned = assignedElements.get(name)
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
                    "lenght": length,
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
            ]

            elementList.append({
                "section": coords["section"],
                "elements": elements
            })

        return elementList

    def elementLength(self, node_i, node_j):
        return math.sqrt((node_j[0] - node_i[0]) ** 2 + (node_j[1] - node_i[1]) ** 2)

    def toJson(self, indent=4):
        return json.dumps({ 'coordinates': self.getCoordinates(), 'elements': self.getElements() }, indent=indent)

    def saveToFile(self, filename: str):
        with open(filename, 'w') as f:
            json.dump({ 'coordinates': self.getCoordinates(), 'elements': self.getElements() }, f, indent=4)
        print(f"✅ Saved tower sections to {filename}")
