

import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import rasterio

from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from rasterio.features import geometry_mask


nir_file = "/Users/keerth/Desktop/GIS/VIT-Paper/TS/LC08_L2SP_142051_20150405_20200909_02_T1/LC08_L2SP_142051_20150405_20200909_02_T1_SR_B5.TIF"

swir1_file = "/Users/keerth/Desktop/GIS/VIT-Paper/TS/LC08_L2SP_142051_20150405_20200909_02_T1/LC08_L2SP_142051_20150405_20200909_02_T1_SR_B6.TIF"


with rasterio.open(nir_file) as src:
    nir = src.read(1).astype(np.float32)

    raster_crs = src.crs
    transform = src.transform

    height = src.height
    width = src.width

    extent = [
        src.bounds.left,
        src.bounds.right,
        src.bounds.bottom,
        src.bounds.top
    ]

with rasterio.open(swir1_file) as src:
    swir1 = src.read(1).astype(np.float32)


nir[nir <= 0] = np.nan
swir1[swir1 <= 0] = np.nan


NDBI = (swir1 - nir) / (swir1 + nir)


chennai_boundary = gpd.read_file(
    "/Users/keerth/Desktop/GIS/VIT-Paper/Chennai_map.kml",
    driver="KML"
)

chennai_clean = chennai_boundary.to_crs(raster_crs)
chennai_clean = chennai_clean.dissolve()


mask_geom = geometry_mask(
    chennai_clean.geometry,
    transform=transform,
    invert=True,
    out_shape=(height, width)
)


NDBI_clip = NDBI.copy()
NDBI_clip[~mask_geom] = np.nan


NDBI_class = np.digitize(
    NDBI_clip,
    bins=[-0.20, -0.01, 0.00, 0.01, 0.20]
).astype(float)

NDBI_class[np.isnan(NDBI_clip)] = np.nan

ndbi_cmap = ListedColormap([
    "#2166ac",
    "#92c5de",
    "#ffffbf",
    "#fdae61",
    "#f46d43",
    "#d73027"
])

ndbi_cmap.set_bad("white")

fig, ax = plt.subplots(figsize=(10,10))

img = ax.imshow(
    np.ma.masked_invalid(NDBI_class),
    extent=extent,
    cmap=ndbi_cmap,
    origin="upper",
    vmin=0,
    vmax=5
)

# Chennai Boundary

chennai_clean.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1.5
)

xmin, ymin, xmax, ymax = chennai_clean.total_bounds

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

legend_elements = [
    Patch(facecolor="#2166ac", label="Water / Vegetation"),
    Patch(facecolor="#92c5de", label="Low Built-up"),
    Patch(facecolor="#ffffbf", label="Moderate Built-up"),
    Patch(facecolor="#fdae61", label="Built-up"),
    Patch(facecolor="#f46d43", label="Dense Built-up"),
    Patch(facecolor="#d73027", label="Highly Urbanized")
]

ax.legend(
    handles=legend_elements,
    loc="lower right",
    title="Built-up Intensity",
    fontsize=7,
    title_fontsize=8
)

ax.set_title(
    "Spatial Distribution of NDBI in Chennai (2015)",
    fontsize=12,
    fontweight="bold"
)

ax.set_xlabel("Easting (m)")
ax.set_ylabel("Northing (m)")

plt.tight_layout()

plt.savefig(
    "/Users/keerth/Desktop/GIS/VIT-Paper/TS/Output/NDBI_2015_Chennai_Final.png",
    dpi=600,
    bbox_inches="tight"
)

plt.show()

print("NDBI 2015 Map Saved Successfully")