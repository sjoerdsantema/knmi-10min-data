# knmi-10min-data
Collect the 10 minute actuals from the KNMI API, store locally on file and convert the data into a list with dictionaries

# api documentation here
https://developer.dataplatform.knmi.nl/apis/5f846a2b7ce0830001941167/documentation/

# get an api key here
https://developer.dataplatform.knmi.nl/get-started#obtain-an-api-key

# variables in nc file
    dimensions(sizes): station(52), time(1)
    variables(dimensions): 
    <class 'str'> station(station), 
    float64 time(time), 
    <class 'str'> stationname(station), 
    float64 lat(station), 
    float64 lon(station), 
    float64 height(station), 
    float64 dd(station, time), => windrichting
    float64 ff(station, time), => windsnelheid (m/s)
    float64 gff(station, time), => windvlagen (m/s)
    float64 ta(station, time), => temperatuur
    float64 rh(station, time), => luchtvochtigheid (%)
    float64 pp(station, time), => luchtdruk
    float64 zm(station, time), => zicht (m)
    float64 D1H(station, time), => regenval in laatste uur(min)
    float64 dr(station, time), => regenval duur in laatste 10m (sec)
    float64 hc(station, time), => hoogte wolkendek (voet)
    float64 hc1(station, time), 
    float64 hc2(station, time), 
    float64 hc3(station, time), 
    float64 nc(station, time), => wolkendek
    float64 nc1(station, time), 
    float64 nc2(station, time), 
    float64 nc3(station, time), 
    float64 pg(station, time), => neerslag gemiddeld in 10 min (mm/h)
    float64 pr(station, time), => neerslag duur 10 min (sec)
    float64 qg(station, time), => globale zonnestraling
    float64 R12H(station, time), => neerslag in laatste 12 uur (mm)
    float64 R1H(station, time), => neerslag in laatste 1 uur (mm)
    float64 R24H(station, time), => neerslag in laatste 24 uur (mm)
    float64 R6H(station, time), => neerslag in laatste 6 uur (mm)
    float64 rg(station, time), => neerslag intensiteit in 10 min (mm/h)
    float64 ss(station, time), => duur zonneschijn (min)
    float64 td(station, time), => dauwpunt (celcius)
    float64 tgn(station, time), => temperatuur gras 10cm (celcius)
    float64 Tgn12(station, time), 
    float64 Tgn14(station, time), 
    float64 Tgn6(station, time), 
    float64 tn(station, time), 
    float64 Tn12(station, time), 
    float64 Tn14(station, time), 
    float64 Tn6(station, time), 
    float64 tx(station, time), 
    float64 Tx12(station, time), 
    float64 Tx24(station, time), 
    float64 Tx6(station, time), 
    float64 ww(station, time), 
    float64 pwc(station, time), 
    float64 ww-10(station, time), 
    float64 ts1(station, time), 
    float64 ts2(station, time), 
  
