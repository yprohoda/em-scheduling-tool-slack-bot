"""Server app, should be run from Terminal along with ngrok server all the time"""

import os
from pprint import pprint

from slack_bolt import App
from decouple import config

from data import home_tab_blocks, available_interviewers_blocks
from db.interviewer_table import get_id_by_slackid, get_inter_id_by_descipline, get_info_by_interv_id
from db.timeslots_confirmed_table import create_record_in_timeslots_confirmed, get_avail_intervs_by_interviewer_id
from db.timeslots_table import prepare_timeslot_data_for_slack, get_real_timeslot_by_timeslot_id

app = App(
    token=config("SLACK_BOT_TOKEN"),
    signing_secret=config("SLACK_SIGNING_SECRET")
)


# Handle a view_submission event
@app.view("view_1")
def handle_submission(ack, body, client, view):
    """Handel clicking Submit on the Scheduler modal window"""
    # pprint(view)
    sel_options = view['state']['values'][list(view['state']['values'].keys())[0]]['checkboxes-action'][
        'selected_options']
    pprint(sel_options)

    slack_id = body["user"]["id"]
    print('user_id', slack_id)

    timeslots_ids = [i['value'] for i in sel_options]
    print('sel_ids', timeslots_ids)

    # Validate the inputs
    errors = {}
    if len(timeslots_ids) < 2:
        errors[list(view['state']['values'].keys())[0]] = "At least 2 checkboxes should be selected."

    if len(errors) > 0:
        ack(response_action="errors", errors=errors)
        return

    # Acknowledge the view_submission event and close the modal
    ack()

    # Saving data to a DB
    interviewer_id = get_id_by_slackid(slack_id)
    for timeslot_id in timeslots_ids:
        create_record_in_timeslots_confirmed(interviewer_id=interviewer_id,
                                             timeslot_id=timeslot_id,
                                             slack_id=slack_id)
                                             #slackname=slack_name)

    # then sending the user a verification of their submission
    # Message to send user
    msg = ""
    try:
        pass
        # Save to DB
        msg = f"Your submission was successful."
    except Exception as e:
        # Handle error
        msg = "There was an error with your submission."
    finally:
        # Message the user
        client.chat_postMessage(channel=slack_id, text=msg)


@app.view("view_2")
def handle_submission(ack, body, client, view):
    """Handel clicking Submit on the Check modal window"""
    pprint(view)

    sel_discipline = view['state']['values'][list(view['state']['values'].keys())[0]]['static_select-action'][
        'selected_option']['text']['text']
    pprint(sel_discipline)

    sel_technology = view['state']['values'][list(view['state']['values'].keys())[1]]['static_select-action'][
        'selected_option']['text']['text']
    pprint(sel_technology)

    slack_id = body["user"]["id"]
    print('user_id', slack_id)

    info = filter_db(sel_discipline, sel_technology)

    # Validate the inputs
    errors = {}
    if len(info) < 1:
        errors[list(view['state']['values'].keys())[0]] = "No interviewers are available. Select other options."

    if len(errors) > 0:
        ack(response_action="errors", errors=errors)
        return

    # Acknowledge the view_submission event and close the modal
    ack()

    msg = ""
    try:
        pass
        msg = info
    except Exception as e:
        # Handle error
        msg = "There was an error with your submission."
    finally:
        # Message the user
        client.chat_postMessage(channel=slack_id, text=msg)


def filter_db(sel_discipline, sel_technology):
    """
    Filter DB to get correct slackname, fullname, date

    :param sel_discipline: str
    :param sel_technology: str
    :return: pretty_string_info: str

    Example:
        @foo1, Foo Bar, 2021-05-24 11-00-12-00
        @evgpro, Evg Pro, 2021-05-24 12-00-13-00
        @evgpro, Evg Pro, 2021-05-24 11-00-12-00
    """
    list_of_inter_ids = get_inter_id_by_descipline(discipline=sel_discipline, technology_stack=sel_technology)
    list_of_inter_ids_and_confirmed_timeslots_ids = get_avail_intervs_by_interviewer_id(inter_ids=list_of_inter_ids)
    final_info = []

    for i in list_of_inter_ids_and_confirmed_timeslots_ids:
        interv_info = get_info_by_interv_id(i[0])
        timeslot_info = get_real_timeslot_by_timeslot_id(i[1])
        info = interv_info + (timeslot_info,)
        final_info.append(info)

    pretty_string_info = ''
    for i in final_info:
        pretty_string_info += str(i).strip('()') + '\n'

    return pretty_string_info.replace("'", "")


@app.event("app_home_opened")
def app_home_opened(event, client, logger):
    user_id = event["user"]

    # Call the views.publish method using the WebClient passed to listeners
    result = client.views_publish(
        user_id=user_id,
        view={
            # Home tabs must be enabled in your app configuration page under "App Home"
            # and your app must be subscribed to the app_home_opened event
            "type": "home",
            "blocks": home_tab_blocks
        },
    )
    logger.info(result)


@app.action("Start-scheduling-bot")
def open_modal(ack, body, client):
    """Opens modal with checkboxes when user clicks Start scheduling button"""
    # Acknowledge the command request
    ack()
    # Call views_open with the built-in client
    response = client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text": "My App"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": prepare_timeslot_data_for_slack()
        }
    )


@app.action("Check-available-interviewers-btn")
def open_modal(ack, body, client):
    """Opens modal with checkboxes when user clicks Start scheduling button"""
    # Acknowledge the command request
    ack()
    # Call views_open with the built-in client
    response = client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": "view_2",
            "title": {"type": "plain_text", "text": "My App"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": available_interviewers_blocks
        }
    )


# Start your app
if __name__ == "__main__":
    """Running Server app, should be done from Terminal"""
    app.start(port=int(os.environ.get("PORT", 3000)))
