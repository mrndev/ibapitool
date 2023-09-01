# ibapitool
utility to fetch data from the Billing API

```
usage: ibapitool [-h] [-p PERIOD] [-s SEPARATOR] contract

tool to fetch data from the billing API. The tool uses the Utilization and Product endpoints to fetch data on daily granularity, combines the tables and
outputs the result as a CSV table

positional arguments:
  contract              Contract number

options:
  -h, --help            show this help message and exit
  -p PERIOD, --period PERIOD
                        Invoicing period (e.g. 2023-07)
  -s SEPARATOR, --separator SEPARATOR
                        Separator for the CSV data (default=';')
```

Example:
```
 python3 ibapitool.py --period 2023-07 1298734
;type;dc;from;to;meterId;meterDesc;region;quantity;unit;price;cost
0;STORAGE;MartinsDC;2023-07-01 00:00:00+00:00;2023-07-31 23:59:59.999000+00:00;S02000;30d per 1GB SSD Premium Storage;de/txl;103.33333333333333;1G*30Days;0.19;19.633333333333333
1;STORAGE;MartinsDC;2023-07-01 00:00:00+00:00;2023-07-31 23:59:59.999000+00:00;S02000;30d per 1GB SSD Premium Storage;de/txl;620.0;1G*30Days;0.19;117.8
2;STORAGE;MartinsDC;2023-07-01 00:00:00+00:00;2023-07-31 23:59:59.999000+00:00;S02000;30d per 1GB SSD Premium Storage;de/txl;620.0;1G*30Days;0.19;117.8
3;STORAGE;MartinsDC;2023-07-01 00:00:00+00:00;2023-07-31 23:59:59.999000+00:00;S02000;30d per 1GB SSD Premium Storage;de/txl;620.0;1G*30Days;0.19;117.8
4;STORAGE;MartinsDC;2023-07-01 00:00:00+00:00;2023-07-31 23:59:59.999000+00:00;S02000;30d per 1GB SSD Premium Storage;de/txl;103.33333333333333;1G*30Days;0.19;19.633333333333333
5;STORAGE;Application LB test de/fra;2023-07-01 00:00:00+00:00;2023-07-31 23:59:59.999000+00:00;S02000;30d per 1GB SSD Premium Storage;de/fra;10.333333333333334;1G*30Days;0.19;1.9633333333333334
```
