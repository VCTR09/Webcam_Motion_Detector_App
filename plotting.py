# from motion_detector import df
# from bokeh.plotting import figure, output_file, show
# from bokeh.models import HoverTool, ColumnarDataSource

# # df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
# # df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

# cds = ColumnarDataSource(df)

# p = figure(x_axis_type='datetime', height=100, width=500, sizing_mode='scale_width', title="Motion Graph")
# # убрать отметки на вертикальной оси
# p.yaxis.minor_tick_line_color = None
# # убрать горизонтальную сетку
# p.yaxis[0].ticker.desired_num_ticks=1

# # hover = HoverTool(tooltips=[("Start", "@Start_string"),("End", "@End_string")])
# hover = HoverTool(
#     tooltips = [
#         ("Start", "@Start{%d/%m/%Y %H:%M:%S}"),
#         ("End", "@End{%d/%m/%Y %H:%M:%S}")
#     ],
#     formatters = {
#         "@Start" : "datetime",
#         "@End" : "datetime"
#     }
# )

# p.add_tools(hover)

# q = p.quad(left="Start", right="End", bottom=0, top=1, color="green", sourse=cds)

# output_file("Graph.html")
# show(p)

from motion_detector import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource
import pandas
 
cds = ColumnDataSource(df)
 
p = figure(
    x_axis_type = "datetime",
    height = 100,
    width = 500,
    sizing_mode = "scale_both",
    title = "Motion graph"
)
 
p.yaxis.minor_tick_line_color = None
p.yaxis[0].ticker.desired_num_ticks = 1
 
hover = HoverTool(
    tooltips = [
        ("Start", "@Start{%d/%m/%Y %H:%M:%S}"), 
        ("End", "@End{%d/%m/%Y %H:%M:%S}")
    ],
    formatters = {
        "@Start" : "datetime",
        "@End" : "datetime"
    }
)
p.add_tools(hover)
 
q = p.quad(
    left = "Start", 
    right = "End", 
    bottom = 0, 
    top = 1,
    color = "green",
    source = cds
)
 
output_file("Graph.html")
show(p)