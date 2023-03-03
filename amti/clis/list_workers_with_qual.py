"""Command line interface for disassociating quals with Workers"""

import logging

import click
import csv

from amti import actions
from amti import settings
from amti import utils


logger = logging.getLogger(__name__)


@click.command(
    context_settings={
        'help_option_names': ['--help', '-h']
    })
@click.option(
    '--qual', '-q', 
    help='QualificationId (or name, if --name flag passed).')
@click.option(
    '--name', '-n',
    is_flag=True,
    help='Search for qual by name instead of id.')
@click.option(
    '--live', '-l',
    is_flag=True,
    help='View the status of HITs from the live MTurk site.')
def list_workers_with_qual(qual, name, live):
    """List workers with a specific qualification.

    Given a qualification (QUAL), list workers who have it

    NOTE: Only works with quals that both exist and are owned by the user.
    """
    env = 'live' if live else 'sandbox'

    client = utils.mturk.get_mturk_client(env)


    # set qual_id
    qual_id = qual
    if name:
        qual_id = utils.mturk.get_qual_by_name(client, qual)
        if qual_id is None:
            raise ValueError(f"No qual with name {qual} found.")

    args = {"QualificationTypeId": qual_id}

    # associate qual with workers
    logger.info(f'Listing workers with qualification {qual_id}.')
    response = client.list_workers_with_qualification_type(
        **args
    )
    for idx in range(response["NumResults"]):
        logger.info(f"\tWorkerId: {response['Qualifications'][idx]['WorkerId']}, Status: {response['Qualifications'][idx]['Status']}, Value: {response['Qualifications'][idx]['IntegerValue']}")

    logger.info('Finished listing quals.')