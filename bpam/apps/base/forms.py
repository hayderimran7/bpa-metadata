# coding=utf-8
from django import forms

KINGDOMS = (('Bacteria', 'Bacteria'),
                ('Archea', 'Archea'),
                ('Eukaryote', 'Eukaryote'),
                ('Fungi', 'Fungi'))


class OTUSearchForm(forms.Form):


    search_field = forms.ChoiceField(choices=[
                            ("----", "----"),
                            ("sample_id", "Sample Id"),
                            ("date_sampled", "Date sampled"),
                            ("lat", "Latitude"),
                            ("lon", "Longitude"),
                            ("depth", "Soil Depth"),
                            ("description", "Description"),  # Horizon Description?
                            ("current_land_use", "Current land-use"),
                            ("general_ecological_zone", "General Ecological Zone"),
                            ("vegetation_type", "Vegetation Type"),
                            ("vegetation_total_cover", "Vegetation Total cover (%)"),
                            ("vegetation_dominant_trees", "Vegetation Dom. Trees"),
                            #("Vegetation Dom. Shrubs", "Vegetation Dom. Shrubs"),
                            #("Vegetation Dom. Grasses", "Vegetation Dom. Grasses"),
                            ("elevation", "Elevation (m)"),
                            ("australian_soil_classification", "Australian Soil Classification"),
                            ("fao_soil_type", "FAO soil classification"),
                            ("immediate_previous_land_use", "Immediate Previous Land Use"),
                            ("agrochemical_additions", "Agrochemical Additions"),
                            ("tillage", "Tillage"),
                            ("fire_history", "Fire History"),
                            ("fire_intensity","Fire Intensity"),
                            #("flooding", "")
                            ("environment_events", "Environment Events"),
                            ("moisture", "Soil moisture (%)"),
                            ("colour", "Soil Colour"),
                            ("texture", "Texture"),
                            ("gravel", "Gravel (%) - ( >2.0 mm)"),
                            ("course_sand", "Course Sand (%) (200-2000 µm)"),
                            ("fine_sand", "Fine Sand (%) - (20-200 µm)"),
                            ("sand", "Sand (%)"),
                            ("silt", "Silt (%) (2-20 µm)"),
                            ("clay", "Clay (%) (<2 µm)"),
                            ("ammonium_nitrogen", "Ammonium Nitrogen (mg/Kg)"),
                            ("nitrate_nitrogen", "Nitrate Nitrogen (mg/Kg)"),
                            ("phosphorus_colwell", "Phosphorus Colwell (mg/Kg)"),
                            ("potassium_colwell", "Potassium Colwell (mg/Kg)"),
                            ("sulphur_colwell", "Sulphur (mg/Kg)"),
                            ("organic_carbon", "Organic Carbon (%)"),
                            ("conductivity", "Conductivity (dS/m)"),
                            ("cacl2_ph", "pH Level (CaCl2) (pH)"),
                            ("h20_ph", "pH Level (H2O) (pH)"),
                            ("dtpa_copper", "DTPA Copper (mg/Kg)"),
                            ("dtpa_iron", "DTPA Iron (mg/Kg)"),
                            ("dtpa_manganese", "DTPA Manganese (mg/Kg)"),
                            ("dtpa_zinc", "DTPA Zinc (mg/Kg)"),
                            ("exc_aluminium", "Exc. Aluminium (meq/100g)"),
                            ("exc_calcium", "Exc. Calcium (meq/100g)"),
                            ("exc_magnesium", "Exc. Magnesium (meq/100g)"),
                            ("exc_potassium", "Exc. Potassium (meq/100g)"),
                            ("exc_sodium", "Exc. Sodium (meq/100g)"),
                            ("boron_hot_cacl2", "Boron Hot CaCl2 (mg/Kg)"),
                            ("total_nitrogen", "Total Nitrogen"),
                            ("total_carbon", "Total Carbon"),
                            ])


    search_value = forms.CharField(max_length=100)

    search_range = forms.ChoiceField(choices=[
                            ("----", "----"),
                            ("lat", "Latitude"),
                            ("lon", "Longitude"),
                            ("depth", "Soil Depth"),
                            ("elevation", "Elevation (m)"),
                            ("texture", "Texture"),
                            ("gravel", "Gravel (%) - ( >2.0 mm)"),
                            ("course_sand", "Course Sand (%) (200-2000 µm)"),
                            ("fine_sand", "Fine Sand (%) - (20-200 µm)"),
                            ("sand", "Sand (%)"),
                            ("silt", "Silt (%) (2-20 µm)"),
                            ("clay", "Clay (%) (<2 µm)"),
                            ("ammonium_nitrogen", "Ammonium Nitrogen (mg/Kg)"),
                            ("nitrate_nitrogen", "Nitrate Nitrogen (mg/Kg)"),
                            ("phosphorus_colwell", "Phosphorus Colwell (mg/Kg)"),
                            ("potassium_colwell", "Potassium Colwell (mg/Kg)"),
                            ("sulphur_colwell", "Sulphur (mg/Kg)"),
                            ("organic_carbon", "Organic Carbon (%)"),
                            ("conductivity", "Conductivity (dS/m)"),
                            ("cacl2_ph", "pH Level (CaCl2) (pH)"),
                            ("h20_ph", "pH Level (H2O) (pH)"),
                            ("dtpa_copper", "DTPA Copper (mg/Kg)"),
                            ("dtpa_iron", "DTPA Iron (mg/Kg)"),
                            ("dtpa_manganese", "DTPA Manganese (mg/Kg)"),
                            ("dtpa_zinc", "DTPA Zinc (mg/Kg)"),
                            ("exc_aluminium", "Exc. Aluminium (meq/100g)"),
                            ("exc_calcium", "Exc. Calcium (meq/100g)"),
                            ("exc_magnesium", "Exc. Magnesium (meq/100g)"),
                            ("exc_potassium", "Exc. Potassium (meq/100g)"),
                            ("exc_sodium", "Exc. Sodium (meq/100g)"),
                            ("boron_hot_cacl2", "Boron Hot CaCl2 (mg/Kg)"),
                            ("total_nitrogen", "Total Nitrogen"),
                            ("total_carbon", "Total Carbon")])
    search_range_min = forms.DecimalField()
    search_range_max = forms.DecimalField()

    search_kingdom = forms.ChoiceField(choices=KINGDOMS)
    search_phylum = forms.CharField(max_length=100)
    search_class = forms.CharField(max_length=100)
    search_order = forms.CharField(max_length=100)
    search_family = forms.CharField(max_length=100)
    search_genus = forms.CharField(max_length=100)
    search_species = forms.CharField(max_length=100)
