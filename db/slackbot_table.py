from db.db_access import dynamodb
from helper import time_date_now


def create_record_slackbot(message):
    """
    Creates record in slackbot table
    """
    datetime_now, timestamp = time_date_now()

    table = dynamodb.Table('slackbot')
    table.put_item(
        Item={
            'id': timestamp,
            'sender': 'slackbot',
            'message': message,
            'date': str(datetime_now),
            'timestamp': timestamp
        }
    )


if __name__ == '__main__':
    create_record_slackbot('hello')
