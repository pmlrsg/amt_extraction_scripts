# AMT CCI Extraction and Visualisation Scripts #

A set of scripts to extract and visualise CCI data covering the AMT track.

To extract from the global CCI datasets the RSG `nk_toolkit` library is used, usage is:

```python
from nk_toolkit import libsubarea

libsubarea.nk_subarea(in_netcdf, out_netcdf_file,
                      ["lon", "lat"], [extent[0], extent[3]],
                      [extent[2], extent[1]])
```

## SST-CCI

### Data extraction

```bash
extract_cci-sst.py --startdate <start_date> --enddate <end_date> \
 -o ./extracted_sst
 --extent <ulx> <uly> <lrx> <lry>
```

### Plotting

```
plot_sst-cci_data.py <in_netcdf.nc> <out_png.png>
```

Create animation gif using:
```
convert -delay 50 -loop 0 ????/*png sst-cci-time-series.gif
```

## OC-CCI

### Data extraction

```bash
extract_cci-oc.py --extent ulx uly lrx lry \
    --startdate <start_date> --enddate <end_date> \
    --product chlor_a --composite daily \
    -o ./extracted_chl
```

### Plotting

```
plot_oc-cci_data.py <in_netcdf.nc> <out_png.png>
```

Create animation gif using:
```
convert -delay 50 -loop 0 ????/*png oc-cci-time-series.gif
```
