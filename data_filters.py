from db.interviewers_table import get_info_by_interv_id, get_inter_id_by_descipline
from db.timeslots_confirmed_table import get_avail_interv_by_interv_id
from db.timeslots_table import get_real_timeslot_by_timeslot_id, get_timeslots_ids_by_date


def convert_int_ids_and_ts_ids_into_friendly_data(int_ids_and_corres_ts_ids):
    """
    Get final info converting int ids to pretty contact info, ts ids to date and time:
    :param: list of tuples [(interviwer_id, timeslot_id)]
    :return: str info. Example: @evgpro, Evg Pro, 2021-05-01 12-00-13-00
    """
    final_info = []
    for i in int_ids_and_corres_ts_ids:
        interv_info = get_info_by_interv_id(i[0])
        timeslot_info = get_real_timeslot_by_timeslot_id(i[1])
        info = interv_info + (timeslot_info,)
        final_info.append(info)

    pretty_string_info = ''
    for i in final_info:
        pretty_string_info += str(i).strip('()') + '\n'

    return pretty_string_info.replace("'", "")


def filter_db(discipline, technology, date):
    """
    Filter DB to get correct slackname, fullname, date

    :param discipline: str
    :param technology: str
    :return: pretty_string_info: str

    Example:
        @foo1, Foo Bar, 2021-05-24 11-00-12-00
        @evgpro, Evg Pro, 2021-05-24 12-00-13-00
        @evgpro, Evg Pro, 2021-05-24 11-00-12-00
    """

    # Select all interviewers ids filtered by disciplines and technologies
    int_ids = get_inter_id_by_descipline(discipline=discipline, technology_stack=technology)

    # Select interviewers ids and timeslots ids from confirmed timeslots
    int_ids_and_confirmed_ts_ids = get_avail_interv_by_interv_id(inter_ids=int_ids)

    # Select interviewers ids that match specific date
    corresp_ts_ids = get_timeslots_ids_by_date(date=date)

    # Select interviewers ids and timeslots id that match specific date and confirmed date
    int_ids_and_corres_ts_ids = [i for i in int_ids_and_confirmed_ts_ids if i[1] in corresp_ts_ids]

    return convert_int_ids_and_ts_ids_into_friendly_data(int_ids_and_corres_ts_ids)