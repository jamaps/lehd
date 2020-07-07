import pandas as pd

class utils:

    def get_state_alpha(df, id):

        """
        joins state alpha codes to a dataframe with state numeric codes
        """

        df["state_numeric"] = df[id].astype(str).str[0:2]

        state_codes = [["AL","01"],["AK","02"],["AS","60"],["","03"],["AZ","04"],["AR","05"],["BI","81"],["CA","06"],["","07"],["CO","08"],["CT","09"],["DE","10"],["DC","11"],["FL","12"],["FM","64"],["GA","13"],["","14"],["GU","66"],["HI","15"],["HI","84"],["ID","16"],["IL","17"],["IN","18"],["IA","19"],["JI","86"],["JA","67"],["KS","20"],["KY","21"],["KR","89"],["LA","22"],["ME","23"],["MH","68"],["MD","24"],["MA","25"],["MI","26"],["MI","71"],["MN","27"],["MS","28"],["MO","29"],["MT","30"],["NI","76"],["NE","31"],["NV","32"],["NH","33"],["NJ","34"],["NM","35"],["NY","36"],["NC","37"],["ND","38"],["MP","69"],["OH","39"],["OK","40"],["OR","41"],["PW","70"],["PA","95"],["PA","42"],["","43"],["PR","72"],["RI","44"],["SC","45"],["SD","46"],["TN","47"],["TX","48"],["UM","74"],["UT","49"],["VT","50"],["VA","51"],["","52"],["VI","78"],["WI","79"],["WA","53"],["WV","54"],["WI","55"],["WY","56"]]

        state_codes = pd.DataFrame(state_codes, columns = ["state_alpha","state_numeric"])

        return pd.merge(df, state_codes, on = "state_numeric")["state_alpha"].unique()


    def infer_geog_input(geoid):

        """
        infers the geography type based on the length of a GEOID
        """

        if len(geoid) == 2:
            return "S"
        elif len(geoid) == 5:
            return "C"
        elif len(geoid) == 10:
            return "CS"
        elif len(geoid) == 7:
            return "P"
        elif len(geoid) == 11:
            return "CT"
        elif len(geoid) == 12:
            return "BG"
        elif len(geoid) == 15:
            return "B"
        else:
            return "error"


    def get_geoid(block_id, gtype):

        """
        gets the GEOID for different higher level geographies from a block GEOID
        """

        if gtype == "S":
            return(block_id[0:2])
        elif gtype == "C":
            return(block_id[0:5])
        elif gtype == "CS":
            return(block_id[0:10])
        elif gtype == "P":
            return(block_id[0:7])
        elif gtype == "CT":
            return(block_id[0:11])
        elif gtype == "BG":
            return(block_id[0:12])
        else:
            None
