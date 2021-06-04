import boto3
from decouple import config

dynamodb = boto3.resource('dynamodb',
                          region_name='eu-central-1',
                          aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY")
                          )


def create_table(table_name, column1, column2):
    """
    Create table in Dynamo DB
    :param table_name: table created in DB
    """
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': column1,
                'KeyType': 'HASH'
            },
            {
                'AttributeName': column2,
                'KeyType': 'RANGE'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': column1,
                'AttributeType': 'N'
            },
            {
                'AttributeName': column2,
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)


if __name__ == '__main__':
    #create_table('timeslots_confirmed', 'interviwer_id', 'timeslot_id')
    create_table(table_name='timeslots_confirmed',
                 column1='interviewer_id',
                 column2='timeslot_id')
