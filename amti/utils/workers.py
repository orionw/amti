""" Module for worker management functions """
import boto3
import click
import csv
from typing import List

def chunk_list(items: List, n: int = 100) -> List:
    """Create generatator that yields n sized chunks of input list."""
    for i in range(0, len(items), n):
        yield items[i:i + n]

def read_workerids_from_file(file: click.Path) -> List:
    """Read WorkerIds from file.
    
    Read WorkerIds from CSV file. Return list of extracted WorkerIds.

    Parameters
    ----------
    file : click.Path
        Path to CSV file of WorkerIds.

    Returns
    -------
    list
        List of extracted WorkerId strings.
        
    """
    worker_ids = []
    with open(file, 'r') as f:
        reader = csv.reader(f)

        # check if first row is header
        first_row = next(reader)
        if 'WorkerId' not in first_row:
            worker_ids += first_row

        for row in reader:
            worker_ids += row

    return worker_ids


def read_data_from_csv(file: click.Path, headers: List = None) -> List:
    """Read WorkerIds from file.
    
    Read data from CSV file. Return list of values.

    Parameters
    ----------
    file : click.Path
        Path to CSV file

    Returns
    -------
    list
        List of extracted WorkerId strings.
        
    """
    data = []
    with open(file, 'r') as f:
        reader = csv.reader(f)

        # check if first row is header
        first_row = next(reader)
        if 'WorkerId' not in first_row:
            if headers is None:
                raise Exception("Cannot read a file with no headers")
            data += first_row
        else:
            headers = first_row

        for row in reader:
            data.append({col_name: value for (col_name, value) in zip(headers, row)})

    return data