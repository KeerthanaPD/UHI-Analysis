## Overview

This project investigates the Urban Heat Island (UHI) effect in Chennai, India, from 2015 to 2026 using multi-temporal Landsat imagery, remote sensing techniques, and machine learning. The study evaluates how vegetation, built-up areas, and surface moisture influence land surface temperature (LST) and UHI formation across the city. 

The workflow integrates spectral index analysis, thermal mapping, hotspot detection, Random Forest regression, and future temperature forecasting to support sustainable urban planning and climate resilience.

## Objectives

- Analyze temporal variations in vegetation, built-up areas, and moisture conditions.
- Estimate Land Surface Temperature (LST) across Chennai.
- Identify Urban Heat Island (UHI) hotspots.
- Evaluate relationships between environmental indices and LST using Random Forest Regression.
- Forecast future LST and UHI trends. 

## Study Area

Chennai, Tamil Nadu, India

Coordinates:
- Latitude: 12.9°N – 13.3°N
- Longitude: 80.1°E – 80.3°E 

## Data Source

- Landsat Collection 2 Level 2 Imagery
- USGS Earth Explorer
- Study Years: 2015, 2017, 2020, 2022, 2024, 2026 

## Methodology

Workflow Overview:

1. Data Acquisition
2. Cloud Removal and Preprocessing
3. Chennai Boundary Clipping
4. Spectral Index Computation
   - NDVI
   - NDBI
   - NDWI
5. Land Surface Temperature (LST) Estimation
6. UHI Hotspot Mapping
7. Random Forest Regression
8. Trend Analysis
9. Future Forecasting (2028 and 2030)

## Indices Used
### NDVI
Vegetation Condition Assessment

NDVI = (NIR - Red) / (NIR + Red)

### NDBI
Built-up Area Assessment

NDBI = (SWIR - NIR) / (SWIR + NIR)

### NDWI
Surface Moisture Assessment

NDWI = (Green - NIR) / (Green + NIR) 

## Technologies Used

- Python
- Jupyter Notebook
- Rasterio
- GeoPandas
- NumPy
- Pandas
- Matplotlib
- Scikit-learn
- QGIS 

## Key Findings
### Mean Land Surface Temperature (°C)

| Year | LST |
|------|------|
| 2015 | 41.36 |
| 2017 | 41.84 |
| 2020 | 45.07 |
| 2022 | 44.41 |
| 2024 | 46.83 |
| 2026 | 44.90 |

Forecast:
- 2028: 47.17°C
- 2030: 48.02°C 

### UHI Hotspot Area (%)

| Year | Hotspot Area |
|------|-------------|
| 2015 | 9.49 |
| 2017 | 11.64 |
| 2020 | 11.04 |
| 2022 | 9.03 |
| 2024 | 10.80 |
| 2026 | 11.64 |

Forecast:
- 2028: 11.14%
- 2030: 11.28% 
