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

Keep the filename exactly `ServiceTruckCSV.csv` and preserve the same column
headers. Replace the file in the repository and commit the change. The GitHub
Action will rebuild and publish the site. Reload the site after the deployment
finishes to see the new data.

The frontend does not upload or save CSV files. To update the GitHub Pages site,
commit the new `ServiceTruckCSV.csv` to `main` or run the workflow after
updating the file in GitHub.

The map connects the CSV's start and stop locations; it does not reproduce the
roads actually driven. Roads are geographic context only.

## Rebuild the dashboard

Only changes to layout, styling, map logic, or road data require a rebuild:

```sh
python build_dashboard.py
```

Commit the regenerated `fleet-dashboard.html`. The builder uses
`roads_4326.geojson` for the road layer and the SVG logo in this directory.
