import psycopg2

def create_table(conn, create_table_sql):
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        cursor.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        if conn:
            conn.rollback()

def table_exists(conn, table_name):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", (table_name,))
        exists = cursor.fetchone()[0]
        cursor.close()
        return exists
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        if conn:
            conn.rollback()
        return False

def run_migration(conn, table_name, create_table_sql):
  try:
        # Run the migration
        if not table_exists(conn, table_name):
            create_table(conn, create_table_sql)
            print(f"Table '{table_name}' created successfully.")
        else:
            print(f"Table '{table_name}' already exists. No action taken.")
  except (Exception, psycopg2.DatabaseError) as error:
          print(f"Error: {error}")

