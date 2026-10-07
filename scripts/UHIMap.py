import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

print("Mean LST =", np.nanmean(LST_clip))

UHI = np.digitize(LST_clip,bins=[25,30,35,40,45]).astype(float)
UHI[np.isnan(LST_clip)] = np.nan

mean_temp = np.nanmean(LST_clip)
std_temp = np.nanstd(LST_clip)
threshold = mean_temp + std_temp
hotspot_pixels = np.nansum(LST_clip >= threshold)
total_pixels = np.nansum(~np.isnan(LST_clip))
hotspot_percentage = (hotspot_pixels / total_pixels) * 100
print("Mean LST     =", round(mean_temp,2))
print("Std Dev      =", round(std_temp,2))
print("Threshold    =", round(threshold,2))
print("Hotspot Area (%) =",round(hotspot_percentage,2))

# CLASS DISTRIBUTION
unique, counts = np.unique(UHI[~np.isnan(UHI)],return_counts=True)
print("\nUHI Class Distribution")
for u, c in zip(unique, counts):
    print(f"Class {int(u)} : {c}")
    
# UHI COLOR SCHEME
uhi_cmap = ListedColormap([
    "#2c7bb6",
    "#abd9e9",
    "#ffffbf",
    "#fdae61",
    "#f46d43",
    "#d7191c"
])
uhi_cmap.set_bad("white")
# PLOT
fig, ax = plt.subplots(figsize=(10,10))
img = ax.imshow(np.ma.masked_invalid(UHI),extent=extent,cmap=uhi_cmap,origin='upper',vmin=0,vmax=5)

chennai_clean.boundary.plot(ax=ax,color='black',linewidth=2)

xmin, ymin, xmax, ymax = chennai_clean.total_bounds
pad = 1000
ax.set_xlim(xmin-pad, xmax+pad)
ax.set_ylim(ymin-pad, ymax+pad)

# Title
ax.set_title("Urban Heat Island Map of Chennai (2015)",fontsize=18,fontweight='bold')
plt.tight_layout()
plt.savefig("/UHI-Analysis/Map/UHI_2015_Chennai.png",dpi=600,bbox_inches='tight')
plt.show()
