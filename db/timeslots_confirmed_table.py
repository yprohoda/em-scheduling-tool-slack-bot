from pprint import pprint

from db.db_access import dynamodb
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


# def get_confirmed_inter_id_by_inter_id(inter_ids: list):
#     list_of_confirmed_timeslots_ids = []
#     for inter_id in inter_ids:
#         list_of_confirmed_timeslots_ids += [(int(i['interviewer_id']), int(i['timeslot_id'])) for i in get_all_items() if
#                                             i['interviewer_id'] == inter_id]
#     return list_of_confirmed_timeslots_ids

def get_avail_intervs_by_interviewer_id(inter_ids: list):
    """
    Get confirmed timeslots ids for interviewers id
    :param inter_ids: list
    :return: [(interviewer id, confirmed timeslots id)]: list of tuples
    """
    list_of_confirmed_timeslots_ids = []
    for inter_id in inter_ids:
        list_of_confirmed_timeslots_ids += [(int(i['interviewer_id']), int(i['timeslot_id'])) for i in get_all_items() if i['interviewer_id'] == inter_id]
    return list_of_confirmed_timeslots_ids


if __name__ == '__main__':
    # create_record_in_timeslots_confirmed(1, 1)
    # pprint(get_all_available_interviews())
    # print(get_confirmed_timeslots_ids_by_interviewer_id(2))
    print(get_avail_intervs_by_interviewer_id([1,2,3]))
    # print(get_confirmed_inter_id_by_inter_id([1,2,3]))