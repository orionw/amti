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
    help="Path to file of AssignmentIDs to check.")
@click.option(
     '--hit_id',
    type=str,
    help="The HITId to check for bonuses sent.")
@click.option(
     '--assignment_id', '-a',
    type=str,
    help="The AssignmentId to check for bonuses sent.")
@click.option(
    '--live', '-l',
    is_flag=True,
    help='View the status of HITs from the live MTurk site.')
def list_bonuses(file, hit_id, assignment_id, live):
    """Check bonuses sent

    Check for bonuses sent to either a HITId or an AssignmentId
    """
    env = 'live' if live else 'sandbox'

    client = utils.mturk.get_mturk_client(env)

    if not hit_id and not assignment_id and not file:
        raise Exception("Have to give either a HITId, an AssignmentId, or a file")
    
    if file:
        data = utils.workers.read_data_from_csv(file)
        input_dicts = [{"AssignmentId": item["AssignmentId"]} for item in data]
    else:
        input_dict = {}
        if assignment_id:
            input_dict["AssignmentId"] = assignment_id
        if hit_id:
            input_dict["HITId"] = hit_id
        input_dicts = input_dict

    output_str = \
        f'\n' \
            f'  Bonuses :' \
        f'\n  =============' 
    for item_to_check in input_dicts:
        response = client.list_bonus_payments(**item_to_check)
        for item in response["BonusPayments"]:
            output_str += f"\n    WorkerId: {item['WorkerId']}, Amount: {item['BonusAmount']}, Time Sent: {item['GrantTime']}"
            # output_str += "\n"

    click.echo(output_str + '\n')
