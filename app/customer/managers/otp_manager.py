import hashlib
import secrets
from django.utils import timezone
from customer.models import Otp
from customer.miscellaneous_values.otp import OtpStatus


class OTPManager:
    """
    Manages the entire OTP workflow

    """
    DAILY_OTP_LIMIT = 50
    ALLOWED_LOGIN_ATTEMPTS = 3
    BUFFER_SECONDS_BETWEEN_TWO_SUCCESSFUL_LOGIN_ATTEMPTS = 30
    OTP_HASH_VALUE = 'CwpDSq9nwwi'
    OTP_VALID_SECONDS = 300

    @classmethod
    def get_hashed_otp(cls, plain_text_otp: str) -> str:
        """
        Encrypts the plain text otp
        :param plain_text_otp: String which needs to be encrypted
        :return: Encrypted string
        """
        return hashlib.md5(str(plain_text_otp).encode('utf-8')).hexdigest()


    def is_otp_valid(self, phone_number: str, plain_text_otp: str):
        
        current_datetime = timezone.now()
        hashed_otp = self.get_hashed_otp(plain_text_otp)
        valid_from_time = current_datetime - timezone.timedelta(seconds=self.OTP_VALID_SECONDS)
        filters = dict(
            phone_number=phone_number,
            otp=hashed_otp,
            created_on__gte=valid_from_time,
        )
        existing_otp = Otp.objects.filter(**filters).order_by("-created_on").first()
        if existing_otp and existing_otp.status == OtpStatus.VALID:
            existing_otp.status = OtpStatus.USED
            existing_otp.save()
            return True

        return False

    def invalidate_older_otp_object(self, phone_number: str):
        otps = Otp.objects.filter(phone_number=phone_number, status=OtpStatus.VALID)
        for otp in otps:
            otp.status = OtpStatus.EXPIRED
            otp.save()

    def generate_new_otp(self, phone_number: str):
        plain_text_otp = str(secrets.choice(range(1000, 9999)))
        otp = Otp()
        otp.phone_number = phone_number
        otp.otp = self.get_hashed_otp(plain_text_otp)
        otp.status = OtpStatus.VALID
        otp.save()
        return plain_text_otp

    def send_otp(self, phone_number: str):
        
        self.invalidate_older_otp_object(phone_number)
        otp = self.generate_new_otp(phone_number)

        yesterday = timezone.now() - timezone.timedelta(days=1)
        daily_otp_count = Otp.objects.filter(
            phone_number=phone_number, created_on__gte=yesterday).count()
        if daily_otp_count > self.DAILY_OTP_LIMIT:
            raise OtpDailyLimitReached
        
        identification_hash = self.OTP_HASH_VALUE
        otp_text = notification_texts.get('OTP', {}).get('SMS', "").format(otp, identification_hash)

        #send OTP to user using SMS 
