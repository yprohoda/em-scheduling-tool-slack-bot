"""Sending DM in Slack by manual run or scheduler"""

from slack_sdk import WebClient
from decouple import config

from data_forms import start_scheduling_bot
from helper import task_scheduler


class SlackbotSender:
    def __init__(self, channel):
        self.channel = channel
        self.slack_client = WebClient(token=config("SLACK_BOT_TOKEN"))  # Creates a slack client

    def send_message(self, message):
        """Send message to slack channel
        """
        self.slack_client.chat_postMessage(channel=self.channel, text=message)

    def send_block(self, blocks):
        """Send message to slack channel
        """
        self.slack_client.chat_postMessage(channel=self.channel, text='text', blocks=blocks)

    # def send_scheduled_message(self, post_at, blocks, text='text'):
    #     """
    #     Send scheduled message
    #     :param sch_time: timestamp
    #     :param message: string message
    #     """
    #     self.slack_client.chat_scheduleMessage(
    #         channel=self.channel,
    #         text=text,
    #         post_at=post_at,
    #         blocks=blocks
    #     )


def send_message_to_all_interviewers(message):
    from db.interviewers_table import get_all_slack_ids
    for interviewer in get_all_slack_ids():
        slackbot = SlackbotSender(interviewer)
        slackbot.send_block(blocks=message)


def main():
    task_scheduler(send_message_to_all_interviewers)


if __name__ == '__main__':
    # main()
    send_message_to_all_interviewers(start_scheduling_bot)
