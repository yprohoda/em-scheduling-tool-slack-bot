from db.db_access import dynamodb, create_table
from helper import time_date_now

table = dynamodb.Table('timeslots_confirmed')


def create_record_in_timeslots_confirmed(interviewer_id, timeslot_id, slack_id):
    """
    Creates record in timeslots table
    """
    datetime, timestamp = time_date_now()
    table.put_item(
        Item={
            'interviewer_id': int(interviewer_id),
            'timeslot_id': int(timeslot_id),
            'slack_id': slack_id,
            'datetime': str(datetime),
            'timestamp': str(timestamp),
        }
    )


def get_all_items():
    response = table.scan()
    return response['Items']


def get_all_available_interviews():
    return [(int(i['interviewer_id']), int(i['timeslot_id'])) for i in get_all_items()]


def get_avail_interv_by_interv_id(inter_ids: list):
    """
    Get confirmed timeslots ids for interviewers id
    :param inter_ids: list
    :return: [(interviewer id, confirmed timeslots id)]: list of tuples
    """
    list_of_confirmed_timeslots_ids = []
    for inter_id in inter_ids:
        list_of_confirmed_timeslots_ids += [(int(i['interviewer_id']), int(i['timeslot_id'])) for i in get_all_items() if i['interviewer_id'] == inter_id]
    return list_of_confirmed_timeslots_ids


def create_timeslots_confirmed_table():
    create_table(table_name='timeslots_confirmed',
                 column1='interviewer_id',
                 column2='timeslot_id',
                 type1='N',
                 type2='N')


if __name__ == '__main__':
    create_timeslots_confirmed_table()