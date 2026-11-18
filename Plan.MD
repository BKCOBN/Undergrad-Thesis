# Timeline

## Course deadlines (official, Brightspace + supervisor)
- project proposal - Fri Jan 8, submit on Brightspace + send to Pearce (completion check) - lands in week 8
- progress report - Wed Feb 24, submit on Brightspace + send to Pearce (completion check) - lands right at the start of week 15
- final thesis submission - Mon Mar 29 - week 19 got shortened so this lands right at the end of it, not buried mid-week
- all project artefacts sent to Pearce - Fri Apr 9 - covered by weeks 20-21
- presentation booked with Pearce - on or before Apr 9 - also weeks 20-21

## Week 1 (Nov 18 - Nov 24): get set up + sort out axis 2
- set up `code/` folder (python - pandas, geopandas, rasterio/rioxarray, matplotlib, plotly, `requirements.txt`), `datasets/raw/`, `datasets/processed/`
- install QGIS, make sure Zonal Statistics plugin + Processing toolbox actually work
- grab: Global Solar Atlas PVOUT global raster (GeoTIFF, globalsolaratlas.info/download, need to register), NASA SEDAC GPWv4 population density raster (GeoTIFF, need a free NASA Earthdata login), Natural Earth Admin-0 country boundaries (shapefile/GeoPackage, no login needed)
- in QGIS: clip the PVOUT raster to country borders, run population-weighted Zonal Stats (coefficient of variation of PVOUT) per country
- crunch the heterogeneity number for all ~190 countries, pick a cutoff so Canada/Russia/US land above it and small/flat countries like Belgium land below it
- end goal: locked list of which countries need the detailed treatment (Tier 1) vs just the country average (Tier 2), save as a CSV

## Week 2 (Nov 25 - Dec 1): grab Path 1 (deaths) data
- grab: OWID/Energy Institute coal consumption by country-year 1965-2024 (just a CSV, ourworldindata.org/grapher/coal-consumption-by-country-terawatt-hours-twh); McDuffie et al 2021 Nat Commun GBD-MAPS global supplementary data (coal-attributable PM2.5 deaths by country/region, 2017) - from the paper's supplementary stuff or the HEI GBD-MAPS report; WHO Ambient Air Quality Database / PM2.5 exposure by country-year
- sign up for: IHME GBD Results Tool account (ghdx.healthdata.org) - need this for air pollution deaths by country-year, 1990-2023
- just loading stuff and eyeballing it this week, no merging yet

## Week 3 (Dec 2 - Dec 8): grab Path 2 (solar/cost) data
- grab: World Bank/Global Solar Atlas country PVOUT rankings (kWh/kWp/year, energydata.info); IRENA Renewable Power Generation Costs data - solar capex ($/W) by region/year; Ember Yearly Electricity Data (or IEA) - country electricity prices for the LCOE stuff
- note which countries are missing electricity price data now so it's not a surprise later - probably need a regional average fallback
- also peek at the PVOUT raster in QGIS next to the Tier 1/2 list from week 1
- last normal week before exams eat everything - catch up here if weeks 1-2 slipped at all

## Week 4 (Dec 9 - Dec 15): dead week, exams starting
- nothing critical, exams take priority
- if there's downtime: skim the McDuffie paper's methods, skim IRENA's cost methodology

## Week 5 (Dec 16 - Dec 22): dead week, exams
- nothing planned, just get through exams

## Week 6 (Dec 23 - Dec 29): dead week, holiday
- totally optional, nothing that matters if skipped

## Week 7 (Dec 30 - Jan 5): dead week / easing back in
- check in with Koami/Pearce on where things stand
- double check the plan from week 8 on still makes sense, move stuff around if actual free time looks different

## Week 8 (Jan 6 - Jan 12): smash everything into one master table
- also due this week: project proposal, Fri Jan 8 - Brightspace + send to Pearce
- schema: `iso3, country, year, variable, value, source`
- line up the country codes across every dataset from weeks 2-3 (this is the "data exists but nobody put it together" part - good CS chapter material)
- check what's missing per dataset, decide case by case whether to drop it, fill it in, or just flag it
- quick sanity plots - top 20 coal countries, PM2.5 vs coal consumption - just to make sure nothing looks broken
- end goal: one clean `master_country_year.csv`

## Week 9 (Jan 13 - Jan 19): axis 1 calibration, part 1
- McDuffie numbers = ground truth for 2017, coal-attributable deaths per country
- build the rough proxy version for every year: WHO PM2.5 x IHME deaths x coal's share of the energy mix

## Week 10 (Jan 20 - Jan 26): axis 1 calibration, part 2
- figure out the gap between the 2017 proxy guess and the real McDuffie number, per country
- use that gap to correct the whole proxy time series
- sanity check: plot the corrected trends, make sure China/India etc look right

## Week 11 (Jan 27 - Feb 2): wrap up Path 1 + first map
- end goal: final coal-deaths-by-country-year table, trend included
- make the first heat map in QGIS (coal deaths by country)

## Week 12 (Feb 3 - Feb 9): Path 2, everyone at once (Tier 1 + Tier 2)
- Tier 2 (the easy countries): PV GW needed = energy to replace / country's average PVOUT
- Tier 1 (the tricky ones): use the population-weighted PVOUT breakdown from week 1, lean the PV toward where people actually live, add it up to a national number
- spot check - does the Tier 1 number actually move in the direction you'd expect compared to just using the simple average?
- end goal: PV GW needed for basically every country

## Week 13 (Feb 10 - Feb 16): money stuff
- total cost to build: IRENA $/W x GW needed
- 20-year cost: work out LCOE for solar (capex, some O&M guess, discount rate, capacity factor from PVOUT) vs what coal electricity actually costs (Ember/IEA, or a regional guess if missing)
- end goal: $ saved and $ per life saved, per country

## Week 14 (Feb 17 - Feb 23): put it all together
- final heat maps in QGIS (lives saved, % deaths avoided, PV needed, $ per life saved), summary tables in python (total lives saved, total PV, total cost), plus the "where should we prioritize" ranking
- nice to have, not required: if Koami's got time, run PySAM for just the US and compare to the original 2017 paper

## Week 15 (Feb 24 - Mar 2): the "ok I actually feel good about this" week
- also due this week: progress report, Wed Feb 24 - Brightspace + send to Pearce (this is basically "share preliminary results" below, just formalized)
- rerun the whole pipeline from scratch, raw files to final figures - make sure it's not held together with one lucky run
- squash whatever bugs show up
- show Pearce the full preliminary results, get a go/no-go before starting to write
- by the end of this: should feel done, with a month left to spare

## Week 16 (Mar 3 - Mar 9): writing, week 1
- intro/background, methods (the CS-flavored stuff - data pipeline, the heterogeneity cutoff thing, the calibration trick, pipeline engineering), data section

## Week 17 (Mar 10 - Mar 16): writing, week 2
- results (maps/tables), discussion (prioritization - lives vs cost), start the abstract

## Week 18 (Mar 17 - Mar 23): writing, week 3
- full draft done, send to Pearce, start folding in feedback, clean up figures

## Week 19 (Mar 24 - Mar 28, shortened to 5 days): buffer / fixing stuff, submit
- whatever feedback's left, formatting, proofreading, final figure tweaks
- aim to have the final PDF locked a day early, not right at the wire
- if there's spare time: build the interactive map thing as a bonus - first thing to drop if not
- **submit the thesis - Mon Mar 29**

## Week 20 (Mar 30 - Apr 5): artefact prep
- thesis is in, this week's just about the "project artefacts" deliverable - clean up the `code/` repo, export final datasets/figures, make sure everything's organized enough to hand off
- reach out to Pearce to actually book the presentation slot (don't leave this to the last few days)
- start pulling together presentation slides/material

## Week 21 (Apr 6 - Apr 9): send it off
- finish presentation prep
- **send all project artefacts to Pearce - Fri Apr 9**
- **presentation should be booked with Pearce by Apr 9** (ideally booked way earlier, see week 20 - this is just the hard deadline)
