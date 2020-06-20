# lehd

A Python library for downloading [LEHD](https://lehd.ces.census.gov/data/) (Longitudinal Employer-Household Dynamics) data into Pandas DataFrames

### How to use

```python
import lehd

# downloading workplace data for Arizona (state ID = 44)
# and New Mexico () for 2016
df = lehd.dl_lodes.wac(
    locations = ["44", "35"],
    year = 2016
    )

# downloading residential data for Arizona (state ID = 44)
# for 2016, while also summarizing data by census tract,
# only workforce type "SE01" ($1250 per month or less)
df = lehd.dl_lodes.rac(
    locations = ["44"],
    year = 2016,
    geography = "CT",
    seg = "SE01"
    )

# downloading OD data for 3 counties in Rhode Island,
# aggregating data by counties
df = lehd.dl_lodes.od(
    year = 2016,
    geography = "C",
    type = "JT00",
    origins = ["44001","44003","44005"]
    )

# downloading and summarizing OD data from county 44001
# to all other counties in Rhode Island
df = lehd.dl_lodes.od(
    year = 2016,
    geography = "C",
    type = "JT00",
    origins = ["44001"],
    destinations = ["44"],
    constrained = "yes"
    )

```

```python
>>> df.head()
  h_geoid_C w_geoid_C  S000  SA01  SA02  SA03  SE01  SE02  SE03  SI01  SI02  SI03
0     44001     44001  5794  1310  2701  1783  1857  1992  1945  1045   559  4190
1     44001     44003  1524   323   811   390   350   416   758   150   390   984
2     44001     44005  2121   476  1050   595   475   645  1001   371   231  1519
3     44001     44007  7557  1150  4100  2307  1227  1931  4399   602   960  5995
4     44001     44009   694   184   315   195   183   191   320   119   149   426
```


### Functions

These are the details for the three main download functions for the three LODES data types (WAC, RAC, OD)

***

```python
lehd.dl_lodes.wac(
  locations,
  year = 2016,
  geography = "B",
  seg = "S000",
  type = "JT00"
  ):
```

Downloads workplace characteristic (WAC) data into a pandas dataframe

`locations` | List of workplace locations to download data for, where locations are strings of GEOIDs. Must be specified

`year` : int or str representing the year to download data for

`geography` : The geographic scale in which to aggregate data to. The options are as follows:
`"B"`  | blocks
`"BG"` | block groups
`"CT"` | census tracts
`"P"`  | places
`"CS"` | county subdivision
`"C"`  | counties
`"S"`  | states
The default are blocks, which are how the raw data is provided, which thus does not require aggregation

`seg` : Segment of the workforce, can have the values of “S000”, “SA01”, “SA02”, “SA03”, “SE01”, “SE02”, “SE03”, “SI01”, “SI02”, or “SI03”. Default is all workers. Please see https://lehd.ces.census.gov/data/lodes/LODES7/LODESTechDoc7.4.pdf for detail on the subset workforce segments

`type` : From the LEHD documentation, this can have a value of "JT00" for All Jobs, "JT01" for Primary Jobs, "JT02" for All Private Jobs, "JT03" for Private Primary Jobs, "JT04" for All Federal Jobs, or "JT05" for Federal Primary Jobs.

***

```python
lehd.dl_lodes.rac(
  locations,
  year = 2016,
  geography = "B",
  seg = "S000",
  type = "JT00"
  ):
```

Downloads residential characteristic (RAC) data into a pandas dataframe

`locations` | List of workplace locations to download data for, where locations are strings of GEOIDs. Must be specified

`year` : int or str representing the year to download data for

`geography` : The geographic scale in which to aggregate data to. The options are as follows:
`"B"`  | blocks
`"BG"` | block groups
`"CT"` | census tracts
`"P"`  | places
`"CS"` | county subdivision
`"C"`  | counties
`"S"`  | states
The default are blocks, which are how the raw data is provided, which thus does not require aggregation

`seg` : Segment of the workforce, can have the values of “S000”, “SA01”, “SA02”, “SA03”, “SE01”, “SE02”, “SE03”, “SI01”, “SI02”, or “SI03”. Default is all workers. Please see https://lehd.ces.census.gov/data/lodes/LODES7/LODESTechDoc7.4.pdf for detail on the subset workforce segments

`type` : From the LEHD documentation, this can have a value of "JT00" for All Jobs, "JT01" for Primary Jobs, "JT02" for All Private Jobs, "JT03" for Private Primary Jobs, "JT04" for All Federal Jobs, or "JT05" for Federal Primary Jobs.


***

```python
lehd.dl_lodes.od(
  year = 2016,
  geography = "B",
  type = "JT00",
  origins = None,
  destinations = None,
  constrained = "no"
  )
```


Downloads origin destination (OD) commuting flow data into a pandas dataframe

`year` : int or str representing the year to download data for

geography : The geographic scale in which to aggregate data to. The options are as follows:
`"B"`  | blocks
`"BG"` | block groups
`"CT"` | census tracts
`"P"`  | places
`"CS"` | county subdivision
`"C"`  | counties
`"S"`  | states
the default are blocks, which are how the raw data is provided, which thus does not require aggregation

`type` : from the LEHD documentation, this can have a value of "JT00" for All Jobs, "JT01" for Primary Jobs, "JT02" for All Private Jobs, "JT03" for Private Primary Jobs, "JT04" for All Federal Jobs, or "JT05" for Federal Primary Jobs.

`origins` | list of origins to download data for, where origins are strings of GEOIDs. Must be specified if destinations is not specified

`destinations` | list of destinations to download data for, where destinations are strings of GEOIDs. Must be specified if origins is not specified

`note`: one of origins or destinations must be provided

constrained : whether or not to only download data within a state
`yes`  | download only the data from the input origins, to the input destinations,
`no`   | download all data without OD constraints

"""
