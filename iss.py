from skyfield.api import load, wgs84
import utm
import time

#create a function to get UTM coordinates from lat/long
def get_utm(lat, lon):
    #convert lat/long to UTM
    return utm.from_latlon(lat, lon)
    #return UTM coordinates

stations_url = 'http://celestrak.com/NORAD/elements/stations.txt?'
satellites = load.tle_file(stations_url)
print('Loaded', len(satellites), 'satellites')

by_name = {sat.name: sat for sat in satellites}
satellite = by_name['ISS (ZARYA)']
print(satellite)
#print(satellite.epoch.utc_jpl())
print(satellite.epoch.utc_jpl())

ts = load.timescale()
t = ts.now()

days = t - satellite.epoch
print('{:.3f} days away from epoch'.format(days))
if abs(days) > 14:
    print('WARNING: Satellite is more than 2 weeks away from epoch')
    satellites = load.tle_file(stations_url, reload=True)
else:
    print('Satellite is within 2 weeks of epoch')

while 1:
    t = ts.now()

    geocentric = satellite.at(t)
    subpoint = wgs84.subpoint(geocentric)
    print("\n========================\n")
    print('Latitude:', subpoint.latitude)
    print('Longitude:', subpoint.longitude)
    print('Elevation (m):', int(subpoint.elevation.m))

    bluffton = wgs84.latlon(48.856613, 2.352222)

    difference = satellite - bluffton
    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()

    if alt.degrees > 0:
        print('The ISS is above the horizon')

    print("Altitude:", alt)
    print("Azimut:", az)
    print(int(distance.km), 'km de distance par rapport à Paris')

    #call the function to get UTM coordinates
    utm_val= get_utm(float(subpoint.latitude.degrees), float(subpoint.longitude.degrees))
    print(utm_val)
    time.sleep(5)

