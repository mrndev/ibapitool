# ibapitool

Troubleshooting/monitoring utility for billing data. The utility fetches data
from the billing API (usage and prices) and combines them to a flat csv table. The
script also serves as a generic example how to use the Billing  API.

## Example:
Set and export the credential environment variables
```bash
read IONOS_USERNAME
read -s IONOS_PASSWORD
export IONOS_USERNAME IONOS_PASSWORD
```
read the data wrom IONOS APIs with the ibapitool (type and period are optional)
```bash
python3 ibapitool.py --period 2023-09 --type=S3 127538398
```
The output will be something like this
<pre>
<b>type;dc;from;to;meterId;meterDesc;region;quantity;unit;price;cost</b>
S3;S3;2023-09-02 00:00;2023-09-02 23:59;S3TI1000;1 GB S3 common traffic incoming;de/fra;0.00;1G;0.00;0.00
S3;S3;2023-09-01 00:00;2023-09-01 23:59;S3TI1000;1 GB S3 common traffic incoming;de/fra;0.00;1G;0.00;0.00
S3;S3;2023-09-02 00:00;2023-09-02 23:59;S3TO1000;1 GB S3 common traffic outbound;de/fra;0.00;1G;0.00;0.00
S3;S3;2023-09-01 00:00;2023-09-01 23:59;S3TO1000;1 GB S3 common traffic outbound;de/fra;0.00;1G;0.00;0.00
S3;S3;2023-09-02 00:00;2023-09-02 23:59;S3SU1100;30d per 1GB S3 Object Storage for first 50TB;de/fra;11.52;1G*30Days;0.01;0.17
S3;S3;2023-09-01 00:00;2023-09-01 23:59;S3SU1100;30d per 1GB S3 Object Storage for first 50TB;de/fra;11.52;1G*30Days;0.01;0.17
 </pre>


## Usage
```
usage: ibapitool [-h] [-p PERIOD] [--dc DC] [-r RESOURCE] [--type {SERVER,STORAGE,SNAPSHOT,NATGATEWAY,NIC,IP,IP_ADDRESS,CUBETEMPLATE,LOADBALANCER,BACKUP,S3,TRAFFIC,DB}] [-v]
                 [-s SEPARATOR] [-F FLOAT_FORMAT] [-D DATE_FORMAT]
                 contract

tool to fetch data from the billing API. The tool uses the Utilization and Product (prices) endpoints, joins the tables and outputs the result as a CSV table

positional arguments:
  contract              Contract number

options:
  -h, --help            show this help message and exit
  -p PERIOD, --period PERIOD
                        Invoicing period (e.g. 2023-07)
  --dc DC               Return data just for the given datacenter UUID (all returned by default)
  -r RESOURCE, --resource RESOURCE
                        Return data just for the given resource UUID, such as VM or NIC (all returned by default)
  --type {SERVER,STORAGE,SNAPSHOT,NATGATEWAY,NIC,IP,IP_ADDRESS,CUBETEMPLATE,LOADBALANCER,BACKUP,S3,TRAFFIC,DB}
                        Return data just for the given resource type (all returned by default)
  -v, --verbose         print some troubleshooting information
  -s SEPARATOR, --separator SEPARATOR
                        Separator for the CSV data (default=';')
  -F FLOAT_FORMAT, --float-format FLOAT_FORMAT
                        Float format in the resulting csv file (default='%.2f')
  -D DATE_FORMAT, --date-format DATE_FORMAT
                        Date format in the resulting csv file (default='%Y-%m-%d %H:%M')

```

