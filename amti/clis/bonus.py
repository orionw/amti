"""Command line interfaces for bonus-ing Workers"""

import logging

import click
import csv
import json

from amti import actions
from amti import settings
from amti import utils


logger = logging.getLogger(__name__)


@click.command(
    context_settings={
        'help_option_names': ['--help', '-h']
    })
@click.option(
     '--file', '-f',
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Path to file of WorkerIds to block.")
@click.option(
    '--live', '-l',
    is_flag=True,
    help='View the status of HITs from the live MTurk site.')
def bonus_workers(file, live):
    """Send notification message to workers.

    Given a space seperated list of WorkerIds (IDS), or a path to
    a CSV of WorkerIds, send a notification to each worker. 
    """
    env = 'live' if live else 'sandbox'

    client = utils.mturk.get_mturk_client(env)

    data = utils.workers.read_data_from_csv(file)
    bonus_sum = sum([float(item["BonusAmount"]) for item in data])
    num_workers = len(set([item["WorkerId"] for item in data]))

    cost_approved = click.confirm(f'Approve cost (~{bonus_sum:.2f} USD) for {num_workers} unique WorkerIds and {len(data)} bonuses. Proceed?')
    if not cost_approved:
        logger.info(' The bonus cost was not approved. Aborting bonus send.')
        return
    
    for worker_dict in data:
        logger.info(f"Sending bonus to workers: {worker_dict['WorkerId']}")

        response = client.send_bonus(
            AssignmentId=worker_dict['AssignmentId'],
            BonusAmount=worker_dict['BonusAmount'],
            WorkerId=worker_dict['WorkerId'],
            Reason=worker_dict['Reason'],
        )

    logger.info('Finished sending bonuses.')