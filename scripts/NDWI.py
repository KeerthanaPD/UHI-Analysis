

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from rasterio.features import geometry_mask



transform = src.transform

mask_geom = geometry_mask(
    chennai_clean.geometry,
    transform=transform,
    invert=True,
    out_shape=NDWI.shape
)


NDWI_clip = NDWI.copy()
NDWI_clip[~mask_geom] = np.nan


NDWI_class = np.digitize(
    NDWI_clip,
    bins=[-0.20, -0.10, 0.00, 0.10, 0.20]
).astype(float)

NDWI_class[np.isnan(NDWI_clip)] = np.nan


ndwi_cmap = ListedColormap([
    "#8c510a",  # Very Dry
    "#d8b365",  # Dry
    "#f6e8c3",  # Moderate
    "#92c5de",  # Moist
    "#4393c3",  # Water
    "#2166ac"   # Deep Water
])

ndwi_cmap.set_bad("white")


fig, ax = plt.subplots(figsize=(10,10))

img = ax.imshow(
    np.ma.masked_invalid(NDWI_class),
    extent=extent,
    cmap=ndwi_cmap,
    origin='upper',
    vmin=0,
    vmax=5
)

# Chennai Boundary

chennai_clean.boundary.plot(
    ax=ax,
    color='black',
    linewidth=1
)

# Zoom

xmin, ymin, xmax, ymax = chennai_clean.total_bounds

pad = 1000

ax.set_xlim(xmin-pad, xmax+pad)
ax.set_ylim(ymin-pad, ymax+pad)


legend_elements = [

    Patch(facecolor='#8c510a',
          label='Very Dry (< -0.20)'),

    Patch(facecolor='#d8b365',
          label='Dry (-0.20 to -0.10)'),

    Patch(facecolor='#f6e8c3',
          label='Moderate (-0.10 to 0.00)'),

    Patch(facecolor='#92c5de',
          label='Moist (0.00 to 0.10)'),

    Patch(facecolor='#4393c3',
          label='Water (0.10 to 0.20)'),

    Patch(facecolor='#2166ac',
          label='Deep Water (> 0.20)')
]

ax.legend(
    handles=legend_elements,
    loc='lower right',
    title='NDWI Classes',
    fontsize=7,
    title_fontsize=8,
    framealpha=0.7
)


#cbar = plt.colorbar(img,ax=ax,shrink=0.8)
#cbar.set_label("NDWI Classes")


ax.set_title(
    "NDWI Distribution of Chennai (2015)",
    fontsize=14,
    fontweight='bold'
)

ax.set_xlabel("Easting (m)")
ax.set_ylabel("Northing (m)")

plt.tight_layout()


plt.savefig(
    "/Users/keerth/Desktop/GIS/VIT-Paper/TS/Output/NDWI_2015_Chennai.png",
    dpi=600,
    bbox_inches='tight'
)

plt.show()

print("NDWI Map Saved")