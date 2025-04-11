import numpy as np
import json
import math

class Section:

    def __init__(self, towerData, elementSections=None, sectionLibrary=None):
        self.towerData = towerData
        self.elementSections = elementSections or {}  # maps section → element → name
        self.sectionLibrary = sectionLibrary or {}    # maps round/angular data
        self._validateInputs()

    def _validateInputs(self):
        requiredKeys = ["Tower_Base_Width", "Top_Width", "Height", "Variable_Segments", "Constant_Segments"]
        for key in requiredKeys:
            if key not in self.towerData:
                raise ValueError(f"Missing required parameter: {key}")
            
    DEFAULT_ELEMENT_PROPERTIES = {
        "secction_type": "round",
        "cross_area": 1222.6,             # mm²
        "projected_width": 0.0508,        # meters
        "density": 7850,                  # kg/m³
        "young_modulus": 200000,          # MPa (N/mm²)
        "moment_of_inertia": 275000.0     # mm⁴
        }

    def getSectionProps(self, sectionType: str, sectionName: str):
        if sectionType not in self.sectionLibrary:
            return self.DEFAULT_ELEMENT_PROPERTIES

        for entry in self.sectionLibrary[sectionType]:
            if entry["name"] == sectionName:
                return entry

        return self.DEFAULT_ELEMENT_PROPERTIES


    def getCoordinates(self):
        
        baseWidth = self.towerData["Tower_Base_Width"]
        topWidth = self.towerData["Top_Width"]
        totalHeight = self.towerData["Height"]
        variableSegments = self.towerData["Variable_Segments"]
        constantSegments = self.towerData["Constant_Segments"]

        segmentHeight = totalHeight / (variableSegments + constantSegments)
        taperDelta = (baseWidth - topWidth) / 2
        alpha = np.arctan(taperDelta / (variableSegments*segmentHeight))

        currentBase = baseWidth
        coordinatesList = []
        secction_init_x = 0.0 
        secction_init_y = 0.0

        for i in range(variableSegments):

            sectionNumber = i + 1  # start from 1

            segmentDelta = np.tan(alpha) * segmentHeight
            phi = np.arctan(segmentHeight / (currentBase - segmentDelta))
            gHeight = np.tan(phi) * (currentBase / 2)
            deltaG = gHeight * np.tan(alpha)

        
            localCoords = {
                'section': sectionNumber,
                'a': [round((0.0 + secction_init_x),3), round((0.0 + secction_init_y),3)],
                'b': [round(currentBase + secction_init_x, 3), 0.0 + secction_init_y],
                'c': [round(segmentDelta +secction_init_x, 3), round(segmentHeight + secction_init_y, 3)],
                'd': [round((currentBase - segmentDelta) + secction_init_x, 3), round(segmentHeight + secction_init_y, 3)],
                'e': [round(deltaG + secction_init_x, 3), round(gHeight + secction_init_y, 3)],
                'f': [round((currentBase - deltaG) + secction_init_x, 3), round(gHeight + secction_init_y, 3)],
                'g': [round((currentBase / 2) + secction_init_x, 3), round(gHeight + secction_init_y, 3)],
            }

            coordinatesList.append(localCoords)
            currentBase -= segmentDelta * 2
            secction_init_x = secction_init_x + round(segmentDelta, 3)
            secction_init_y = secction_init_y + round(segmentHeight, 3)
        
        for i in range(constantSegments):
            
            sectionNumber = sectionNumber + 1

            localCoords = {
                'section': sectionNumber,
                'a': [round((0.0 + secction_init_x),3), round((0.0 + secction_init_y),3)],
                'b': [round(currentBase + secction_init_x, 3), (0.0 + secction_init_y)],
                'c': [round(secction_init_x, 3), round(segmentHeight + secction_init_y, 3)],
                'd': [round(currentBase + secction_init_x, 3), round(segmentHeight + secction_init_y, 3)],
                'e': [round(secction_init_x, 3), round((segmentHeight/2) + secction_init_y, 3)],
                'f': [round((currentBase) + secction_init_x, 3), round((segmentHeight/2) + secction_init_y, 3)],
                'g': [round((currentBase / 2) + secction_init_x, 3), round((segmentHeight/2) + secction_init_y, 3)],
            }

            coordinatesList.append(localCoords)
            secction_init_y = secction_init_y + round(segmentHeight, 3)

        return coordinatesList
    
    def getElements(self):

        coordinatesList = self.getCoordinates()
        elementList = []

        for i in range(len(coordinatesList)):

            sectionNumber = str(coordinatesList[i]["section"])

            assignedElements = self.elementSections.get(sectionNumber, {})

            def buildElement(name, node_i, node_j):

                assigned = assignedElements.get(name, None)

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
                buildElement("M1", coordinatesList[i]['a'], coordinatesList[i]['e']),
                buildElement("M2", coordinatesList[i]['e'], coordinatesList[i]['c']),
                buildElement("M3", coordinatesList[i]['b'], coordinatesList[i]['f']),
                buildElement("M4", coordinatesList[i]['f'], coordinatesList[i]['d']),
                buildElement("D1", coordinatesList[i]['a'], coordinatesList[i]['g']),
                buildElement("D2", coordinatesList[i]['g'], coordinatesList[i]['d']),
                buildElement("D3", coordinatesList[i]['g'], coordinatesList[i]['b']),
                buildElement("D4", coordinatesList[i]['g'], coordinatesList[i]['c']),
                buildElement("C1", coordinatesList[i]['g'], coordinatesList[i]['e']),
                buildElement("C2", coordinatesList[i]['g'], coordinatesList[i]['f']),
            ]

            elementList.append({
                "section": coordinatesList[i]["section"],
                "elements": elements
            })

        return elementList

    
    def elementLength (self, node_i, node_j):

        x1 = node_i[0]
        y1 = node_i[1]
        x2 = node_j[0]
        y2 = node_j[1]

        length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        return length


    def toJson(self, indent=4):

        coordinates = self.getCoordinates()
        elements = self.getElements()

        return json.dumps({ 'coordinates': coordinates, 'elements': elements }, indent=indent)

    def saveToFile(self, filename: str):

        coordinates = self.getCoordinates()
        elements = self.getElements()

        with open(filename, 'w') as f:
            json.dump({ 'coordinates': coordinates, 'elements': elements }, f, indent=4)
        print(f"Saved tower sections to {filename}")

if __name__ == "__main__":
    towerData = {
        "Tower_Base_Width": 3.6,
        "Top_Width": 2,
        "Height": 29.3,
        "Variable_Segments": 8,
        "Constant_Segments": 2
    }

    section = Section(towerData)
    print(section.toJson())
    section.saveToFile("tower_sections.json")
