import arcpy
import os
import csv
from collections import defaultdict

def main():
    input_folder = arcpy.GetParameterAsText(0)
    selected_gdbs_input = arcpy.GetParameterAsText(1)
    selected_rules_input = arcpy.GetParameterAsText(2) 
    raw_output = arcpy.GetParameterAsText(3)
    
    in_len_str = arcpy.GetParameterAsText(4)   
    in_poly_str = arcpy.GetParameterAsText(5)  
    in_bldg_str = arcpy.GetParameterAsText(6)  

    selected_gdbs = []
    if selected_gdbs_input and selected_gdbs_input.strip() != "":
        names = [n.replace("'", "").strip() for n in selected_gdbs_input.split(';')]
        selected_gdbs = [os.path.join(input_folder, n) for n in names]
    else:
        if input_folder and os.path.exists(input_folder):
            selected_gdbs = [os.path.join(input_folder, f) for f in os.listdir(input_folder) 
                             if f.lower().endswith(".gdb")]

    def parse_linear_to_meters(s, default):
        try:
            p = s.replace("'", "").split()
            v = float(p[0])
            u = p[1].lower() if len(p) > 1 else "meters"
            return v * 0.3048 if "foot" in u or "feet" in u else v
        except: return default

    def parse_area_to_sqm(s, default):
        try:
            p = s.replace("'", "").split()
            v = float(p[0])
            u = p[1].lower() if len(p) > 1 else "squaremeters"
            return v * 0.092903 if "feet" in u else v
        except: return default

    L_LIMIT = parse_linear_to_meters(in_len_str, 1.0)
    A_LIMIT = parse_area_to_sqm(in_poly_str, 5.0)
    B_LIMIT = parse_area_to_sqm(in_bldg_str, 5.0)

    FC_STRUCTURE = {
        "All_lines": "Base_ULU", "All_polygons": "Base_ULU", "Buildings": "Base_ULU",
        "Bus_Stop_Pnt": "Base_ULU", "Communication_Pnt": "Base_ULU",
        "Community_toilet": "Base_ULU", "Tree": "Base_ULU", "land_use": "Base_ULU",
        "Water_NW_Pnt": "Utilities", "Power_NW_Pnt": "Utilities",
    }

    def get_fc_path(gdb, fc_name):
        dataset = FC_STRUCTURE.get(fc_name)
        return os.path.join(gdb, dataset, fc_name) if dataset else os.path.join(gdb, fc_name)

    def manual_check(gdb): return "" 

    def check_duplicates(gdb, fc_name):
        try:
            fc_path = get_fc_path(gdb, fc_name)
            if arcpy.Exists(fc_path):
                out_table = r"memory\temp_ident_" + fc_name
                arcpy.management.FindIdentical(fc_path, out_table, ["Shape"], xy_tolerance="0.01 Meters")
                seqs = [row[0] for row in arcpy.da.SearchCursor(out_table, "FEAT_SEQ")]
                arcpy.Delete_management(out_table)
                return len(seqs) - len(set(seqs))
            return "Layer Missing"
        except: return "Error"

    def rule_dangles(gdb):
        dataset_name = "Base_ULU"
        topo_name = "Temp_Dangle_Topo"
        fd_path = os.path.join(gdb, dataset_name)
        lines_path = os.path.join(fd_path, "All_lines")
        topo_path = os.path.join(fd_path, topo_name)
        temp_err_point = os.path.join(fd_path, "temp_error_point")
        temp_buffer = r"memory\dangle_buffer"
        temp_join = r"memory\dangle_join"
        if not arcpy.Exists(lines_path): return "Layer Missing"
        try:
            if arcpy.Exists(topo_path): arcpy.management.Delete(topo_path)
            if arcpy.Exists(temp_err_point): arcpy.management.Delete(temp_err_point)
            arcpy.management.CreateTopology(fd_path, topo_name)
            arcpy.management.AddFeatureClassToTopology(topo_path, lines_path, 1, 1)
            arcpy.management.AddRuleToTopology(topo_path, "Must Not Have Dangles (Line)", lines_path)
            arcpy.management.ValidateTopology(topo_path)
            arcpy.management.ExportTopologyErrors(topo_path, fd_path, "temp_error")
            dangle_count = 0
            if arcpy.Exists(temp_err_point):
                arcpy.analysis.Buffer(temp_err_point, temp_buffer, "0.3 Meters")
                arcpy.analysis.SpatialJoin(temp_buffer, lines_path, temp_join, "JOIN_ONE_TO_ONE", "KEEP_ALL", match_option="INTERSECT")
                lyr = "dangle_lyr"
                arcpy.management.MakeFeatureLayer(temp_join, lyr, "Join_Count > 1")
                dangle_count = int(arcpy.management.GetCount(lyr)[0])
                arcpy.management.Delete(lyr)
            arcpy.management.Delete(topo_path)
            for suffix in ["_point", "_line", "_poly"]:
                fc = os.path.join(fd_path, f"temp_error{suffix}")
                if arcpy.Exists(fc): arcpy.management.Delete(fc)
            arcpy.management.Delete(temp_buffer)
            arcpy.management.Delete(temp_join)
            return dangle_count
        except: 
            if arcpy.Exists(topo_path): arcpy.management.Delete(topo_path)
            return "Error"
    
    def check_small_area(gdb, fc_name, limit):
        try:
            fc_path = get_fc_path(gdb, fc_name)
            if arcpy.Exists(fc_path):
                count = sum(1 for row in arcpy.da.SearchCursor(fc_path, ["SHAPE@AREA"]) if row[0] <= limit)
                return count
            return "Layer Missing"
        except: return "Error"

    def rule_generic_spatial(gdb, target_fc, overlay_fc, option="INTERSECT", query=None, overlay_query=None):
        try:
            t_path = get_fc_path(gdb, target_fc); o_path = get_fc_path(gdb, overlay_fc)
            if arcpy.Exists(t_path) and arcpy.Exists(o_path):
                arcpy.MakeFeatureLayer_management(t_path, "t_lyr", query)
                arcpy.MakeFeatureLayer_management(o_path, "o_lyr", overlay_query)
                arcpy.SelectLayerByLocation_management("t_lyr", option, "o_lyr")
                count = int(arcpy.GetCount_management("t_lyr")[0])
                arcpy.Delete_management("t_lyr"); arcpy.Delete_management("o_lyr")
                return count
            return "Layer Missing"
        except: return "Error"

    def rule_aqua_conflicts(gdb):
        try:
            poly = get_fc_path(gdb, "All_polygons")
            if arcpy.Exists(poly):
                temp = "lyr_aqua"; buf = r"memory\aqua_buf"
                arcpy.MakeFeatureLayer_management(poly, temp, "Sub_Class = 'Aquaculture'")
                arcpy.Buffer_analysis(temp, buf, "-0.01 Meters")
                res = []
                for fc, q, lbl in [(get_fc_path(gdb, "Buildings"), None, "Bld"), 
                                   (get_fc_path(gdb, "All_lines"), "Class=1", "Rd"), 
                                   (get_fc_path(gdb, "Tree"), None, "Tree")]:
                    c = 0
                    if arcpy.Exists(fc):
                        lyr = "temp_check"
                        arcpy.MakeFeatureLayer_management(fc, lyr, q)
                        arcpy.SelectLayerByLocation_management(lyr, "INTERSECT", buf)
                        c = int(arcpy.GetCount_management(lyr)[0])
                        arcpy.Delete_management(lyr)
                    res.append(f"{lbl}:{c}")
                arcpy.Delete_management(temp); arcpy.Delete_management(buf)
                return " | ".join(res)
        except: return "Error"

    def rule_bridge_flyover(gdb):
        try:
            lines = get_fc_path(gdb, "All_lines")
            if arcpy.Exists(lines):
                arcpy.MakeFeatureLayer_management(lines, "target", "Class = 1")
                arcpy.MakeFeatureLayer_management(lines, "bridge", "Class = 3")
                arcpy.MakeFeatureLayer_management(lines, "fly", "Class = 4")
                arcpy.SelectLayerByLocation_management("bridge", "CROSSED_BY_THE_OUTLINE_OF", "target")
                c1 = int(arcpy.GetCount_management("bridge")[0])
                arcpy.SelectLayerByLocation_management("fly", "CROSSED_BY_THE_OUTLINE_OF", "target")
                c2 = int(arcpy.GetCount_management("fly")[0])
                arcpy.Delete_management("target"); arcpy.Delete_management("bridge"); arcpy.Delete_management("fly")
                return f"Bridge:{c1} | Flyover:{c2}"
        except: return "Error"

    ALL_RULES = [
        (1, "No Gaps", manual_check),
        (2, "No overlaps in each layer", manual_check),
        (3, "Buildings crossing Landuse polygons", lambda g: rule_generic_spatial(g, "Buildings", "All_polygons", "CROSSED_BY_THE_OUTLINE_OF")),
        (4, "Buildings on Waterbody class", lambda g: rule_generic_spatial(g, "Buildings", "All_polygons", "INTERSECT", None, "Class = 5")),
        (5, "Buildings, Roads, Trees in Aquaculture", rule_aqua_conflicts),
        (6, "Building overlap", manual_check),
        (7, "Buildings on Vacant lands", lambda g: rule_generic_spatial(g, "Buildings", "All_polygons", "INTERSECT", None, "Class = 23")),
        (8, "Road crossing Building", lambda g: rule_generic_spatial(g, "All_lines", "Buildings", "CROSSED_BY_THE_OUTLINE_OF", "Class = 1")),
        (9, "Road class in place of Residential", lambda g: rule_generic_spatial(g, "All_lines", "Buildings", "INTERSECT", "Class = 1", "Class = 6")),
        (10, "Bridges / Flyovers (all sub-classes) crossing Road", rule_bridge_flyover),
        (11, f"Small Length in All_Lines (<={L_LIMIT:.3f}m)", lambda g: rule_generic_spatial(g, "All_lines", "All_lines", "INTERSECT", f"Shape_Length <= {L_LIMIT}")),
        (12, "Trees on Roads", lambda g: rule_generic_spatial(g, "Tree", "All_lines", "INTERSECT", None, "Class = 1")),
        (13, "Trees on Buildings", lambda g: rule_generic_spatial(g, "Tree", "Buildings", "INTERSECT")),
        (14, "Dangles in Lines", rule_dangles),
        (15, "Cutbacks in Polygons", manual_check),
        (16, "Cutbacks in Lines", manual_check),
        (17, "Cutbacks in Buildings", manual_check),
        (18, "Slivers in Buildings", manual_check),
        (19, "Slivers in Polygons", manual_check),
        (20, f"Small area in Buildings (<={B_LIMIT:.3f}sqm)", lambda g: check_small_area(g, "Buildings", B_LIMIT)),
        (21, f"Small areas in Polygons (<={A_LIMIT:.3f}sqm)", lambda g: check_small_area(g, "All_polygons", A_LIMIT)),
        (22, "Duplicates in Trees", lambda g: check_duplicates(g, "Tree")),
        (23, "Duplicates in Buildings", lambda g: check_duplicates(g, "Buildings")),
        (24, "Duplicates in Polygons", lambda g: check_duplicates(g, "All_polygons")),
        (25, "Duplicates in Lines", lambda g: check_duplicates(g, "All_lines")),
        (26, "Duplicates in Water-NW Points", lambda g: check_duplicates(g, "Water_NW_Pnt")),
        (27, "Duplicates in Power-NW Points", lambda g: check_duplicates(g, "Power_NW_Pnt")),
        (28, "Duplicates in Community-Toilet", lambda g: check_duplicates(g, "Community_toilet")),
        (29, "Bus stop point on Buildings", lambda g: rule_generic_spatial(g, "Bus_Stop_Pnt", "Buildings", "INTERSECT")),
        (30, "Communication point on Buildings", lambda g: rule_generic_spatial(g, "Communication_Pnt", "Buildings", "INTERSECT")),
        (31, "Gap in data at Area Boundary Limit (AOI)", manual_check)
    ]

    RULES_TO_RUN = []
    if selected_rules_input:
        targets = [r.replace("'", "").strip() for r in selected_rules_input.split(';')]
        for rule in ALL_RULES:
            clean_name = rule[1].split(" (<=")[0]
            if any(t.split(". ", 1)[-1].startswith(clean_name) for t in targets): 
                RULES_TO_RUN.append(rule)
    if not RULES_TO_RUN: RULES_TO_RUN = ALL_RULES

    total_steps = len(selected_gdbs) * len(RULES_TO_RUN)
    arcpy.SetProgressor("step", "Analyzing...", 0, total_steps, 1)

    matrix_data = defaultdict(dict)
    city_names = []
    for gdb_path in selected_gdbs:
        city = os.path.basename(gdb_path).split('_')[0].upper()
        city_names.append(city)
        for orig_sno, name, func in RULES_TO_RUN:
            arcpy.SetProgressorLabel(f"{city}: {name}")
            matrix_data[orig_sno][city] = func(gdb_path)
            arcpy.SetProgressorPosition()

    output_path = raw_output if ".csv" in raw_output.lower() else raw_output + ".csv"
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["S.No", "Validation Rule"] + city_names)
        for i, (orig_sno, name, _) in enumerate(RULES_TO_RUN, 1):
            row = [i, name]
            for city in city_names:
                row.append(matrix_data[orig_sno].get(city, "N/A"))
            writer.writerow(row)

    try:
        aprx = arcpy.mp.ArcGISProject("CURRENT")
        if aprx.activeMap:
            aprx.activeMap.addDataFromPath(output_path)
    except: pass

if __name__ == "__main__": main()