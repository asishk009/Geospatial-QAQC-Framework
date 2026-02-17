import arcpy
import os

class ToolValidator(object):
    def __init__(self):
        self.params = arcpy.GetParameterInfo()

    def initializeParameters(self):
        if not self.params[4].value: self.params[4].value = "1 Meters"
        if not self.params[5].value: self.params[5].value = "5 SquareMeters"
        if not self.params[6].value: self.params[6].value = "5 SquareMeters"

        self.params[2].filter.list = [
            "1. No Gaps", "2. No overlaps in each layer", "3. Buildings crossing Landuse polygons",
            "4. Buildings on Waterbody class", "5. Buildings, Roads, Trees in Aquaculture",
            "6. Building overlap", "7. Buildings on Vacant lands", "8. Road crossing Building",
            "9. Road class in place of Residential", "10. Bridges / Flyovers (all sub-classes) crossing Road",
            "11. Small Length in All_Lines", "12. Trees on Roads", "13. Trees on Buildings",
            "14. Dangles in Lines", "15. Cutbacks in Polygons", "16. Cutbacks in Lines",
            "17. Cutbacks in Buildings", "18. Slivers in Buildings", "19. Slivers in Polygons",
            "20. Small area in Buildings", "21. Small areas in Polygons", "22. Duplicates in Trees",
            "23. Duplicates in Buildings", "24. Duplicates in Polygons", "25. Duplicates in Lines",
            "26. Duplicates in Water-NW Points", "27. Duplicates in Power-NW Points",
            "28. Duplicates in Community-Toilet", "29. Bus stop point on Buildings",
            "30. Communication point on Buildings", "31. Gap in data at Area Boundary Limit (AOI)"
        ]

    def updateParameters(self):
        if self.params[0].altered:
            folder = str(self.params[0].value)
            if folder and os.path.exists(folder):
                gdbs = [f for f in os.listdir(folder) if f.lower().endswith(".gdb")]
                self.params[1].filter.list = gdbs
        
        if not self.params[1].value:
            self.params[1].description = "Select Geodatabases (Leave empty to process ALL in folder)"
        else:
            self.params[1].description = "Select Geodatabases"

    def updateMessages(self):
        return