Energy systems performance dashboard
==============================

Documentation available at: https://fluffy-bassoon-gql6w3l.pages.github.io/

The energy systems performance dashboard assesses gas and electricity consumption and invoice data to help site managers have a clearer understanding of their energy consumption & spend.

This can be locally run by going to `main.py` and running the script (username and passwords are at the begining of the `main.py` file).

If you want to upload your own sites data to be visualised you can find examples of the various input data types in `src > data`.

The current version has 4 tabs:

1. Overview - This take contains a sankey diagram of the site's energy system. This can be altered by changing the sankey data in the `src.utils.schema.py` and `src.components.summary_plots.py`. The tab also has a table and line plot of the year on year energy consumption of the site with the table also showing the min, max and mean values for each months energy consumption.

2. Power - This tab holds a load duration curve that highlights the sites power demand usage, ensure you update the `POWER_LIMS` variable in `src.components.power_plots.py` if using on personal data so that the power demand limit is updated for your meters. There is also a peak demand table and lineplot that highglights the top 10 biggest power demand peaks in the dataset, or filtered dataset. This is designed to help site managers identify potential periods of repeated high demand to try and avoid more in future.

3. Consumption - This tab holds a baseline plot highlighting the average baseload consumption (default is monthly baseload), and a lineplot and table highlighting off hours of high consumption. This is designed to help site managers identify periods outside of normal operating hours that are exibiting unusually high consumption. Ensure you update the `WORK_HOURS` dict in `src.components.consumption_plots.py` to your specific site opening hours to ensure accruate results.

4. Cost - The cost tab is unfinished but currently shows the breakdown of energy bills in either cost (£) or as a percentage of the bill. This is helpful to see the breakdown of energy bills over time. In the example data plot, you'll notice that standing charges rise quite significantly against other percentage parts of the bill.


Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    │ 
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │ 
    ├── assets   <- Holds logo that goes in the sidebar and .css style sheet for the styling
    │ 
    ├── main.py   <- Script to run to initialise the web app.
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── components           <- Scripts to generate the tab contents
    │   │   │                 
    │   │   ├── consumption_plots.py <- Scripts to generate the plots for the consumption tab
    │   │   ├── cost_plots.py <- Scripts to generate the plots for the cost tab
    │   │   ├── filter_objects.py <- Scripts to generate filtering objects and format them.
    │   │   ├── gen_content_obj.py <- Scripts to add generic objects to different tab objects
    │   │   ├── layout.py <- Script to generate the layout of the dash app
    │   │   ├── line_fig.py <- Scripts to generate plotly lineplots, used by most tabs
    │   │   ├── power_plots.py <- Scripts to generate the plots for the power tab
    │   │   ├── sidebar.py <- Scripts to render the navigation sidebar 
    │   │   ├── submeter_plots.py <- Scripts to generate the plots for the submeter tab (currently not in use)
    │   │   └── summary_plots.py <- Scripts to generate the plots for the summary tab
    │   │
    │   ├── data       <- Scripts and files used for plots and tables in dash app
    │   │   │                 
    │   │   ├── duos_data.csv <- Example price profile data, was used in cost tab but plot has been removed from deployment version 
    │   │   ├── elec_hh_data.csv <- Example electricity half-hourly energy consumption data
    │   │   ├── electric_invoice_data.csv <- Example electricity invoice data   
    │   │   ├── gas_hh_data.csv <- Example gas half-hourly energy consumption data            
    │   │   ├── gas_invoice_data.csv <- Example gas invoice data              
    │   │   ├── loader.py <- Scripts for loading app data for plot/table creation
    │   │   └── metadata.py <- .py file holding e2sviz metadata dicts used in project for e2sviz plotting functionality
    │   │
    │   ├── tabs       <- Scripts to generate the different tabs            
    │   │   ├── consumption_tab.py <- Scripts to generate the consumption tab
    │   │   ├── cost_tab.py <- Scripts to generate the cost tab            
    │   │   ├── general_tab.py <- Script of render function for rendering different sections of the tabs    
    │   │   ├── overview_tab.py <- Scripts to generate the overview tab 
    │   │   └── power_tab.py <- Scripts to generate the power tab
    │   │
    │   └── utils  <- Scripts to create exploratory and results oriented visualizations   
    │       ├── IDS.py <- Script holding IDs for tabs, meters and content types
    │       ├── page_text.py <- Script holding the html dash text content of each of the different tabs
    │       └── schema.py <- Schema file holding general information used by the different files
    │ 
    └── Procfile   <- Required file for deployment through Heroku.


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
