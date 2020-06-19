# lehdpy

**lehdpy** is a Python library for downloadidng [LEHD](https://lehd.ces.census.gov/data/) (Longitudinal Employer-Household Dynamics) data into Pandas DataFrames

### How to use

```python
import lehd
import pandas as pd

# downloading workplace data (WAC) for Arizona (state ID = 44) and New Mexico () for 2016
df = lehd.dl_lodes.wac(locations = ["44", "35"], year = 2016)

# downloading residential data (RAC) for Arizona (state ID = 44) for 2016
# also summarizing data by census tract, and workforce type "SE01" ($1250 per month or less)
df = lehd.dl_lodes.rac(locations = ["44"], year = 2016, geography = "CT")

# downloading OD data (OD) for 3 counties in Rhode Island, aggregating data by counties
df = lehd.dl_lodes.od(year = 2016, geography = "CT", type = "JT00", origins = ["44001","44003","44005"])

# downloading OD from county 44001 to all other coutnies in Rhode Island
df = lehd.dl_lodes.od(year = 2016, geography = "C", type = "JT00", origins = ["44001"], destinations = ["44"], constrained = "yes")

print(df)
```

```
  h_geoid_C w_geoid_C  S000  SA01  SA02  SA03  SE01  SE02  SE03  SI01  SI02  SI03
0     44001     44001  5794  1310  2701  1783  1857  1992  1945  1045   559  4190
1     44001     44003  1524   323   811   390   350   416   758   150   390   984
2     44001     44005  2121   476  1050   595   475   645  1001   371   231  1519
3     44001     44007  7557  1150  4100  2307  1227  1931  4399   602   960  5995
4     44001     44009   694   184   315   195   183   191   320   119   149   426
```
