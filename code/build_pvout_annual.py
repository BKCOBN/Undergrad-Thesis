# Global Solar Atlas = PVOUT as 12 monthly files (PVOUT_01 = jan ... PVOUT_12 = dec)
# This just averages them into one annual PVOUT grid.

# imports
from contextlib import ExitStack
from pathlib import Path
import numpy as np
import rasterio
from rasterio.windows import Window

# where the 12 monthly files live, where the output goes, how many rows to read at a time
INPUT_FOLDER = Path("datasets/raw/pvout/World_PVOUT_GISdata_LTAm_AvgDailyTotals_GlobalSolarAtlas-v2_GEOTIFF")
OUTPUT_FILE = Path("datasets/processed/pvout_annual_avg_daily.tif")
BLOCK_SIZE = 1000

# grab all 12 monthly tifs, make sure none are missing
monthly_files = sorted(INPUT_FOLDER.glob("PVOUT_*.tif"))

# open all 12, copy profile from one of them for the output file
with ExitStack() as stack:
    datasets = [stack.enter_context(rasterio.open(fp)) for fp in monthly_files]
    meta = datasets[0].profile.copy()
    meta.update(dtype="float32", count=1, compress="lzw", nodata=np.nan)

    rows_total, cols_total = datasets[0].height, datasets[0].width

    # by row-chunk avg 12 months together, write it out
    with rasterio.open(OUTPUT_FILE, "w", **meta) as out_ds:
        for y_off in range(0, rows_total, BLOCK_SIZE):
            win_height = min(BLOCK_SIZE, rows_total - y_off)
            win = Window(0, y_off, cols_total, win_height)

            cube = np.stack([ds.read(1, window=win, masked=True).filled(np.nan) for ds in datasets])
            mean_grid = np.nanmean(cube, axis=0).astype(np.float32)

            out_ds.write(mean_grid, 1, window=win)

print(f"done, wrote {OUTPUT_FILE}")