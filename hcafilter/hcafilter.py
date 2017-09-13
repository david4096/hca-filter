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
import json

import pandas
import boto3


def filter_buckets(from_bucket, to_bucket):
    """
    Gathers the manifest from the to_bucket and samples in the from_bucket
    and writes the resulting filtered data to the to_bucket with a filename
    matching the from_bucket.

    :param from_bucket:
    :param to_bucket:
    :return:    Returns the TSV that passed the filter.
    """
    # Download to_bucket manifest, this file has been created via a request
    # to a microservice.
    s3 = boto3.client('s3')
    # Download the file in the from_bucket.
    print(
        s3.download_file(
            Bucket=from_bucket,
            Key=from_bucket,
            Filename=from_bucket))
    # Download the manifest
    manifest_filename = 'manifest.json'
    s3.download_file(
        Key=manifest_filename,
        Bucket=to_bucket,
        Filename=manifest_filename)
    with open('manifest.json', 'r') as json_file:
        manifest = json.load(json_file)
    sample_ids = manifest[from_bucket]
    # Read the file and reject values not in manifest.
    filename = from_bucket + '-filtered'
    print(sample_ids)
    pandas.read_csv(
        from_bucket, index_col=0, sep='\t').filter(
            sample_ids, axis='index').to_csv(filename, sep='\t')
    # Write results to to_bucket
    # Each file is a tsv with the filename matching the bucket it filtered
    # from. This allows workers to easily check to see if the work has been
    # done by checking for the presence of the file in the to_bucket.
    print(s3.upload_file(Filename=filename, Bucket=to_bucket, Key=from_bucket))

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
    filter_buckets(parsed.from_bucket_id, parsed.to_bucket_id)
    shutil.rmtree(temp_path)
