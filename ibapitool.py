#!/usr/bin/env python
# coding: utf-8

# This utility uses the pandas library to fethch data from the [IONOS Billing
# API](https://api.ionos.com/docs/billing/v3/) endpoints (Utilization nad
# Products) and combine them to a flat table that can be further processed in
# excel or other table based tools

# General Notes for using the Billing API

# - The Utilisation data is calculated "at the end of the day". For example
# data traffic caused today will be available in the API on the following day.
# The API does not deliver real time data

# - There are three very similar looking endpoints - "utilization", "usage" and
# "env". "Usage" is a legacy endpoint that delivers more summarized and less
# detailed information. env (Comes from the german word
# "Einzelverbindungsnachweis") can also be considered legacy as it does not
# contain S3 data. Here we just use the Utilization endpoint. It provides more
# details and you can always ignore filters/fields that are not use. 


# Import libraries to get data from the REST API. Pandas is used for data analysation and reporting
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import argparse
import re, os

parser = argparse.ArgumentParser(
        prog="ibapitool",
        description="tool to fetch data from the billing API. The tool uses the Utilization and Product (prices) endpoints, joins the tables and outputs the result as a CSV table"
        )

parser.add_argument("contract",
        help="Contract number")
parser.add_argument("-p","--period",
        help="Invoicing period (e.g. 2023-07)",default="")
parser.add_argument("-d","--dc",
        help="Return data just for the given datacenter UUID (all returned by default)")
parser.add_argument("-r","--resource",
        help="Return data just for the given resource UUID, such as VM or NIC (all returned by default)")
parser.add_argument("-t","--type",
        help="Return data just for the given resource type (all returned by default)")
parser.add_argument("-s","--separator",
        help="Separator for the CSV data (default='%(default)s')",default=";")
parser.add_argument("-F","--float-format",dest="float_format",
        help="Float format in the resulting csv file (default='%(default)s')",
        default="%.2f")
parser.add_argument("-D","--date-format",dest="date_format",
        help="Date format in the resulting csv file (default='%(default)s')",
        default="%Y-%m-%d %H:%M")

args = parser.parse_args()


# Setup Authentication - You need to user the contract owner credential when
# using the Billing API. The Billing API does not currently does not support
# token authentication. You can set the variables for example like this:

# export IONOS_USERNAME=jane.doe@example.com
# read -s -p "Password: " IONOS_PASSWORD
#
# Q: Why not just use command line parameters? 
# A: Because it is bad practice for credentials. The values are written in the command line history

args.user = os.getenv("IONOS_USERNAME")
args.password = os.getenv("IONOS_PASSWORD")


if args.user is None or args.password is None:
    print("you need to set the contract owner credentials to environment variables IONOS_USERNAME and IONOS_PASSWORD")
    exit(1)

auth=HTTPBasicAuth(args.user, args.password)


# # Fetch and Prepare the Data - fetching here means requesting the data from the
# API and the preparation is mostly just flattening the nested JSON data. Flat
# table data is easier to use for reporting and data analyzation. ## Getting
# the Utilization Data

query_params=[]
for p in ["dc","resource","type"]:
    a=vars(args)[p]
    if a:
        query_params.append(p+"="+a)

if query_params:
    query_params="?"+"&".join(query_params)
else:
    query_params=""

# get the data from the API. Its nested JSON data
r=requests.get(f"https://api.ionos.com/billing/{args.contract}/utilization/{args.period}{query_params}",auth=auth)
d=r.json()
print(f"https://api.ionos.com/billing/{args.contract}/utilization/{args.period}{query_params}")

# Check that we have a valid result
if "datacenters" not in d:
    print(d)
    exit(1)
if not d["datacenters"]:
    print("no results with the given query")
    exit(1)

meters=[]

# The data in the API is nested json. Great for applications but not so great
# for a table presentation. Here we first modify or "flatten" the data to get a
# better table presentation that can be further exported as CSV if needed.
for dc in d["datacenters"]:
    for meter in dc["meters"]:
        meter["dc"]=dc["name"]
        meter["unit"]=meter["quantity"]["unit"]
        meter["quantity"]=meter["quantity"]["quantity"]
        meters.append(meter)

# make a pandas dataframe of the flattened data
meters=pd.DataFrame(meters)

# convert the string times to datetime data format
for f in ["from","to"]:
    meters[f]=pd.to_datetime(meters[f])

# reorder columns and show the most important ones
utilization=meters[["type","dc","from","to","meterId","meterDesc","region","quantity","unit"]]

# now we have the data in a nice flat table **But**, there is something obvious
# missing in the table and that is the quantity or usage in terms for dollars
# or Euros. In other words, the price is missing. We are going to add this
# information in the next steps

# The utilization API gives units and meters of usage (GB, hours etc) but it
# does not include the prices. In order to see the consumption in termns of
# money we need to combine it with the data from the Products API which
# contains the unit price.

# Fetch the product JSON data from the API
r=requests.get(f"https://api.ionos.com/billing/{args.contract}/products",auth=auth)
products=pd.DataFrame( r.json()["products"])

# Again, the data is nested, but Luckily not that deep. We need to do just some
# minimal data flattening to make it usable for our our purposes flatten the
# unitCost to quantity and unit and the delete it

products["price"]=products["unitCost"].apply(lambda x:x["quantity"]).astype(float)
products["unit"]=products["unitCost"].apply(lambda x:x["unit"])
products=products.drop(columns=["unitCost","deprecated"])

# Now we have a nice clean table that contains the meterId and unit price. The inner join will drop
# elements from the utilization table that do not have a corresponding product and price. Utilization
# of products with no price are not of intrest for cost reporting
combined = pd.merge(utilization, products[["meterId","price"]],how="inner",on="meterId")

# make the meterDesc string a bit shorter (many contain the "+1 hyperthred.." string)
combined.loc[:,"meterDesc"]=combined.meterDesc.str.replace(r"(+1 hyperthread core)","",regex=False)

# we need to multiply the "quantity" from the utilization table with unit price
# in the products table. we will use the meterId as the key.

# multiply the price with the cuantity and we will have the cost for the given time window
combined=combined.assign(cost=combined["quantity"]*combined["price"])

# The S3 API calls does not cost anything so lets remove them from our statistics to get the results
# a bit cleaner
costs=combined[~combined.meterDesc.str.contains("S3 API")].copy()

print(costs.to_csv(index=None,sep=args.separator,float_format=args.float_format,
    date_format=args.date_format))
