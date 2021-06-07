"""Server app, should be run from Terminal along with ngrok server all the time"""

import os
from pprint import pprint

from slack_bolt import App
from decouple import config

from data_forms import home_tab_blocks, available_interviewers_blocks
from data_filters import filter_db
from db.interviewers_table import get_id_by_slackid
from db.timeslots_confirmed_table import create_record_in_timeslots_confirmed
from db.timeslots_table import prepare_timeslot_data_for_slack

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
    slack_id = body["user"]["id"]
    timeslots_ids = [i['value'] for i in sel_options]

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

    # Get selected options from slack response
    sel_discipline = view['state']['values'][list(view['state']['values'].keys())[0]]['static_select-action'][
        'selected_option']['text']['text']
    sel_technology = view['state']['values'][list(view['state']['values'].keys())[1]]['static_select-action'][
        'selected_option']['text']['text']
    sel_date = view['state']['values'][list(view['state']['values'].keys())[2]]['datepicker-action'][
        'selected_date']
    slack_id = body["user"]["id"]

    print('Selected info:', slack_id, sel_discipline, sel_technology, sel_date)

    filtered_info = filter_db(sel_discipline, sel_technology, sel_date)

    # Validate the inputs
    errors = {}
    if len(filtered_info) < 1:
        errors[list(view['state']['values'].keys())[0]] = "No interviewers are available. Select other options."

    if len(errors) > 0:
        ack(response_action="errors", errors=errors)
        return

    # Acknowledge the view_submission event and close the modal
    ack()

    msg = ""
    try:
        pass
        msg = filtered_info
    except Exception as e:
        # Handle error
        msg = "There was an error with your submission."
    finally:
        # Message the user
        client.chat_postMessage(channel=slack_id, text=msg)


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
