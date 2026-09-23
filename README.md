# Fleet Trip Review

Static Barbados fleet dashboard. The site reads `ServiceTruckCSV.csv` from the
same directory whenever it opens. The CSV is not embedded in the HTML.

## Publish with GitHub Pages

1. Create a public GitHub repository and upload the site files, including
   `index.html`, `fleet-dashboard.html`, `ServiceTruckCSV.csv`, and the
   `.github/workflows/refresh-dashboard.yml` workflow.
2. In the repository, open **Settings > Pages**. Set **Source** to **GitHub
   Actions**, then save.
3. Push to `main` or open **Actions > Refresh dashboard site > Run workflow**.
   The action runs `python build_dashboard.py` and deploys the refreshed site.
4. Open the Pages URL shown in Settings after the deployment finishes.

The dashboard and CSV will be public to anyone with their URLs. Do not add data
that should be limited to management or the company.

## Replace the CSV

Keep the filename exactly `ServiceTruckCSV.csv`. The builder accepts both the
original short headers (such as `Device`, `Start Date`, and `Distance`) and the
current export headers (such as `DeviceName`, `TripDetailStartDateTime`, and
`TripDetailDistance`). It also accepts both `TripDetailDrivingDuraion` from the
current file and the correctly spelled `TripDetailDrivingDuration`.

Replace the file in the repository and commit the change. The GitHub Action
will rebuild and publish the site. Reload the site after the deployment finishes
to see the new data. Business names and destination coordinates are used when
the export provides them.

The frontend does not upload or save CSV files. To update the GitHub Pages site,
commit the new `ServiceTruckCSV.csv` to `main` or run the workflow after
updating the file in GitHub.

The map connects the CSV's start and stop locations; it does not reproduce the
roads actually driven. Roads are geographic context only.

## Time calculations

- Current-export driving time is calculated from each trip's start and stop
  timestamps because its `H:MM` duration values are rounded down to minutes.
- Stops between trips are calculated from the previous stop timestamp to the
  next start timestamp for the same vehicle.
- A stop that continues into the next calendar day is classified as an
  overnight gap and excluded from the dashboard's day-stop hours.
- Idling uses the source duration because the export does not provide separate
  idling start and stop timestamps.

## Rebuild the dashboard

Only changes to layout, styling, map logic, or road data require a rebuild:

```sh
python build_dashboard.py
```

Commit the regenerated `fleet-dashboard.html`. The builder uses
`roads_4326.geojson` for the road layer and the SVG logo in this directory.
