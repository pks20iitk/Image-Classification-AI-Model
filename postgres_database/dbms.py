# import psycopg2
# import json
# import logging
# from config import read_config
# from database import connect_to_database, execute_query, close_connection
#
# logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
# logger = logging.getLogger("cnnClassifierLogger")
# logger.addHandler(logging.FileHandler("running_logs.log"))
# logger.addHandler(logging.StreamHandler())
#
#
# def main():
#     try:
#         params = read_config()
#         conn = connect_to_database(params)
#         print("connection sucssefull")
#
#         if conn is not None:
#             try:
#                 with psycopg2.connect(**params) as conn, conn.cursor() as cursor:
#                     create_table_query = """
#                                CREATE TABLE IF NOT EXISTS public.result_table (
#                                    id SERIAL PRIMARY KEY,
#                                    loss DOUBLE PRECISION,
#                                    accuracy DOUBLE PRECISION,
#                                    image VARCHAR(255),
#                                    predicted_result VARCHAR(50),
#                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                                );
#                            """
#                     cursor.execute(create_table_query)
#
#                     insert_query = """
#                                INSERT INTO public.result_table (loss, accuracy, image, predicted_result)
#                                VALUES (%s, %s, %s, %s)
#                            """
#                     cursor.execute(
#                         insert_query,
#                         (float(raw_result[0]), float(raw_result[1]), 'your_image_filename.jpg', prediction_label)
#                     )
#                     conn.commit()
#
#             except Exception as e:
#                 logger.error(f"Error: {e}")
#             query = 'SELECT * FROM public."user"'
#             result = execute_query(conn, query)
#
#             if result:
#                 print('PostgreSQL database version:')
#                 print(result)
#
#             close_connection(conn)
#     except Exception as e:
#         print(e)
#
#
# if __name__ == '__main__':
#     main()
