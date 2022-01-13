import os
from dotenv import load_dotenv

load_dotenv()
access_points_file = os.getenv('ACCESS_POINTS_FILE')
server_address = os.getenv('SERVER_ADDRESS')
server_port = int(os.getenv('SERVER_PORT'))
