# Fleet Trip Review

Static Barbados fleet dashboard. The site reads `ServiceTruckCSV.csv` from the
same directory whenever it opens or the **Refresh ServiceTruckCSV.csv** button
is pressed. The CSV is not embedded in the HTML.

## Publish with GitHub Pages

1. Create a public GitHub repository and upload the site files, including
   `index.html`, `fleet-dashboard.html`, and `ServiceTruckCSV.csv`.
2. In the repository, open **Settings > Pages**. Set **Source** to **Deploy from
   a branch**, choose the default branch and **/(root)**, then save.
3. Open the Pages URL shown in Settings after the deployment finishes.

The dashboard and CSV will be public to anyone with their URLs. Do not add data
that should be limited to management or the company.

## Replace the CSV

Keep the filename exactly `ServiceTruckCSV.csv` and preserve the same column
headers. Replace the file in the repository and commit the change. GitHub Pages
will publish the new version. Reload the site, or press **Refresh
ServiceTruckCSV.csv** if it is already open. Use **Choose CSV** to inspect a
local file without publishing it.

The map connects the CSV's start and stop locations; it does not reproduce the
roads actually driven. Roads are geographic context only.

## Rebuild the dashboard

Only changes to layout, styling, map logic, or road data require a rebuild:

```sh
python build_dashboard.py
```

Commit the regenerated `fleet-dashboard.html`. The builder uses
`roads_4326.geojson` for the road layer and the SVG logo in this directory.
