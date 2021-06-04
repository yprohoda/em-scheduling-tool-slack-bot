from pprint import pprint

from db.db_access import dynamodb

table = dynamodb.Table('interviewers')


def get_all_interviewers():
    response = table.scan()
    return response['Items']


def get_all_slack_ids():
    return [i['slack_id'] for i in get_all_interviewers()]


def get_id_by_slackid(slack_id):
    return int([i['id'] for i in get_all_interviewers() if i['slack_id'] == slack_id][0])


def get_all_disciplines():
    return [i['discipline'] for i in get_all_interviewers()]


def get_discipline_by_interviewer_id(id_):
    return [i['discipline'] for i in get_all_interviewers() if i['id'] == id_]


def get_inter_id_by_descipline(discipline, technology_stack):
    return [int(i['id']) for i in get_all_interviewers() if
            discipline in i['discipline'] and
            technology_stack in i['technology_stack']]


def get_info_by_interv_id(interv_id):
    return [(i['slack_name'], i['full_name']) for i in get_all_interviewers() if i['id'] == interv_id][0]


if __name__ == '__main__':
    # pprint(get_all_interviewers())
    # pprint(get_discipline_by_interviewer_id(1))
    # print(get_inter_id_by_descipline('Dev', 'Python'))
    print(get_info_by_interv_id(1))