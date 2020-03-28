from bokeh.plotting import figure, output_file, show
import pandas as pd
import numpy as np
import math
from bokeh.tile_providers import STAMEN_TERRAIN
NYC = x_range, y_range = ((-8242000, -8210000), (4965000, 4990000))
plot_width = int(750)
plot_height = int(plot_width // 1.2)
def lonlat_to_meters(df, lon_name, lat_name):
    lat = df[lat_name]
    lon = df[lon_name]
    origin_shift = 2 * np.pi * 6378137 / 2.0
    mx = lon * origin_shift / 180.0
    my = np.log(np.tan((90 + lat) * np.pi / 360.0)) / (np.pi / 180.0)
    my = my * origin_shift / 180.0
    df.loc[:, lon_name] = mx
    df.loc[:, lat_name] = my
def transform(output_read):
    min_lat = 40.5
    min_long = -74.25
    unit_length = 0.001
    output_read[:,1] = output_read[:,1]*unit_length + min_long
    output_read[:,0] = (output_read[:,0])*unit_length + min_lat
    df = pd.DataFrame(output_read,columns=['Dropoff_latitude', 'Dropoff_longitude'])
    return df

def cal_diameter(lon, lat):
    origin_shift = 2 * np.pi * 6378137 / 2.0
    mx = lon * origin_shift / 180.0
    my = np.log(np.tan((90 + lat) * np.pi / 360.0)) / (np.pi / 180.0)
    my = my * origin_shift / 180.0
    return mx,my
    # return np.sqrt(my*my + mx*mx)


def base_plot(tools='pan,wheel_zoom,reset', plot_width=plot_width, plot_height=plot_height, **plot_args):
    p = figure(tools=tools, plot_width=plot_width, plot_height=plot_height,
               x_range=x_range, y_range=y_range, outline_line_color=None,
               min_border=0, min_border_left=0, min_border_right=0,
               min_border_top=0, min_border_bottom=0, **plot_args)

    p.axis.visible = False
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    return p

def plot_all(df1,result):
    df = transform(result)
    n = 10
    step = 0.001 / n
    for index, row in df.iterrows():
        for j in range(1, n + 1):
            df.loc[df.shape[0]] = [row['Dropoff_latitude'] + step * j, row['Dropoff_longitude']]
        for j in range(1, n + 1):
            df.loc[df.shape[0]] = [row['Dropoff_latitude'] + step * j, row['Dropoff_longitude'] + 0.001]
        for j in range(1, n + 1):
            df.loc[df.shape[0]] = [row['Dropoff_latitude'], row['Dropoff_longitude'] + step * j]
        for j in range(1, n + 1):
            df.loc[df.shape[0]] = [row['Dropoff_latitude'] + 0.001, row['Dropoff_longitude'] + step * j]

    lonlat_to_meters(df1, 'Pickup_longitude', 'Pickup_latitude')
    lonlat_to_meters(df1, 'Dropoff_longitude', 'Dropoff_latitude')
    lonlat_to_meters(df, 'Dropoff_longitude', 'Dropoff_latitude')
    options = dict(line_color=None, fill_color='red', size=1)
    options1 = dict(line_color=None, fill_color='blue', size=2)
    p = base_plot()
    p.add_tile(STAMEN_TERRAIN)
    p.circle(x=df1['Dropoff_longitude'], y=df1['Dropoff_latitude'], **options)
    p.circle(x=df['Dropoff_longitude'], y=df['Dropoff_latitude'], **options1)
    show(p)

def plot_gird(output_read):
    result = transform(output_read)

    n = 10
    step = 0.001/n
    print(result)
    df = result
    for index, row in result.iterrows():
        for j in range(1, n + 1):
            df.loc[df.shape[0]] = [row['Dropoff_latitude'] + step * j, row['Dropoff_longitude']]
        for j in range(1, n + 1):
            df.loc[df.shape[0]] = [row['Dropoff_latitude'] + step * j, row['Dropoff_longitude'] + 0.001]
        for j in range(1, n + 1):
            df.loc[df.shape[0]] = [row['Dropoff_latitude'], row['Dropoff_longitude'] + step * j]
        for j in range(1, n + 1):
            df.loc[df.shape[0]] = [row['Dropoff_latitude'] + 0.001, row['Dropoff_longitude'] + step * j]
    print(df.shape)
    lonlat_to_meters(df, 'Dropoff_longitude', 'Dropoff_latitude')
    options = dict(line_color=None, fill_color='blue', size=2)
    p = base_plot()
    p.add_tile(STAMEN_TERRAIN)
    p.circle(x=df['Dropoff_longitude'], y=df['Dropoff_latitude'], **options)
    show(p)