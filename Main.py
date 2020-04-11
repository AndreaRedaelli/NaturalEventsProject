import WSCall


if (__name__ == "__main__"):
    limit=""
    days="20"
    source=""
    status=""
    #df = WSCall.callWS(limit,days,source,status)

    df = WSCall.GetImage("LAYERS=VIIRS_SNPP_CorrectedReflectance_TrueColor&STYLES=&FORMAT=image%2Fpng&TRANSPARENT=true&HEIGHT=256&WIDTH=256&TIME=2020-03-01&CRS=EPSG:4326&BBOX=-61,-81,-28,-48");
    print(df)
