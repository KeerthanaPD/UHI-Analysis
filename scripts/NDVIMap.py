from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap
from rasterio.features import geometry_mask
import matplotlib.pyplot as plt
import numpy as np


transform = src.transform

mask_geom = geometry_mask(
    chennai_clean.geometry,
    transform=transform,
    invert=True,
    out_shape=NDVI.shape
)


NDVI_clip = NDVI.copy()
NDVI_clip[~mask_geom] = np.nan


NDVI_class = np.digitize(
    NDVI_clip,
    bins=[0, 0.1, 0.2, 0.3, 0.4]
).astype(float)

NDVI_class[np.isnan(NDVI_clip)] = np.nan


ndvi_cmap = ListedColormap([
    "#2166ac",  # Water / very low
    "#d73027",  # Built-up / barren
    "#fdae61",  # Sparse vegetation
    "#a6d96a",  # Moderate vegetation
    "#1a9850",  # Dense vegetation
    "#006837"   # Very dense vegetation
])

ndvi_cmap.set_bad("white")


fig, ax = plt.subplots(figsize=(10,10))

img = ax.imshow(
    np.ma.masked_invalid(NDVI_class),
    extent=extent,
    cmap=ndvi_cmap,
    origin="upper",
    vmin=0,
    vmax=5
)

# Chennai Boundary

chennai_clean.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1
)

# Zoom

xmin, ymin, xmax, ymax = chennai_clean.total_bounds

pad = 1000

ax.set_xlim(xmin-pad, xmax+pad)
ax.set_ylim(ymin-pad, ymax+pad)


legend_elements = [
    Patch(facecolor='#2166ac',
          label='Water/Non-Vegetated (<0)'),

    Patch(facecolor='#d73027',
          label='Non-Vegetated (0-0.1)'),

    Patch(facecolor='#fdae61',
          label='Sparse Vegetation (0.1-0.2)'),

    Patch(facecolor='#a6d96a',
          label='Moderate Vegetation (0.2-0.3)'),

    Patch(facecolor='#1a9850',
          label='Dense Vegetation (0.3-0.4)'),

    Patch(facecolor='#006837',
          label='Very Dense Vegetation (>0.4)')
]

ax.legend(
    handles=legend_elements,
    loc='lower right',
    title='NDVI Classes',
    fontsize=7,
    title_fontsize=8
)


ax.set_title(
    "Spatial Distribution of NDVI in Chennai (2015)",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Easting (m)")
ax.set_ylabel("Northing (m)")

plt.tight_layout()



plt.savefig(
    "/Users/keerth/Desktop/GIS/VIT-Paper/TS/Output/NDVI_2015_Chennai.png",
    dpi=600,
    bbox_inches="tight"
)

plt.show()

print("NDVI 2015 Map Saved")