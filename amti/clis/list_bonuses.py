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
def list_bonuses(hit_id, assignment_id, live):
    """Check bonuses sent

    Check for bonuses sent to either a HITId or an AssignmentId
    """
    env = 'live' if live else 'sandbox'

    client = utils.mturk.get_mturk_client(env)

    if not hit_id and not assignment_id:
        raise Exception("Have to give either a HITId or an AssignmentId")
    
    input_dict = {}
    if assignment_id:
        input_dict["AssignmentId"] = assignment_id
    if hit_id:
        input_dict["HITId"] = hit_id

    response = client.list_bonus_payments(**input_dict)
    output_str = \
      f'\n' \
        f'  Batch Status:' \
      f'\n  =============' 
    
    for item in response["BonusPayments"]:
       output_str += f"\n    WorkerId: {item['WorkerId']}, Amount: {item['BonusAmount']}, Time Sent: {item['GrantTime']}"
    
    click.echo(output_str + '\n')
