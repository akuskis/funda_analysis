#!/usr/bin/env python3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def load_data(filepath):
    data_frame = pd.read_json(filepath)

    # drop missed prices (by request and on auction)
    # TODO: rework dumper (we are not interested in records without valid price)
    mask_valid_price = (data_frame['price'] != 'on') & (data_frame['price'] != 'by')
    data_frame = data_frame[mask_valid_price]

    # prepare fields
    data_frame['price'] = data_frame['price'].str.replace(',', '').astype(float) / 1000
    data_frame['living_area'] = data_frame['living_area'].str.replace(',', '').astype(float)
    data_frame['year_of_construction'] = pd.to_numeric(data_frame['year_of_construction'], errors='coerce')

    return data_frame


data_frame = load_data('../scrapy/x.json')

# drop old buildings
mask_year_of_construction = data_frame['year_of_construction'] > 1990
data_frame = data_frame[mask_year_of_construction]

# filter by living area
mask_living_area = data_frame['living_area'].between(80, 100)
data_frame = data_frame[mask_living_area]

# filter 10% of cheapest and 10% of most expensive
df = pd.DataFrame()
for town in data_frame['town'].unique():
    partial_mask = data_frame['town'] == town
    min, max = data_frame[partial_mask]['price'].quantile([0.1, 0.9])
    mask = (data_frame['town'] == town) & (data_frame['price'].between(min, max))
    df = pd.concat([df, data_frame[mask]])
data_frame = df

# select some towns
mask_by_towns = (data_frame['town'] == 'Amsterdam') | (data_frame['town'] == 'Rotterdam') | (
            data_frame['town'] == 'Haarlem') | (data_frame['town'] == 'Utrecht')
data_frame = data_frame[mask_by_towns]

# draw plot
sns.boxplot(x="price", y="town", data=data_frame, orient='h')
plt.xlabel('Price in thousands of EUR')
plt.ylabel('Town')
plt.title('Distribution of Home Prices')
plt.show()
