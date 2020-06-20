

import lehd
import pandas as pd
import urllib.request
import gzip


class dl_lodes:

    """
    Simple class for downloading LEHD data.

    For more information about this source data, see https://lehd.ces.census.gov/data/
    """

    def __init__(self):

        None


    def wac(locations, year = 2016, geography = "B", seg = "S000", type = "JT00"):

        """
        Downloads workplace characteristic (WAC) data into a pandas dataframe

        Parameters
        ----------
        locations | List of workplace locations to download data for, where locations are strings of GEOIDs. Must be specified

        year : int or str representing the year to download data for

        geography : The geographic scale in which to aggregate data to. The options are as follows:
        "B"  | blocks
        "BG" | block groups
        "CT" | census tracts
        "P"  | places
        "CS" | county subdivision
        "C"  | counties
        "S"  | states
        The default are blocks, which are how the raw data is provided, which thus does not require aggregation

        seg : Segment of the workforce, can have the values of “S000”, “SA01”, “SA02”, “SA03”, “SE01”, “SE02”, “SE03”, “SI01”, “SI02”, or “SI03”. Default is all workers. Please see https://lehd.ces.census.gov/data/lodes/LODES7/LODESTechDoc7.4.pdf for detail on the subset workforce segments

        type : From the LEHD documentation, this can have a value of "JT00" for All Jobs, "JT01" for Primary Jobs, "JT02" for All Private Jobs, "JT03" for Private Primary Jobs, "JT04" for All Federal Jobs, or "JT05" for Federal Primary Jobs.

        """

        # initial parameter checking

        year = int(year)
        if year < 2002:
            raise Exception('LEHD OD data is unavailable prior to 2002')
        if year > 2017:
            raise Exception('LEHD OD data is unavailable after to 2017')

        if geography not in ["B","BG","CT","C","S"]:

            raise Exception('Please make sure the input parameter @geography is one of ["B","BG","CT","C","S"]')

        if type not in ["JT00","JT01","JT02","JT03","JT04","JT05"]:

            raise Exception('Please make sure the input parameter @type is one of ["JT00","JT01","JT02","JT03","JT04","JT05"]')

        if seg not in ["S000", "SA01", "SA02", "SA03", "SE01", "SE02", "SE03", "SI01", "SI02"]:

            raise Exception('Please make sure the input parameter @seg is one of ["S000", "SA01", "SA02", "SA03", "SE01", "SE02", "SE03", "SI01", "SI02"]')


        # getting list of states to download data for

        states_for_dl = []
        if locations is not None:
            locations = pd.DataFrame(locations)
            locations.columns = ["o"]
            locations["gtype"] = locations["o"].apply(lehd.utils.infer_geog_input)
            states_for_dl = lehd.utils.get_state_alpha(locations, "o")
        else:
            raise Exception('Please input a list of locations to download data for')
        states_for_dl = list(set(list(states_for_dl)))

        # setting up the URLs needed for download, then download and put into a single pandas dataframe

        url_base = "https://lehd.ces.census.gov/data/lodes/LODES7/"
        dfl = []
        for state in states_for_dl:
            file_name = state.lower() + "_wac_" + seg + "_" + type + "_" + str(year) + ".csv.gz"
            url = url_base + state.lower() + "/wac/" + file_name
            print("Trying to download ", file_name, " from ", url, " ......")
            df = pd.read_csv(urllib.request.urlopen(url), compression = "gzip")
            dfl.append(df)
        df = pd.concat(dfl)

        # cleaning and adding leading 0s to block ids
        df["w_geoid_B"] = df["w_geocode"].astype(str)
        df["w_geoid_B"] = df["w_geoid_B"].str.zfill(15)
        del df["w_geocode"]

        # add column for aggregation, if applicable
        if geography != "B":
            df["w_geoid_" + geography] = df["w_geoid_B"].apply(lehd.utils.get_geoid, args = (geography,))


        # substting the data based on the input locations

        print("Subsetting the data based on the input locations list ...")
        dfm = []
        for geoid in list(locations["gtype"].unique()):
            if geoid != "B" and geoid != geography:
                df["w_geoid_" + geoid] = df["w_geoid_B"].apply(lehd.utils.get_geoid, args = (geoid,))
            list_unique = list(locations["o"][locations["gtype"] == geoid].unique())
            dfs = df[df["w_geoid_" + geoid].isin(list_unique)]["w_geoid_B"].unique()
            dfm = dfm + list(dfs)
        df = df.query("w_geoid_B in @dfm")


        # aggregating the output if applicable, and returning the resulting dataframe

        print("Finalizing the output ...")

        if geography == "B":
            return df
        else:
            output_values = ['C000', 'CA01', 'CA02', 'CA03', 'CE01', 'CE02', 'CE03', 'CNS01', 'CNS02', 'CNS03', 'CNS04', 'CNS05', 'CNS06', 'CNS07', 'CNS08', 'CNS09', 'CNS10', 'CNS11', 'CNS12', 'CNS13', 'CNS14', 'CNS15', 'CNS16', 'CNS17', 'CNS18', 'CNS19', 'CNS20', 'CR01', 'CR02', 'CR03', 'CR04', 'CR05', 'CR07', 'CT01', 'CT02', 'CD01', 'CD02', 'CD03', 'CD04', 'CS01', 'CS02']
            df = df.groupby(["w_geoid_" + geography])[output_values].sum().reset_index()
            return df
        print("Finished !!!")





    def rac(locations, year = 2016, geography = "B", seg = "S000", type = "JT00"):

        """
        Downloads residential characteristic (RAC) data into a pandas dataframe

        Parameters
        ----------
        locations | List of home locations to download data for, where locations are strings of GEOIDs. Must be specified

        year : int or str representing the year to download data for

        geography : The geographic scale in which to aggregate data to. The options are as follows:
        "B"  | blocks
        "BG" | block groups
        "CT" | census tracts
        "P"  | places
        "CS" | county subdivision
        "C"  | counties
        "S"  | states
        The default are blocks, which are how the raw data is provided, which thus does not require aggregation

        seg : Segment of the workforce, can have the values of “S000”, “SA01”, “SA02”, “SA03”, “SE01”, “SE02”, “SE03”, “SI01”, “SI02”, or “SI03”. Default is all workers. Please see https://lehd.ces.census.gov/data/lodes/LODES7/LODESTechDoc7.4.pdf for detail on the subset workforce segments

        type : From the LEHD documentation, this can have a value of "JT00" for All Jobs, "JT01" for Primary Jobs, "JT02" for All Private Jobs, "JT03" for Private Primary Jobs, "JT04" for All Federal Jobs, or "JT05" for Federal Primary Jobs.

        """

        # initial parameter checking

        year = int(year)
        if year < 2002:
            raise Exception('LEHD OD data is unavailable prior to 2002')
        if year > 2017:
            raise Exception('LEHD OD data is unavailable after to 2017')

        if geography not in ["B","BG","CT","C","S"]:

            raise Exception('Please make sure the input parameter @geography is one of ["B","BG","CT","C","S"]')

        if type not in ["JT00","JT01","JT02","JT03","JT04","JT05"]:

            raise Exception('Please make sure the input parameter @type is one of ["JT00","JT01","JT02","JT03","JT04","JT05"]')

        if seg not in ["S000", "SA01", "SA02", "SA03", "SE01", "SE02", "SE03", "SI01", "SI02"]:

            raise Exception('Please make sure the input parameter @seg is one of ["S000", "SA01", "SA02", "SA03", "SE01", "SE02", "SE03", "SI01", "SI02"]')


        # getting list of states to download data for

        states_for_dl = []
        if locations is not None:
            locations = pd.DataFrame(locations)
            locations.columns = ["o"]
            locations["gtype"] = locations["o"].apply(lehd.utils.infer_geog_input)
            states_for_dl = lehd.utils.get_state_alpha(locations, "o")
        else:
            raise Exception('Please input a list of locations to download data for')
        states_for_dl = list(set(list(states_for_dl)))


        # setting up the URLs needed for download, then download and put into a single pandas dataframe

        url_base = "https://lehd.ces.census.gov/data/lodes/LODES7/"
        dfl = []
        for state in states_for_dl:
            file_name = state.lower() + "_rac_" + seg + "_" + type + "_" + str(year) + ".csv.gz"
            url = url_base + state.lower() + "/rac/" + file_name
            print("Trying to download ", file_name, " from ", url, " ......")
            df = pd.read_csv(urllib.request.urlopen(url), compression = "gzip")
            dfl.append(df)
        df = pd.concat(dfl)

        # cleaning and adding leading 0s to block ids
        df["h_geoid_B"] = df["h_geocode"].astype(str)
        df["h_geoid_B"] = df["h_geoid_B"].str.zfill(15)
        del df["h_geocode"]

        # add column for aggregation, if applicable
        if geography != "B":
            df["h_geoid_" + geography] = df["h_geoid_B"].apply(lehd.utils.get_geoid, args = (geography,))


        # substting the data based on the input locations

        print("Subsetting the data based on the input locations list ...")
        dfm = []
        for geoid in list(locations["gtype"].unique()):
            if geoid != "B" and geoid != geography:
                df["h_geoid_" + geoid] = df["h_geoid_B"].apply(lehd.utils.get_geoid, args = (geoid,))
            list_unique = list(locations["o"][locations["gtype"] == geoid].unique())
            dfs = df[df["h_geoid_" + geoid].isin(list_unique)]["h_geoid_B"].unique()
            dfm = dfm + list(dfs)
        df = df.query("h_geoid_B in @dfm")


        # aggregating the output if applicable, and returning the resulting dataframe

        print("Finalizing the output ...")

        if geography == "B":
            return df
        else:
            output_values = ['C000', 'CA01', 'CA02', 'CA03', 'CE01', 'CE02', 'CE03', 'CNS01', 'CNS02', 'CNS03', 'CNS04', 'CNS05', 'CNS06', 'CNS07', 'CNS08', 'CNS09', 'CNS10', 'CNS11', 'CNS12', 'CNS13', 'CNS14', 'CNS15', 'CNS16', 'CNS17', 'CNS18', 'CNS19', 'CNS20', 'CR01', 'CR02', 'CR03', 'CR04', 'CR05', 'CR07', 'CT01', 'CT02', 'CD01', 'CD02', 'CD03', 'CD04', 'CS01', 'CS02']
            df = df.groupby(["h_geoid_" + geography])[output_values].sum().reset_index()
            return df
        print("Finished !!!")





    def od(year = 2016, geography = "B", type = "JT00", origins = None, destinations = None, constrained = "no"):

        """
        Downloads origin-destination (OD) commuting flow data into a pandas dataframe

        Parameters
        ----------
        year : int or str reperesenting the year to download data for

        geography : the geographic scale in which to aggregate data to
        "B"  | blocks
        "BG" | block groups
        "CT" | census tracts
        "P"  | places
        "CS" | county subdivision
        "C"  | counties
        "S"  | states
        the default are blocks, which are how the raw data is provided, which thus does not require aggregation

        type : from the LEHD docementation, this can have a value of "JT00" for All Jobs, "JT01" for Primary Jobs, "JT02" for All Private Jobs, "JT03" for Private Primary Jobs, "JT04" for All Federal Jobs, or "JT05" for Federal Primary Jobs.

        origins | list of origins to download data for, where origins are strings of GEOIDs. Must be specified if destinations is not specified

        destinations | list of destinations to download data for, where destinations are strings of GEOIDs. Must be specified if origins is not specified

        note: one of origins or destinations must be provided

        constrained : whether or not to only download data within a state
        "yes"  | download only the data from the input origins, to the input destinations,
        "no"   | download all data without OD constraints

        """


        # verifying the input parameters

        year = int(year)
        if year < 2002:
            raise Exception('LEHD OD data is unavailable prior to 2002')
        if year > 2017:
            raise Exception('LEHD OD data is unavailable after to 2017')

        if constrained not in ["yes","no"]:

            raise Exception('Please make sure the input parameter @constrained is one of ["yes","no"]')

        if geography not in ["B","BG","CT","C","S"]:

            raise Exception('Please make sure the input parameter @geography is one of ["B","BG","CT","C","S"]')

        if type not in ["JT00","JT01","JT02","JT03","JT04","JT05"]:

            raise Exception('Please make sure the input parameter @type is one of ["JT00","JT01","JT02","JT03","JT04","JT05"]')

        if origins is None and destinations is None:

            raise Exception("Please input a list of origins and/or a list of destinations")


        # creating dataframes for the origins and destinations, and grabbing the list of state alpha codes needed for downloading

        origin_states = []
        if origins is not None:

            origins = pd.DataFrame(origins)
            origins.columns = ["o"]
            origins["gtype"] = origins["o"].apply(lehd.utils.infer_geog_input)
            origin_states = lehd.utils.get_state_alpha(origins, "o")

        destination_states = []
        if destinations is not None:

            destinations = pd.DataFrame(destinations)
            destinations.columns = ["d"]
            destinations["gtype"] = destinations["d"].apply(lehd.utils.infer_geog_input)
            destination_states = lehd.utils.get_state_alpha(destinations, "d")

        states_for_dl = list(origin_states) + list(destination_states)
        states_for_dl = list(set(states_for_dl))



        # setting up the URLs needed for download, then download and put into a single pandas dataframe

        url_base = "https://lehd.ces.census.gov/data/lodes/LODES7/"
        dfl = []
        for state in states_for_dl:
            for part in ["aux", "main"]:
                file_name = state.lower() + "_od_" +  part + "_" + type + "_" + str(year) + ".csv.gz"
                url = url_base + state.lower() + "/od/" + file_name
                print("Trying to download ", file_name, " from ", url, " ......")
                df = pd.read_csv(urllib.request.urlopen(url), compression = "gzip")
                dfl.append(df)

        print("Concatinating data for the states in ", states_for_dl)
        df = pd.concat(dfl)



        # updating the GEOID to be strings and have leading 0s where appropriate

        df["h_geoid_B"] = df["h_geocode"].astype(str)
        df["h_geoid_B"] = df["h_geoid_B"].str.zfill(15)
        del df["h_geocode"]
        df["w_geoid_B"] = df["w_geocode"].astype(str)
        df["w_geoid_B"] = df["w_geoid_B"].str.zfill(15)
        del df["w_geocode"]



        # creating the geoid for the desired output geography

        if geography != "B":
            df["h_geoid_" + geography] = df["h_geoid_B"].apply(lehd.utils.get_geoid, args = (geography,))
            df["w_geoid_" + geography] = df["w_geoid_B"].apply(lehd.utils.get_geoid, args = (geography,))


        # subsetting data based on inputs

        # generating subset if origin data are input
        if origins is not None:
            print("Subsetting the data based on the input origin input list ...")
            dfm_o = []
            for geoid in list(origins["gtype"].unique()):
                if geoid != "B" and geoid != geography:
                    df["h_geoid_" + geoid] = df["h_geoid_B"].apply(lehd.utils.get_geoid, args = (geoid,))
                list_unique = list(origins["o"][origins["gtype"] == geoid].unique())
                dfs = df[df["h_geoid_" + geoid].isin(list_unique)]["h_geoid_B"].unique()
                dfm_o = dfm_o + list(dfs)

        # generating subset if destination geoid are input
        if destinations is not None:
            print("Subsetting the data based on the input destination input list ...")
            dfm_d = []
            for geoid in list(destinations["gtype"].unique()):
                if geoid != "B" and geoid != geography:
                    df["w_geoid_" + geoid] = df["w_geoid_B"].apply(lehd.utils.get_geoid, args = (geoid,))
                list_unique = list(destinations["d"][destinations["gtype"] == geoid].unique())
                dfs = df[df["w_geoid_" + geoid].isin(list_unique)]["w_geoid_B"].unique()
                dfm_d = dfm_d + list(dfs)

        # subsetting, based on the inputs
        if destinations is None:
            df = df.query("h_geoid_B in @dfm_o")
        elif origins is None:
            df = df.query("w_geoid_B in @dfm_d")
        else:
            if constrained == "no":
                df = df.query("w_geoid_B in @dfm_d or h_geoid_B in @dfm_o")
            if constrained == "yes":
                df = df.query("w_geoid_B in @dfm_d and h_geoid_B in @dfm_o")



        # aggregating by geography, and returning a dataframe

        print("Finalizing the output ...")
        if geography == "B":
            return df
        else:
            df = df.groupby(["h_geoid_" + geography,"w_geoid_" + geography])[["S000","SA01","SA02","SA03","SE01","SE02","SE03","SI01","SI02","SI03"]].sum().reset_index()
            return df
        print("Finished !!!")
