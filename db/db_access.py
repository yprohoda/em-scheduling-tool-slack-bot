import boto3
from decouple import config

dynamodb = boto3.resource('dynamodb',
                          region_name='eu-central-1',
                          aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY")
                          )


def create_table(table_name, column1, column2, type1='N', type2='N'):
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
                'AttributeType': type1
            },
            {
                'AttributeName': column2,
                'AttributeType': type2
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
    pass