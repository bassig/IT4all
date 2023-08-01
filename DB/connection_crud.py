from DB.db_initializer import get_connection
import aiomysql


# async def add_connections(connections):
#     query = """
#     INSERT INTO Connection (SourceMac, DestMac, ProtocolName, Length, Time)
#     VALUES (%s, %s, %s, %s, %s)
#     """
#     try:
#         connection = await get_connection()
#         async with connection.cursor() as cursor:
#             for connection_data in connections:
#                 await cursor.execute(
#                     query,
#                     (connection_data.SourceMac, connection_data.DestMac, connection_data.ProtocolName,
#                      connection_data.Length, connection_data.Time)
#                 )
#         connection.commit()
#         print("Multiple rows inserted successfully.")
#         return True
#     except Exception as e:
#         print(f"Error: {e}")
#         return False


# async def add_connections(connections):
#     if not connections:
#         return False
#
#     query = """
#     INSERT INTO Connection (SourceMac, DestMac, ProtocolName, Length, Time)
#     VALUES (%s, %s, %s, %s, %s)
#     """
#     try:
#         connection = await get_connection()
#         async with connection.cursor() as cursor:
#             connection_data_list = [(conn.SourceMac, conn.DestMac, conn.ProtocolName, conn.Length, conn.Time) for conn
#                                     in connections]
#             await cursor.executemany(query, connection_data_list)
#             await connection.commit()
#             print(f"{len(connections)} connections inserted successfully.")
#             return True
#     except Exception as e:
#         print(f"Error: {e}")
#         return False


async def add_connections(connections):
    if not connections:
        return False

    query = """
    INSERT INTO Connection (SourceMac, DestMac, ProtocolID, Length, Time)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        connection = await get_connection()
        async with connection.cursor() as cursor:
            for conn in connections:
                try:
                    await cursor.execute(query,
                                         (conn.SourceMac, conn.DestMac, conn.ProtocolID, conn.Length, conn.Time))
                except Exception as e:
                    print(f"Error inserting connection: {conn.SourceMac} -> {conn.DestMac}. Error: {e}")
            await connection.commit()
            print(f"{len(connections)} connections inserted successfully.")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False


async def get_protocol_id(protocol: str):
    connection = await get_connection()
    async with connection.cursor() as cursor:
        # Get the ProtocolID based on the protocol name
        query_to_check_role_id = "SELECT ID FROM Protocol WHERE Name = %s"
        print(f"Executing query: {query_to_check_role_id} with parameter: {protocol}")
        await cursor.execute(query_to_check_role_id, (protocol,))
        protocol_id = await cursor.fetchone()
        print(f"Result: {protocol_id}")
        return protocol_id

