import numpy as np
import json

class Section:
    def __init__(self, towerData):
        self.towerData = towerData
        self._validateInputs()

    def _validateInputs(self):
        requiredKeys = ["Tower_Base_Width", "Top_Width", "Height", "Variable_Segments", "Constant_Segments"]
        for key in requiredKeys:
            if key not in self.towerData:
                raise ValueError(f"Missing required parameter: {key}")

    def getCoordinates(self):
        
        baseWidth = self.towerData["Tower_Base_Width"]
        topWidth = self.towerData["Top_Width"]
        totalHeight = self.towerData["Height"]
        variableSegments = self.towerData["Variable_Segments"]
        constantSegments = self.towerData["Constant_Segments"]

        segmentHeight = totalHeight / (variableSegments + constantSegments)
        taperDelta = (baseWidth - topWidth) / 2
        alpha = np.arctan(taperDelta / totalHeight)

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

        return coordinatesList

    def toJson(self, indent=4):
        return json.dumps(self.getCoordinates(), indent=indent)

    def saveToFile(self, filename: str):
        with open(filename, 'w') as f:
            json.dump(self.getCoordinates(), f, indent=4)
        print(f"Saved tower sections to {filename}")

if __name__ == "__main__":
    towerData = {
        "Tower_Base_Width": 3.0,
        "Top_Width": 2.0,
        "Height": 24.0,
        "Variable_Segments": 3,
        "Constant_Segments": 1
    }

    section = Section(towerData)
    print(section.toJson())
    section.saveToFile("tower_sections.json")
