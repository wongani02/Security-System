import socket
import os
import sys
import django
import json
from twilio.rest import Client


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings") 

django.setup()


Twilio_Phone_Number = '####'
admin_Phone = '######'

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_AUTH_TOKEN)


def get_host_ip():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Connect to a known address (Google's DNS server)
        s.connect(('8.8.8.8', 80))
        # Get the local IP address of the host
        host_ip = s.getsockname()[0]
        print('This is the current ipaddress', host_ip)
    except Exception as e:
        print("Error:", e)
        host_ip = None
    finally:
        s.close()
    
    return host_ip

#add your django server's port here.
host, port = get_host_ip(), 8000


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()

print(f"Listening on {host}:{port}")

conn, addr = s.accept()
print(f"Connection established with {addr}")

from security.models import (
    SecuredDoor, UserSecurityCredential, SecurityLog
)


try:
    while True:
        data = conn.recv(1024)
        if not data:
            break

        try: 
            decoded_data = data.decode('utf-8')
            json_data = json.loads(decoded_data)
            print(json_data)

            response_to_server = {'access': False }
            try:
                user = UserSecurityCredential.objects.get(card_uid=json_data['id'])
                print(user)

                door = SecuredDoor.objects.get(id=json_data['door_id'])
                print(door)

                response_to_server = None
                if user in door.permitted_users.all():
                    log = SecurityLog.objects.create(
                        door=door,
                        access_pass=user,
                        session_id=json_data['session_id'],
                        entry_img=json_data['image_id'],
                        entry_status=True
                    )
                    response_to_server={'access': True }
                else:
                    log = SecurityLog.objects.create(
                        door=door,
                        access_pass=user,
                        session_id=json_data['session_id'],
                        entry_img=json_data['image_id'],
                        entry_status=False
                    )
                    response_to_server={'access': False }

                    twilio_client.messages.create(
                        body=f'{user.card_name} tried to access {door.door_name}.',
                        from_=Twilio_Phone_Number,
                        to=admin_Phone
                    )
            except Exception as e:
                print('ERROR: ', e)
        
            response_to_server = json.dumps(response_to_server)
            conn.sendall(response_to_server.encode('utf-8'))
            print('response sent')

        except Exception as e:
            print('Error : ', e)
            pass
        print(f"Received: {data.decode('utf-8')}")

except Exception as e:
    print("Error:", e)
    
finally:
    conn.close()


