import psycopg2
import pandas as pd


spreadsheet_file = 'TweetDates.tsv'

def database_setup():
    # dataframe

    column_types = {
        'date': str,
        'tweet_text': str,
        'image_id': str,
        'link': str,
        'characters': str
    }
    df = pd.read_csv(spreadsheet_file, sep='\t', dtype=column_types)

    df.head()
    print(df.dtypes)

    df['year'] = df['date'].str.split('-').str[0].astype(int)
    df['month'] = df['date'].str.split('-').str[1].astype(int)
    df['day'] = df['date'].str.split('-').str[2].astype(int)
    print(df)
    #df['datetime'] = pd.to_datetime(df['date'], format='ISO8601')
    #df['year'] = df['date'].dt.year


    # Converting format of date not necessary, as xlsx date column is already in the correct datetime format
    #   If you need to convert the date format, uncomment the following line:
    #   df["date"] = pd.to_datetime(df["date"])
    #df['date_year'] = df['date'].year

    # Convert DataFrame to list of tuples
    data_tuples = list(df.itertuples(index=False, name=None))
    print(data_tuples)

    # Connect to PostgreSQL database
    conn = psycopg2.connect(host="localhost", dbname="tweets", user="postgres", password="corndog", port=5432)
    cursor = conn.cursor()
    # Drop and reload old table
    cursor.execute("""DROP TABLE IF EXISTS tweet;""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS tweet (
            id SERIAL PRIMARY KEY,
            date TIMESTAMP,
            date_year INT,
            date_month INT,
            date_day INT,
            tweet_text TEXT,
            image_id TEXT,
            link TEXT,
            characters INT
        );
        """)
    conn.commit()
    # Insert tweet text into the table
    insert_query = """INSERT INTO tweet (date, tweet_text, image_id, link, characters, date_year, date_month, date_day)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    # Execute the insert query with the data
    cursor.executemany(insert_query, data_tuples)
    conn.commit()


    # Close connections
    cursor.close()
    conn.close()

database_setup()