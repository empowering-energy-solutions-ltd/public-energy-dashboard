# Energy Dashboard

The energy systems performance dashboard assesses gas and electricity consumption and invoice data to help site managers have a clearer understanding of their energy consumption & spend.

This can be locally run by going to `main.py` and running the script (username and passwords are at the begining of the `main.py` file).

If you want to upload your own sites data to be visualised you can find examples of the various input data types in `src > data`.

The current version has 4 tabs:

1. Overview - This take contains a sankey diagram of the site's energy system. This can be altered by changing the sankey data in the `src.utils.schema.py` and `src.components.summary_plots.py`. The tab also has a table and line plot of the year on year energy consumption of the site with the table also showing the min, max and mean values for each months energy consumption.

2. Power - This tab holds a load duration curve that highlights the sites power demand usage, ensure you update the `POWER_LIMS` variable in `src.componenets.power_plots.py` if using on personal data so that the power demand limit is updated for your meters. There is also a peak demand table and lineplot that highglights the top 10 biggest power demand peaks in the dataset, or filtered dataset. This is designed to help site managers identify potential periods of repeated high demand to try and avoid more in future.

3. Consumption - This tab holds a baseline plot highlighting the average baseload consumption (default is monthly baseload), and a lineplot and table highlighting off hours of high consumption. This is designed to help site managers identify periods outside of normal operating hours that are exibiting unusually high consumption. Ensure you update the `WORK_HOURS` dict in `src.components.consumption_plots.py` to your specific site opening hours to ensure accruate results.

4. Cost - The cost tab is unfinished but currently shows the breakdown of energy bills in either cost (£) or as a percentage of the bill. This is helpful to see the breakdown of energy bills over time. In the example data plot, you'll notice that standing charges rise quite significantly against other percentage parts of the bill.

