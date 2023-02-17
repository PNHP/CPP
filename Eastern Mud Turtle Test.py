######################################################################################################################################################
# Eastern Mud Turtle Core
######################################################################################################################################################

# Define the tool
class EasternMudTurtleCore(object):
    def __init__(self):
        self.label = "Eastern Mud Turtle Core"
        self.description = ""
        self.canRunInBackground = False
        self.category = "Reptiles"
        self.params = [
            parameter("EO ID of record for which you are creating CPP:", "eoid", "GPLong"),
            parameter("Core CPP Layer", "cpp_core", "GPFeatureLayer", cpp_core_path),
            parameter("NWI Layer", "NWI", "GPFeatureLayer"),
            parameter("NHD Waterbodies", "waterbodies", "GPFeatureLayer")]

    def getParameterInfo(self):
        return self.params

# define parameters
    def execute(self, params, messages):
        eoid = params[0].valueAsText
        cpp_core = params[1].valueAsText
        NWI = params[2].valueAsText
        waterbodies = params[3].valueAsText

        specID = "Reptiles_Eastern_Mud_Turtle_20130515"

        merge_features = []

        arcpy.AddMessage("create layers")
        NWI_lyr = arcpy.MakeFeatureLayer_management(NWI, "NWI_lyr", "WETLAND_TYPE <> 'Riverine'")
        waterbodies_lyr = arcpy.MakeFeatureLayer_management(waterbodies, "waterbodies_lyr")

        arcpy.AddMessage("select NWI wetlands")
        arcpy.SelectLayerByLocation_management(NWI_lyr, "INTERSECT", habitat, 300, "NEW_SELECTION")
        arcpy.SelectLayerByLocation_management(NWI_lyr, "INTERSECT", nwi, "", "SUBSET_SELECTION")
        nwi_buff = arcpy.Buffer_analysis(NWI_lyr, "memory\\nwi_buff", 300, "", "", "ALL")
        merge_features.append(nwi_buff)

        arcpy.AddMessage("select NHD waterbodies")
        arcpy.SelectLayerByLocation_management(waterbodies_lyr, "INTERSECT", habitat, 300, "NEW_SELECTION")
        arcpy.SelectLayerByLocation_management(waterbodies_lyr, "INTERSECT", nwi, "", "SUBSET_SELECTION")
        waterbodies_nwi_buff = arcpy.Buffer_analysis(waterbodies_lyr, "memory\\waterbodies_nwi_buff", 300, "", "", "ALL")
        merge_features.append(waterbodies_nwi_buff)

        arcpy.AddMessage("merge features")
        merge_lyr = arcpy.Merge_management(merge_features, "memory\\merge_lyr")
        dissolve_lyr = arcpy.Dissolve_management(merge_lyr, "memory\\dissolve_lyr")
        with arcpy.da.SearchCursor(dissolve_lyr, "SHAPE@") as cursor:
            for row in cursor:
                geom = row[0]

        values = calc_attr_core(eoid, eo_ptreps, specID)
        values.append(geom)
        fields = ["SNAME", "EO_ID", "DrawnBy", "DrawnDate", "DrawnNotes", "Status", "SpecID", "ELSUBID",
                  "BioticsExportDate",
                  "SHAPE@"]
        with arcpy.da.InsertCursor(cpp_core, fields) as cursor:
            cursor.insertRow(values)


