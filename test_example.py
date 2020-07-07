import lehd
import pandas as pd
import geopandas as gpd

# downloading workplace data for Arizona (state ID = 44) and New Mexico () for 2016
df = lehd.dl_lodes.wac(
    locations = ["44", "35"],
    year = 2016
    )

# # downloading residential data for Arizona (state ID = 44) for 2016
# # also summarizing data by census tract, and workforce type "SE01" ($1250 per month or less)
df = lehd.dl_lodes.rac(
    locations = ["44"],
    year = 2016,
    geography = "CT",
    seg = "SE01"
    )

# downloading OD data for 3 counties in Rhode Island, aggregating data by counties
df = lehd.dl_lodes.od(
    year = 2016,
    geography = "C",
    type = "JT00",
    origins = ["44001","44003","44005"]
    )

# downloading OD from county 44001 to all other coutnies in Rhode Island
df = lehd.dl_lodes.od(
    year = 2016,
    geography = "C",
    type = "JT00",
    origins = ["44001"],
    destinations = ["44"],
    constrained = "yes"
    )

print(df)
