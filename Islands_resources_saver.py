import os
import SaveLoadEngine

sle = SaveLoadEngine.SaveLoadEngine(os.getcwd() + "\\Islands_resources", "Islands_resources")
random_staff = ({"name": "sharp stone", "minimum": 1, "maximum": 3, "frequency": 15}, {"name": "stick", "minimum": 1, "maximum": 5, "frequency" : 50}, {"name": "very sharp stone", "minimum": 1, "maximum": 1, "frequency": 7})
sle.save(random_staff, "random_staff")