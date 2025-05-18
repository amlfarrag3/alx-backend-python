seed = __import__('seed')


def stream_user_ages():
    """Generator to yield user ages one by one
    Yields:
        int: Age of each user.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data") 
    for row in cursor:
        yield row[0] 
    connection.close()


def calculate_average_age():
    """Calculates the average age using the generator and prints it.
    Rturns:
        None
    """
    total_age = 0
    count = 0
    for age in stream_user_ages(): 
        total_age += age
        count += 1
    print(f"Average age of users: {total_age / count}")

calculate_average_age()
