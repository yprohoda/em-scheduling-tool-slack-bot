"""Block forms"""
# https://app.slack.com/block-kit-builder/

home_tab_blocks = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Start scheduling bot."
        },
        "accessory": {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Start",
                "emoji": True
            },
            "value": "click_me_123",
            "action_id": "Start-scheduling-bot"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Check available interviewers."
        },
        "accessory": {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Check",
                "emoji": True
            },
            "value": "click_me_123",
            "action_id": "Check-available-interviewers-btn"
        }
    }
]

"""Form of Start scheduling bot"""
start_scheduling_bot = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Start scheduling bot"
        },
        "accessory": {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Start",
                "emoji": True
            },
            "value": "click_me_123",
            "action_id": "Start-scheduling-bot"
        }
    }
]

available_interviewers_blocks = [
    {
        "type": "input",
        "element": {
            "type": "static_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select the discipline",
                "emoji": True
            },
            "options": [
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Dev",
                        "emoji": True
                    },
                    "value": "value-0"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "QA",
                        "emoji": True
                    },
                    "value": "value-1"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Devops",
                        "emoji": True
                    },
                    "value": "value-2"
                }
            ],
            "action_id": "static_select-action"
        },
        "label": {
            "type": "plain_text",
            "text": "Discipline",
            "emoji": True
        }
    },
    {
        "type": "input",
        "element": {
            "type": "static_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select the technology",
                "emoji": True
            },
            "options": [
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Python",
                        "emoji": True
                    },
                    "value": "value-0"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Java",
                        "emoji": True
                    },
                    "value": "value-1"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "JavaScript",
                        "emoji": True
                    },
                    "value": "value-2"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "C#",
                        "emoji": True
                    },
                    "value": "value-3"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "C++",
                        "emoji": True
                    },
                    "value": "value-4"
                }
            ],
            "action_id": "static_select-action"
        },
        "label": {
            "type": "plain_text",
            "text": "Technology stack",
            "emoji": True
        }
    },
    {
        "type": "input",
        "element": {
            "type": "datepicker",
            "initial_date": "2021-06-01",
            "placeholder": {
                "type": "plain_text",
                "text": "Select a date",
                "emoji": True
            },
            "action_id": "datepicker-action"
        },
        "label": {
            "type": "plain_text",
            "text": "Date",
            "emoji": True
        }
    }
]


def checkboxes_with_timeslots(list_):
    """From selection timeslots"""
    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Scheduling-slack-bot",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "The bot runs once a week and offers to choose from 10 slots only 2 for the coming week, "
                        "or repeat, as in the last",
                "emoji": True
            }
        },
        {
            "type": "input",
            "element": {
                "type": "checkboxes",
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": list_[0]['date'],
                            "emoji": True
                        },
                        "value": list_[0]['id']
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": list_[1]['date'],
                            "emoji": True
                        },
                        "value": list_[1]['id']
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": list_[2]['date'],
                            "emoji": True
                        },
                        "value": list_[2]['id']
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": list_[3]['date'],
                            "emoji": True
                        },
                        "value": list_[3]['id']
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": list_[4]['date'],
                            "emoji": True
                        },
                        "value": list_[4]['id']
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": list_[5]['date'],
                            "emoji": True
                        },
                        "value": list_[5]['id']
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": list_[6]['date'],
                            "emoji": True
                        },
                        "value": list_[6]['id']
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": list_[7]['date'],
                            "emoji": True
                        },
                        "value": list_[7]['id']
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": list_[8]['date'],
                            "emoji": True
                        },
                        "value": list_[8]['id']
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": list_[9]['date'],
                            "emoji": True
                        },
                        "value": list_[9]['id']
                    },
                ],
                "action_id": "checkboxes-action"
            },
            "label": {
                "type": "plain_text",
                "text": "Choose at least 2 slots from following:",
                "emoji": True
            }
        },
    ]
