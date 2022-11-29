import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# create dataframe
r = pd.read_csv("finance_liquor_sales.csv")
df = pd.DataFrame(r)
print(df.dtypes)

# make date type
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year

# keep only years in range 2016 - 2019
df1 = df[df["year"] >= 2016]
df2 = df1[df1["year"] <= 2019]

# create a new file
df2.to_csv("liquor.csv")

# create new dataframe
r = pd.read_csv("liquor.csv")
df = pd.DataFrame(r)
print(df.head())
print(df.tail())
df.drop(columns=df.columns[0], axis=1, inplace=True)


# group by zip code
zc = df.groupby("zip_code", as_index=False)["bottles_sold"].max()


# find indexes of items description and put them in zc
L = []
item_des = []
for i in range(len(df)):
    for j in range(len(zc)):
        if (df.loc[i, "zip_code"] == zc.loc[j, "zip_code"]) and \
                (df.loc[i, "bottles_sold"] == zc.loc[j, "bottles_sold"]):
            L.append(i)
for i in L:
    for j in range(len(df)):
        if i == j:
            item_des.append(df.loc[j, "item_description"])
zc["item_description"] = item_des
zc.dropna(inplace=True)


# group by store and create the percentage of sales
df["%sales"] = (df["sale_dollars"]/df["sale_dollars"].sum()) * 100
sn = df.groupby("store_name", as_index=False)["%sales"].sum()
sn["%sales"] = sn["%sales"].round(3)
sn.dropna(inplace=True)


# Hexagonal Bin Plot for the most popular item per zip code
plt.xlabel("Zip code")
plt.ylabel("Total sales of the most popular item")
plt.title("Most Popular Item Per Zip Code")
plt.hexbin(x=zc['zip_code'], y=zc['bottles_sold'], gridsize=45, cmap='Greens')
plt.savefig("zipcode.png")
plt.show()


# Treemap for the most popular item per zip code
f1 = px.treemap(zc, path=["zip_code", "item_description"], values="bottles_sold",
                color="bottles_sold", title="Most Popular Item Per Zip Code")
f1.update_traces(hovertemplate="%{label}<br>%{value}<br>%{parent}")
f1.write_html("zip_items.html", auto_open=True)


# Treemap for the percentage of sales per store
f2 = px.treemap(sn, path=["store_name"], values="%sales", color="%sales", title="Percentage Of Sales Per Store")
f2.update_traces(hovertemplate="%{label}<br>%{value}")
f2.write_html("stores.html", auto_open=True)
