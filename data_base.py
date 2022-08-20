import sqlite3

connect = sqlite3.connect("tasks")
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
                                        task STRING,
                                        right_answer STRING
                                    )
                                                   """)
connect.commit()