import arcpy
import os

class ToolValidator(object):

  def __init__(self):
    self.params = arcpy.GetParameterInfo()

  def initializeParameters(self):
    return

  def updateParameters(self):

    if self.params[0].value:
        try:
            input_folder = str(self.params[0].value)
            
            if os.path.exists(input_folder):
                gdb_list = [f for f in os.listdir(input_folder) if f.endswith(".gdb")]
                
                self.params[1].filter.list = gdb_list
        except Exception:
            pass
            
    return

  def updateMessages(self):
    return