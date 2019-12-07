#!/usr/bin/env python
"""
Extract ESA CCI-SST data for a given area

Author: Dan Clewley (dac)
Creation Date: 2019-04-11

"""

from __future__ import print_function
import argparse
import datetime
import glob
import os
import sys

from nk_toolkit import libsubarea

CCI_PATH = "/data/datasets/sst/esa-cci-sst/v2.1/global/1d/"

NETCDF_SEARCH_PATTERN = "nc/*ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0*.nc"

def loop_through_dates(in_dir,
                       out_dir,
                       start_date,
                       end_date,
                       extent,
                       area_code="global-extacted"):
    """
    Look through all dates in range and convert to a NetCDF

    """

    start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    current_date = start_date_obj

    while current_date < end_date_obj:

        file_path = os.path.join(in_dir, "{:02}".format(current_date.year),
                                 "{:02}".format(current_date.month),
                                 "{:02}".format(current_date.day),
                                 NETCDF_SEARCH_PATTERN)

        try:
            in_netcdf = glob.glob(file_path)[0]
        except IndexError:
            print("Couldn't find file for date: {}".format(current_date),
                  file=sys.stderr)
            print(file_path)
            current_date = current_date + datetime.timedelta(days=1)
            continue

        print("Extracting {}".format(in_netcdf))
        out_netcdf_dir = os.path.join(out_dir,
                                      "{:02}".format(current_date.year))
        try:
            os.makedirs(out_netcdf_dir)
        except OSError:
            # If already exists continue
            pass

        # Rename to NEODAAS standard name
        output_name = "SST-CCI_sst_L4_{area}_1d_{date}.nc".format(
                                     area=area_code,
                                     date=os.path.basename(in_netcdf)[0:8])

        out_netcdf_file = os.path.join(out_netcdf_dir, output_name)

        libsubarea.nk_subarea(in_netcdf, out_netcdf_file,
                              ["lon", "lat"], [extent[0], extent[3]],
                              [extent[2], extent[1]])

        current_date = current_date + datetime.timedelta(days=1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract SST-CCI data",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-o", "--outputdir",
                        type=str, help="Input directory", required=True)
    parser.add_argument("-i", "--inputdir",
                        type=str, help="Input directory",
                        default=CCI_PATH)
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
    parser.add_argument("--area_code",
                        help ="Area code to use in file name",
                        type=str,
                        required=False,
                        default="global-extracted")
    args = parser.parse_args()

    loop_through_dates(args.inputdir,
                       args.outputdir,
                       args.startdate, args.enddate,
                       args.extent,
                       area_code=args.area_code)
