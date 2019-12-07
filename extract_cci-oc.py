#!/usr/bin/env python
"""
Extract ESA CCI-OC data for a given area

Author: Dan Clewley (dac)
Creation Date: 2019-06

"""

from __future__ import print_function
import argparse
import datetime
from dateutil import relativedelta
import glob
import os
import sys

from nk_toolkit import libsubarea

CCI_PATH = "/data/datasets/Projects/CCI/v4.0-release/geographic/netcdf"

TEMPORAL_COMPOSITE_NAMES = {
    "daily" : "1d",
    "5day" : "5d",
    "8day" : "8d",
    "monthly" : "1m"
}

def loop_through_dates(in_dir,
                       out_dir,
                       start_date,
                       end_date,
                       extent,
                       temporal_composite="monthly",
                       product="all_products",
                       area="global-extracted",
                       neodaas_name=False):
    """
    Look through all dates in range and convert to a NetCDF

    """

    start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    current_date = start_date_obj

    while current_date < end_date_obj:

        if temporal_composite.lower() == "monthly":
            str_date = current_date.strftime("%Y%m")
        else:
            str_date = current_date.strftime("%Y%m%d")

        file_path = os.path.join(in_dir, temporal_composite, product,
                                 "{:02}".format(current_date.year),
                                 "*{}*nc".format(str_date))
        in_netcdfs = glob.glob(file_path)

        for in_netcdf in in_netcdfs:

            print("Extracting {}".format(in_netcdf))
            out_netcdf_dir = os.path.join(out_dir,
                                          "{:02}".format(current_date.year))
            try:
                os.makedirs(out_netcdf_dir)
            except OSError:
                # If already exists continue
                pass

            if neodaas_name:
                output_name = "OC-CCI_{product}_L4_{area}_{period}_{date}.nc".format(
                                     product=product,
                                     area=area,
                                     period=TEMPORAL_COMPOSITE_NAMES[temporal_composite],
                                     date=str_date)
            else:
                output_name = os.path.basename(in_netcdf).replace(".nc",
                                                                  "_{}.nc".format(area))
            out_netcdf_file = os.path.join(out_netcdf_dir, output_name)

            if os.path.isfile(out_netcdf_file):
                continue

            libsubarea.nk_subarea(in_netcdf, out_netcdf_file,
                                  ["lon", "lat"], [extent[0], extent[3]],
                                  [extent[2], extent[1]])

        if temporal_composite.lower() == "monthly":
            current_date = current_date + relativedelta.relativedelta(months=1)
        # For the daily, 5day and 8day composite itterate a day at a time so get all composites
        # If not then when starting out of sequence keep missing data.
        else:
            current_date = current_date + relativedelta.relativedelta(days=1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subset OC-CCI netCDF files "
                                                 "to a given area",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--inputdir",
                        type=str, required=False,
                        default=CCI_PATH,
                        help="Input directory containing CCI netCDF files")
    parser.add_argument("-o", "--outputdir",
                        type=str, help="Input directory")
    parser.add_argument("--startdate",
                        help ="Start date in format YYYY-MM-DD",
                        type=str,
                        required=True)
    parser.add_argument("--enddate",
                        help ="End date in format YYYY-MM-DD",
                        type=str,
                        required=True)
    parser.add_argument("--extent",
                        help="Extent of output netCDF (ulx uly lrx lry)",
                        type=str,
                        nargs=4,
                        default=None)
    parser.add_argument("--area",
                        help ="Short name to use for area on extacted file",
                        type=str,
                        required=False,
                        default="global-extracted")
    parser.add_argument("--composite",
                        help ="Length of composite to consider",
                        type=str,
                        choices=("daily", "5day", "8day", "monthly"),
                        required=False,
                        default="monthly")
    parser.add_argument("--product",
                        help ="Product to extract",
                        type=str,
                        choices=("all_products", "chlor_a", "iop", "kd", "rrs"),
                        required=False,
                        default="monthly")
    parser.add_argument("--neodaas_name",
                        help ="Rename according to NEODAAS convention",
                        action="store_true",
                        required=False,
                        default=False)
    args = parser.parse_args()

    loop_through_dates(args.inputdir,
                       args.outputdir,
                       args.startdate, args.enddate,
                       args.extent, temporal_composite=args.composite,
                       product=args.product, area=args.area,
                       neodaas_name=args.neodaas_name)
