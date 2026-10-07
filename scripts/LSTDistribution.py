import rasterio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

from rasterio.features import geometry_mask
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

#compute NDWI
folder = "/UHI-Analysis/data"

B3 = rasterio.open(f"{folder}/LC08_L2SP_142051_20150405_20200909_02_T1_SR_B3.TIF").read(1).astype(float)
B4 = rasterio.open(f"{folder}/LC08_L2SP_142051_20150405_20200909_02_T1_SR_B4.TIF").read(1).astype(float)
B5 = rasterio.open(f"{folder}/LC08_L2SP_142051_20150405_20200909_02_T1_SR_B5.TIF").read(1).astype(float)
B6 = rasterio.open(f"{folder}/LC08_L2SP_142051_20150405_20200909_02_T1_SR_B6.TIF").read(1).astype(float)

ST = rasterio.open(f"{folder}/LC08_L2SP_142051_20150405_20200909_02_T1_ST_B10.TIF").read(1).astype(float)
QA = rasterio.open(f"{folder}/LC08_L2SP_142051_20150405_20200909_02_T1_ST_QA.TIF").read(1)

#Scaling
B3 = B3 * 0.0000275 - 0.2
B4 = B4 * 0.0000275 - 0.2
B5 = B5 * 0.0000275 - 0.2
B6 = B6 * 0.0000275 - 0.2

#compute NDVI
NDVI = (B5 - B4) / (B5 + B4)
NDVI[(NDVI < -1) |(NDVI > 1)] = np.nan

#compute NDBI
NDBI = (B6 - B5) / (B6 + B5)
NDBI[(NDBI < -1) |(NDBI > 1)] = np.nan

#compute NDWI
NDWI = (B3 - B5) / (B3 + B5)
NDWI[(NDWI < -1) |(NDWI > 1)] = np.nan

#Create LST
ST[ST == 0] = np.nan
LST_K = ST * 0.00341802 + 149.0
LST = LST_K - 273.15
LST[(LST < 15) |(LST > 70)] = np.nan

# CHENNAI LST VALIDATION
chennai_boundary = gpd.read_file("/Data/Chennai_map.kml",driver="KML")
chennai_clean = chennai_boundary.to_crs("EPSG:32644")
chennai_clean = chennai_clean.dissolve()

with rasterio.open(f"{folder}/LC08_L2SP_142051_20150405_20200909_02_T1_SR_B4.TIF") as src:
   transform = src.transform
mask_geom = geometry_mask(chennai_clean.geometry,transform=transform,invert=True,out_shape=LST.shape)

LST_clip = LST.copy()
LST_clip[~mask_geom] = np.nan
print("\n===== CHENNAI LST STATISTICS =====")
print("Mean :", np.nanmean(LST_clip))
print("Median :", np.nanmedian(LST_clip))
print("Min :", np.nanmin(LST_clip))
print("Max :", np.nanmax(LST_clip))
print("Std :", np.nanstd(LST_clip))

# HISTOGRAM
plt.figure(figsize=(8,5))
plt.hist(LST_clip[~np.isnan(LST_clip)],bins=100,color="red")
plt.xlabel("LST (°C)")
plt.ylabel("Frequency")
plt.title("2015 Chennai LST Distribution")
plt.grid(True)
plt.show()

#UHI Classification
mean_temp = np.nanmean(LST_clip)
std_temp = np.nanstd(LST_clip)

UHI = np.zeros_like(LST_clip)

UHI[LST_clip < mean_temp - std_temp] = 1
UHI[(LST_clip >= mean_temp - std_temp) &
    (LST_clip < mean_temp)] = 2
UHI[(LST_clip >= mean_temp) &
    (LST_clip < mean_temp + std_temp)] = 3
UHI[LST_clip >= mean_temp + std_temp] = 4

UHI[np.isnan(LST_clip)] = np.nan

#Read DEM
DEM = rasterio.open("/UHI-Analysis/data/output_SRTMGL1.tif").read(1).astype(float)

#Create Data Frame
df = pd.DataFrame({'NDVI': NDVI.flatten(),'NDBI': NDBI.flatten(),'NDWI': NDWI.flatten(),'LST': LST.flatten()})
df.replace([np.inf, -np.inf],np.nan,inplace=True)
df.dropna(inplace=True)
print("Rows before sampling:", len(df))
df = df.sample(n=50000,random_state=42)
print("Rows after sampling:", len(df))

# Export CSV
df.to_csv("/UHI-Analysis/Map/UHI_2015Sample_50000.csv",index=False)
print("CSV saved successfully")

# Clip NDVI
NDVI_clip = NDVI.copy()
NDVI_clip[~mask_geom] = np.nan

# Clip NDWI
NDWI_clip = NDWI.copy()
NDWI_clip[~mask_geom] = np.nan

# Clip NDBI
NDBI_clip = NDBI.copy()
NDBI_clip[~mask_geom] = np.nan

# Clip LST
LST_clip = LST.copy()
LST_clip[~mask_geom] = np.nan


#Export NDVI NDBI NDWI LST
summary = pd.DataFrame({
"Parameter": ["NDVI", "NDBI", "NDWI", "LST"],
"Minimum": [np.nanmin(NDVI_clip),np.nanmin(NDBI_clip),np.nanmin(NDWI_clip),np.nanmin(LST_clip)],
"Maximum": [np.nanmax(NDVI_clip),np.nanmax(NDBI_clip),np.nanmax(NDWI_clip),np.nanmax(LST_clip)],
"Mean": [np.nanmean(NDVI_clip),np.nanmean(NDBI_clip),np.nanmean(NDWI_clip),np.nanmean(LST_clip)],
"Median": [np.nanmedian(NDVI_clip),np.nanmedian(NDBI_clip),np.nanmedian(NDWI_clip),np.nanmedian(LST_clip)]})

summary.to_csv("/UHI-Analysis/Map/Index_Summary_2015.csv",index=False)
print("Summary CSV exported successfully")

# Water
water_mask = NDWI_clip > 0
# Built-up
builtup_mask = ((NDBI_clip > -0.01) &(~water_mask))
# Total valid pixels
total_pixels = np.sum(~np.isnan(NDVI_clip))
# Percentages
builtup_percent = (np.sum(builtup_mask) / total_pixels) * 100
water_percent = (np.sum(water_mask) / total_pixels) * 100
non_builtup_percent = ( 100 - builtup_percent - water_percent)
print(f"Built-up Area % = {builtup_percent:.2f}")
print(f"Non-Built-up Area % = {non_builtup_percent:.2f}")
print(f"Water Body % = {water_percent:.2f}")

# Save summary
year = 2015
landcover_summary = pd.DataFrame({"Year":[year],"Builtup_Area_Percent":[builtup_percent],"Non_Builtup_Area_Percent":[non_builtup_percent],"Water_Body_Percent":[water_percent],"Mean_LST":[np.nanmean(LST_clip)]})
print(landcover_summary)
landcover_summary.to_csv(f"Landcover_Summary_{year}.csv",index=False)
landcover_summary = pd.DataFrame({
    "Year":[year],
    "Builtup_Area_Percent":[builtup_percent],
    "Non_Builtup_Area_Percent":[non_builtup_percent],
    "Water_Body_Percent":[water_percent],
    "Mean_LST":[np.nanmean(LST_clip)]})
landcover_summary.to_csv(f"Landcover_Summary_{year}.csv",index=False)
