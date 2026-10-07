import geopandas as gpd
#import rasterio
#import matplotlib.pyplot as plt
#import numpy as np
#from rasterio.features import geometry_mask

input_tif = "/UHI-Analysis/data/LC08_L2SP_142051_20150405_20200909_02_T1_ST_B10.TIF"
output_tif = "/UHI-Analysis/Map/LST_2015.tif"

with rasterio.open(input_tif) as src:
    st = src.read(1).astype(np.float32)
    profile = src.profile

    # Handle NoData values
    nodata = src.nodata
    if nodata is not None:
        mask = (st == nodata)
    else:
        mask = np.zeros_like(st, dtype=bool)

    lst_kelvin = st * 0.00341802 + 149.0
    lst_celsius = lst_kelvin - 273.15
    lst_celsius[mask] = -9999

    profile.update(
        dtype=rasterio.float32,
        nodata=-9999,
        compress='lzw'
    )

    with rasterio.open(output_tif, 'w', **profile) as dst:
        dst.write(lst_celsius.astype(rasterio.float32), 1)
print("LST_2015.tif created successfully")

chennai_boundary = gpd.read_file(
    "/Users/keerth/Desktop/GIS/VIT-Paper/Chennai_map.kml",
    driver="KML"
)

chennai_clean = chennai_boundary.to_crs("EPSG:32644")
chennai_clean = chennai_clean.dissolve()
print(chennai_clean.total_bounds)

with rasterio.open(
    "/UHI-Analysis/data/LC08_L2SP_142051_20150405_20200909_02_T1_SR_B4.TIF"
) as src:
    transform = src.transform
    profile = src.profile
    extent = [
        src.bounds.left,
        src.bounds.right,
        src.bounds.bottom,
        src.bounds.top
    ]
print(extent)

with rasterio.open(
    "/UHI-Analysis/Map/LST_2015.tif"
) as src:
    LST_2015 = src.read(1).astype(float)
mask_geom = geometry_mask(
    chennai_clean.geometry,
    transform=transform,
    invert=True,
    out_shape=LST_2015.shape
)
LST_clip = LST_2015.copy()
LST_clip[~mask_geom] = np.nan
print("Mean Chennai LST =",round(np.nanmean(LST_clip),2))

fig, ax = plt.subplots(figsize=(10,10))
img = ax.imshow(
    np.ma.masked_invalid(LST_clip),
    extent=extent,
    cmap="RdYlBu_r",
    origin="upper",
    vmin=20,
    vmax=55
)

# Chennai Boundary
chennai_clean.boundary.plot(ax=ax,color="black",linewidth=1)
# Zoom to Chennai
xmin, ymin, xmax, ymax = chennai_clean.total_bounds
pad = 1000
ax.set_xlim(xmin-pad, xmax+pad)
ax.set_ylim(ymin-pad, ymax+pad)

# Title
ax.set_title("Land Surface Temperature Distribution of Chennai (2015)",fontsize=12,fontweight="bold")

ax.set_xlabel("Easting (m)")
ax.set_ylabel("Northing (m)")
plt.tight_layout()
plt.savefig("/UHI-Analysis/Map/LST_2015_Chennai.png",dpi=600,bbox_inches="tight")
plt.show()
print("LST 2015 Map Saved")
