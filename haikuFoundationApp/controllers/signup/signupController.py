import boto3
from botocore.exceptions import ClientError


class SignUpController:
    def __init__(self, user_pool_id: str, client_id: str, region: str = "us-east-1"):
        self.user_pool_id = user_pool_id
        self.client_id = client_id

        self.client = boto3.client(
            "cognito-idp",
            region_name=region
        )

    # ---------------------------------------------------------
    # 1. CREATE USER (ADMIN FLOW)
    # ---------------------------------------------------------
    def create_user(self, username: str, email: str, password: str):
        try:
            self.client.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=username,
                UserAttributes=[
                    {"Name": "email", "Value": email}
                ],
                MessageAction="SUPPRESS"
            )

            self.client.admin_set_user_password(
                UserPoolId=self.user_pool_id,
                Username=username,
                Password=password,
                Permanent=True
            )

            return {
                "success": True,
                "message": "User created successfully"
            }

        except self.client.exceptions.UsernameExistsException:
            return {"success": False, "message": "User already exists"}

        except ClientError as e:
            return {"success": False, "message": e.response["Error"]["Message"]}

    # ---------------------------------------------------------
    # 3. SEND EMAIL OTP
    # ---------------------------------------------------------
    def send_email_otp(self, access_token: str):
        try:
            response = self.client.get_user_attribute_verification_code(
                AccessToken=access_token,
                AttributeName="email"
            )

            return {
                "success": True,
                "message": "OTP sent to email"
            }

        except ClientError as e:
            return {"success": False, "message": e.response["Error"]["Message"]}

    # ---------------------------------------------------------
    # 4. VERIFY EMAIL OTP
    # ---------------------------------------------------------
    def verify_email_otp(self, access_token: str, otp: str):
        try:
            response = self.client.verify_user_attribute(
                AccessToken=access_token,
                AttributeName="email",
                Code=otp
            )

            return {
                "success": True,
                "message": "Email verified successfully"
            }

        except ClientError as e:
            return {"success": False, "message": e.response["Error"]["Message"]}



if __name__ == "__main__":
    signup_controller = SignUpController(
        user_pool_id="your_user_pool_id",
        client_id="your_client_id",
        region="your_region"
    )                  
    signup_controller.create_user()