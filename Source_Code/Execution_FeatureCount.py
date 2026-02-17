import arcpy
import os
import pandas as pd
def main():
    gdb_folder = arcpy.GetParameterAsText(0)
    selected_gdbs_raw = arcpy.GetParameterAsText(1)
    output_csv = arcpy.GetParameterAsText(2)
    all_data = []
    if not os.path.exists(gdb_folder):
        arcpy.AddError(f"The input folder '{gdb_folder}' does not exist.")
        return
    if selected_gdbs_raw:
        target_gdbs = [x.strip("'") for x in selected_gdbs_raw.split(';')]
    else:
        target_gdbs = [f for f in os.listdir(gdb_folder) if f.endswith(".gdb")]
    if not target_gdbs:
        arcpy.AddError("No Geodatabases selected or found.")
        return
    arcpy.AddMessage(f"Processing {len(target_gdbs)} Geodatabase(s)...")
    for gdb_name in target_gdbs:
        gdb_name = os.path.basename(gdb_name)
        city_name = gdb_name.split('_')[0].upper()
        full_path = os.path.join(gdb_folder, gdb_name)
        
        if not arcpy.Exists(full_path):
            arcpy.AddWarning(f"GDB not found: {full_path}. Skipping.")
            continue
        arcpy.env.workspace = full_path
        
        datasets = arcpy.ListDatasets(feature_type='feature') or []
        for ds in datasets:
            ds_path = os.path.join(full_path, ds)
            arcpy.env.workspace = ds_path
            fcs = arcpy.ListFeatureClasses() or []
            for fc in fcs:
                try:
                    count = int(arcpy.GetCount_management(fc).getOutput(0))
                    all_data.append({
                        'Feature Dataset': ds,
                        'Feature Class': fc,
                        'City': city_name,
                        'Count': count
                    })
                except Exception as e:
                    arcpy.AddWarning(f"Error counting {fc}: {e}")
        arcpy.env.workspace = full_path
        standalone_fcs = arcpy.ListFeatureClasses() or []
        for fc in standalone_fcs:
            try:
                count = int(arcpy.GetCount_management(fc).getOutput(0))
                all_data.append({
                    'Feature Dataset': 'None',
                    'Feature Class': fc,
                    'City': city_name,
                    'Count': count
                })
            except Exception as e:
                arcpy.AddWarning(f"Error counting {fc}: {e}")
    if not all_data:
        arcpy.AddWarning("No data found to export.")
        return
    df = pd.DataFrame(all_data)
    pivot_df = df.pivot_table(
        index=['Feature Dataset', 'Feature Class'],
        columns='City',
        values='Count',
        fill_value=0
    ).reset_index()
    pivot_df['sort_rank'] = pivot_df['Feature Dataset'].apply(lambda x: 1 if x == 'None' else 0)
    pivot_df = pivot_df.sort_values(by=['sort_rank', 'Feature Dataset', 'Feature Class'])
    pivot_df = pivot_df.drop(columns=['sort_rank'])
    try:
        pivot_df.to_csv(output_csv, index=False)
        arcpy.AddMessage(f"Successfully exported results to: {output_csv}")
        aprx = arcpy.mp.ArcGISProject("CURRENT")
        active_map = aprx.activeMap
        
        if active_map:
            active_map.addDataFromPath(output_csv)
            arcpy.AddMessage("Table added to the Contents pane.")
        else:
            arcpy.AddWarning("No active map found. Table could not be added to the Contents pane automatically.")
        
    except Exception as e:
        arcpy.AddError(f"Failed to write CSV: {e}. Check if the file is open.")
if __name__ == "__main__":
    main()
