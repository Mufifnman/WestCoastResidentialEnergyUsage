# WestCoastResidentialEnergyUsage
A Python Script I threw together to parse US EIA data and make a few plots
I got the data from these queries

[Washington Natural gas distributed](https://www.eia.gov/dnav/ng/ng_cons_sum_dcu_SWA_a.htm)

[Electric generation in PWC](https://www.eia.gov/electricity/data/browser/#/topic/0?agg=2,0,1&fuel=vg&geo=g10000000007&sec=g&linechart=ELEC.GEN.ALL-US-99.A&columnchart=ELEC.GEN.ALL-US-99.A&map=ELEC.GEN.ALL-US-99.A&freq=A&ctype=linechart&ltype=pin&rtype=s&maptype=0&rse=0&pin=)

[Electricity usage by Type in PNC](https://www.eia.gov/electricity/data/browser/#/topic/5?agg=0,1&geo=g10000000007&endsec=vg&linechart=ELEC.SALES.US-ALL.A&columnchart=ELEC.SALES.US-ALL.A&map=ELEC.SALES.US-ALL.A&freq=A&ctype=linechart&ltype=pin&rtype=s&maptype=0&rse=0&pin=)

The charts are for Washington, Oregon, and California, West Coast (which is all three) and the United States, sectors are Residential, Commertial, and Industrial.
1) Natural Gas usage by sector (with electrical utility as a sector)
2) Electrical Utility usage by sector
3) I took the electrical utility usage by sector and applied it to the Natural gas usage to approximate the total use by sector, even if some is converted to electricity first.  I have two pie charts for each of these, one with it added to the total sum, as well as in its own section (e.g. 'resedential electric' as the approximate portion of the natural gas burned for energy that went to resedential uses as electricity).
