import requests
from rest_framework import status
from rest_framework.response import Response

from qteam_quest.utils import get_env_value


def send_sms_code(phone, sms_text):
    prostor_sms_api_login = get_env_value('PROSTOR_SMS_API_LOGIN')
    prostor_sms_api_password = get_env_value('PROSTOR_SMS_API_PASSWORD')
    send_sms_url = f'http://{prostor_sms_api_login}:{prostor_sms_api_password}@api.prostor-sms.ru/' \
                   f'send/?phone={phone}&text={sms_text}'
    response = requests.get(url=send_sms_url)
    if response.content == b'not enough credits':
        return Response({
            'message': 'Not enough credits on Prostor SMS account!',
        }, status=status.HTTP_400_BAD_REQUEST)
    if response.content == b'invalid mobile phone':
        return Response({
            'message': 'Invalid mobile phone!',
        }, status=status.HTTP_400_BAD_REQUEST)
    if response.content == b'text is empty':
        return Response({
            'message': 'Text is empty!',
        }, status=status.HTTP_400_BAD_REQUEST)
