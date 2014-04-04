# coding=utf-8
from django import forms

class OTUSearchForm(forms.Form):
    search = forms.ChoiceField(choices=[
                            ("Sample_id", "Sample_id"),
                            ("Date sampled", "Date sampled"),
                            ("lat (-)", "lat (-)"),
                            ("lon", "lon"),
                            ("Depth", "Depth"),
                            ("Horizon", "Horizon"),
                            ("Description", "Description"),
                            ("Current land-use", "Current land-use"),
                            ("General Ecological Zone", "General Ecological Zone"),
                            ("Vegetation Type", "Vegetation Type"),
                            ("Vegetation Total cover (%)", "Vegetation Total cover (%)"),
                            ("Vegetation Dom. Trees", "Vegetation Dom. Trees"),
                            ("Vegetation Dom. Shrubs", "Vegetation Dom. Shrubs"),
                            ("Vegetation Dom. Grasses", "Vegetation Dom. Grasses"),
                            ("Elevation (m)", "Elevation (m)"),
                            #("Slope (%)", "Slope (%)"),
                            #("Slope Aspect ", "Slope Aspect "),
                            #("Profile Position", "Profile Position"),
                            ("Australian Soil Classification", "Australian Soil Classification"),
                            ("FAO soil classification", "FAO soil classification"),
                            ("Immediate Previous Land Use", "Immediate Previous Land Use"),
                            #("Date since change in Land Use", "Date since change in Land Use"),
                            #("Crop rotation 1yr since present", "Crop rotation 1yr since present"),
                            #("Crop rotation 2yrs since present", "Crop rotation 2yrs since present"),
                            #("Crop rotation 3yrs since present", "Crop rotation 3yrs since present"),
                            #(" Crop rotation 4yrs since present", " Crop rotation 4yrs since present"),
                            #("Crop rotation 5yrs since present", "Crop rotation 5yrs since present"),
                            ("Agrochemical Additions", "Agrochemical Additions"),
                            ("Tillage", "Tillage"),
                            ("Fire", "Fire"),
                            ("", "")])


    search_value = forms.CharField(max_length=100)

    search_range = forms.ChoiceField(choices=[
                                        ("lat (-)", "lat (-)"),
                                        ("lon", "lon"),
                                        ("Depth", "Depth"),
                                        ("Elevation (m)", "Elevation (m)"),
                                        ("Texture", "Texture"),
                                        ("Gravel (%) - ( >2.0 mm)", "Gravel (%) - ( >2.0 mm)"),
                                        ("Course Sand (%) (200-2000 µm)", "Course Sand (%) (200-2000 µm)"),
                                        ("Fine Sand (%) - (20-200 µm)", "Fine Sand (%) - (20-200 µm)"),
                                        ("Sand (%)", "Sand (%)"),
                                        ("Silt  (%) (2-20 µm)", "Silt  (%) (2-20 µm)"),
                                        ("Clay (%) (<2 µm)", "Clay (%) (<2 µm)"),
                                        ("Ammonium Nitrogen (mg/Kg)", "Ammonium Nitrogen (mg/Kg)"),
                                        ("Nitrate Nitrogen (mg/Kg)", "Nitrate Nitrogen (mg/Kg)"),
                                        ("Phosphorus Colwell (mg/Kg)", "Phosphorus Colwell (mg/Kg)"),
                                        ("Potassium Colwell (mg/Kg)", "Potassium Colwell (mg/Kg)"),
                                        ("Sulphur (mg/Kg)", "Sulphur (mg/Kg)"),
                                        ("Organic Carbon (%)", "Organic Carbon (%)"),
                                        ("Conductivity (dS/m)", "Conductivity (dS/m)"),
                                        ("pH Level (CaCl2) (pH)", "pH Level (CaCl2) (pH)"),
                                        ("pH Level (H2O) (pH)", "pH Level (H2O) (pH)"),
                                        ("DTPA Copper (mg/Kg)", "DTPA Copper (mg/Kg)"),
                                        ("DTPA Iron (mg/Kg)", "DTPA Iron (mg/Kg)"),
                                        ("DTPA Manganese (mg/Kg)", "DTPA Manganese (mg/Kg)"),
                                        ("DTPA Zinc (mg/Kg)", "DTPA Zinc (mg/Kg)"),
                                        ("Exc. Aluminium (meq/100g)", "Exc. Aluminium (meq/100g)"),
                                        ("Exc. Calcium (meq/100g)", "Exc. Calcium (meq/100g)"),
                                        ("Exc. Magnesium (meq/100g)", "Exc. Magnesium (meq/100g)"),
                                        ("Exc. Potassium (meq/100g)", "Exc. Potassium (meq/100g)"),
                                        ("Exc. Sodium (meq/100g)", "Exc. Sodium (meq/100g)"),
                                        ("Boron Hot CaCl2 (mg/Kg)", "Boron Hot CaCl2 (mg/Kg)"),
                                        ("Total Nitrogen", "Total Nitrogen"),
                                        ("Total Carbon", "Total Carbon")])
    search_range_min = forms.DecimalField()
    search_range_max = forms.DecimalField()

    search_phylum = forms.CharField(max_length=100)
    search_class = forms.CharField(max_length=100)
    search_order = forms.CharField(max_length=100)
    search_family = forms.CharField(max_length=100)
    search_genus = forms.CharField(max_length=100)
