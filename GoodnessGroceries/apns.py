import json
import jwt
import time
from hyper import HTTPConnection

APNS_KEY_ID = 'QZLBCQ6DBD'
APNS_AUTH_KEY = 'apns_key.p8'
TEAM_ID = 'KZP7B8QNG2'
BUNDLE_ID = 'lu.uni.bicslab.goodnessgroceries'


def send_push_notification(device_token, payload_data):
    f = open(APNS_AUTH_KEY)
    secret = f.read()

    token = jwt.encode({
        'iss': TEAM_ID,
        'iat': time.time()
    },
        secret,
        algorithm='ES256',
        headers={
            'alg': 'ES256',
            'kid': APNS_KEY_ID,
    }
    )

    path = '/3/device/{0}'.format(device_token)

    request_headers = {
        'apns-expiration': '0',
        'apns-priority': '10',
        'apns-topic': BUNDLE_ID,
        'authorization': 'bearer {0}'.format(token.decode('ascii'))
    }

    conn = HTTPConnection('api.development.push.apple.com:443')

    payload = json.dumps(payload_data).encode('utf-8')

    conn.request(
        'POST',
        path,
        payload,
        headers=request_headers
    )
    resp = conn.get_response()
