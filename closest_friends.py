#coding:windows-1252
from dateutil import parser
import json
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, AutoDateFormatter, AutoDateLocator
from statsmodels.nonparametric.kernel_regression import KernelReg, EstimatorSettings
import statsmodels.api as sm
import sys

filepath = sys.argv[1]
years = YearLocator()   # every year
months = MonthLocator()  # every month
yearsFmt = DateFormatter('%Y')
monthsFmt = DateFormatter('%M')

conversations = json.load(open(filepath, encoding='utf8'))

d1 = int(time.mktime(datetime.date(2010,1,1).timetuple()))
d2 = int(time.mktime(datetime.date(2016,1,1).timetuple()))
binz = list(range(d1,d2,int((d2-d1)/300)))

def get_conversation(conv_name):
    global binz

    conv = conversations[conv_name]
    only_times = [parser.parse(msg["time"]).timestamp() for msg in conv]
    points, bins = np.histogram(only_times, bins=binz)
    bins = bins[:-1]
    dates = [datetime.datetime.fromtimestamp(t) for t in bins]
    regressor = KernelReg(points, np.arange(len(points)), 'c', bw=3*np.ones(len(points)))
    smoothed, sm_mfx = regressor.fit()
    print(regressor.bw)

    return points, dates, smoothed
   
# Top 5
conv_names_sorted = sorted(conversations.keys(), key=lambda conv_name: len(conversations[conv_name]), reverse=True)
conv_names_sorted = [conv_name for conv_name in conv_names_sorted if len(conv_name.split(",")) == 2]
top5 = conv_names_sorted[:5]

fig, ax = plt.subplots()
for conv in top5:
    y, x, y_s = get_conversation(conv)
    p = ax.plot_date(x, y_s, '-', label=conv)
    plt.setp(p, linewidth=3)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)

# format the ticks
locator = AutoDateLocator()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(AutoDateFormatter(locator))
ax.autoscale_view()
fig.autofmt_xdate()


plt.show()