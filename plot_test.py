from bokeh.plotting import figure, output_file, show
import pandas as pd
import numpy as np

df = pd.read_csv('yellow_tripdata_2016-01.csv', usecols= \
    ['pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude'],nrows=100)
data = df
data = data[(data['pickup_longitude'] != 0)]
data = data[(data['dropoff_longitude'] != 0)]
data = data[(data['pickup_latitude'] != 0)]
data = data[(data['dropoff_latitude'] != 0)]
df = data


def lonlat_to_meters(df, lon_name, lat_name):
    lat = df[lat_name]
    lon = df[lon_name]
    origin_shift = 2 * np.pi * 6378137 / 2.0
    mx = lon * origin_shift / 180.0
    my = np.log(np.tan((90 + lat) * np.pi / 360.0)) / (np.pi / 180.0)
    my = my * origin_shift / 180.0
    df.loc[:, lon_name] = mx
    df.loc[:, lat_name] = my


lonlat_to_meters(df, 'pickup_longitude', 'pickup_latitude')
lonlat_to_meters(df, 'dropoff_longitude', 'dropoff_latitude')
# df.rename(columns={'Lon':'x', 'Lat':'y'}, inplace=True)

# df.tail()

NYC = x_range, y_range = ((-8242000, -8210000), (4965000, 4990000))

plot_width = int(750)
plot_height = int(plot_width // 1.2)


def base_plot(tools='pan,wheel_zoom,reset', plot_width=plot_width, plot_height=plot_height, **plot_args):
    p = figure(tools=tools, plot_width=plot_width, plot_height=plot_height,
               x_range=x_range, y_range=y_range, outline_line_color=None,
               min_border=0, min_border_left=0, min_border_right=0,
               min_border_top=0, min_border_bottom=0, **plot_args)

    p.axis.visible = False
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    return p


options = dict(line_color=None, fill_color='red', size=3)

from bokeh.tile_providers import STAMEN_TERRAIN
options1 = dict(line_color='blue', fill_color=None, size=10)

samples = df
p = base_plot()
p.add_tile(STAMEN_TERRAIN)
p.circle(x=samples['dropoff_longitude'], y=samples['dropoff_latitude'], **options)
p.square(x=samples['dropoff_longitude'][1:40], y=samples['dropoff_latitude'][1:40],angle=0.0, **options1)
show(p)