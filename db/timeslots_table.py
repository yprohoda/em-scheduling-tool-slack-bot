from db.db_access import dynamodb
from helper import time_date_now
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key


def create_record_timeslots(id, date, time_from, time_to):
    """
    Creates record in timeslots table
    """
    _, timestamp = time_date_now()

    table = dynamodb.Table('timeslots')
    table.put_item(
        Item={
            'id': id,
            'date': date,
            'time_from': time_from,
            'time_to': time_to,

        }
    )

def get_items_from_table_by_id(id):
    table = dynamodb.Table('timeslots')
    try:
        response = table.query(
            KeyConditionExpression=Key('id').eq(id)
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Items']


def get_all_items():
    table = dynamodb.Table('timeslots')
    response = table.scan()
    return response['Items']


def get_all_timeslots():
    """
    Get all timeslots from table
    :return: list of date + time
    """
    timeslots = get_all_items()
    return [{'id': str(i['id']), 'date': i['date'] + ' ' + i['time_from'] + ' - ' + i['time_to']} for i in timeslots]


def prepare_timeslot_data_for_slack():
    from data import checkboxes_with_timeslots
    return checkboxes_with_timeslots(get_all_timeslots())


def get_real_timeslot_by_timeslot_id(timeslot_id):
    return [i['date'] + ' ' + i['time_from'] + '-' + i['time_to'] for i in get_all_items() if i['id'] == timeslot_id][0]


def get_real_timeslots_by_timeslots_id(timeslots_ids: list):
    """
    Get real timeslots for timeslots id list
    :param timeslots_ids: list
    :return: real timeslots: list
    """
    real_ts_list = []
    for id_ in timeslots_ids:
        real_ts_list += [i['date'] + ' ' + i['time_from'] + '-' + i['time_to'] for i in get_all_items() if i['id'] == id_]
    return real_ts_list


if __name__ == '__main__':
    # pprint(get_all_timeslots())
    # for i in range (5, 11):
    #     create_record_timeslots(i, '2021-05-24', '11-00', '12-00')
    # timeslots = get_items_from_table_by_id(2)
    # if timeslots:
    #     pprint(timeslots, sort_dicts=False)
    # pprint(get_all_timeslots())
    # pprint(prepare_timeslot_data_for_slack())
    # print(get_real_timeslots_by_timeslots_id([1,5,6]))
    print(get_real_timeslot_by_timeslot_id(1))