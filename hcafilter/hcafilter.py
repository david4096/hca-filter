"""

hcafilter: Combines gene cell matrices and filters out unwanted samples.

Usage:

`hca-filter from-bucket-id to-bucket-id`

To to-bucket contains a `manifest.json` that includes which samples in the
`from-bucket` should pass the filter. The `manifest.json` should be generated
by a microservice.

"""

import argparse
import tempfile
import shutil


def filter_buckets(from_bucket, to_bucket):
    """
    Gathers the manifest from the to_bucket and samples in the from_bucket
    and writes the resulting filtered data to the to_bucket with a filename
    matching the from_bucket.

    :param from_bucket:
    :param to_bucket:
    :return:
    """
    # Download to_bucket manifest

    # Download from_bucket

    # Reject values not in manifest

    # Write results to to_bucket

    return


def main(args=None):
    """
    The console script that coordinates filtering samples and adding them
    to the to-bucket.

    :param args:
    :return:
    """
    parser = argparse.ArgumentParser(
        description='Filter samples for an HCA study from a bundle.')
    parser.add_argument("from_bucket_id", type=str,
                        help="The ID of the dataset we wish to filter.")
    parser.add_argument("to_bucket_id", type=str,
                        help="The bucket that we are filtering into.")
    parser.add_argument("-l", action="store_true",
                        help="Simply lists the samples in the from bucket"
                             "that will be included.")

    parsed = parser.parse_args(args)
    print(parsed)

    temp_path = tempfile.mkdtemp()

    shutil.rmtree(temp_path)
