import json

from appHandler import lambda_handler

authorization = "Bearer eyJraWQiOiJCYk5XMlFHNnVnTUtZSGJWUGRTdysrcDVzUG1TTzVPR20wWk9DVVZNbmhVPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI4NGE4NjRkOC0yMGQxLTcwNjQtZGYxNC0yYTNhZmVjMGYxMjUiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8xcGdxU3pmNDUiLCJjbGllbnRfaWQiOiIzcTM0YzQ4bzZmdmFxYmRtc3N2dW92dTg2ayIsIm9yaWdpbl9qdGkiOiI3YTIyMGI0My05Y2ZhLTRiOTktODY3YS0xOGJhODcxYTExZmEiLCJldmVudF9pZCI6ImNiNWQ0NWY0LWJkYmItNDg3OS04Y2FkLTdiOWQ3ZjZmNTJiNiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3Nzk1OTYzMzAsImV4cCI6MTc3OTU5OTkzMCwiaWF0IjoxNzc5NTk2MzMwLCJqdGkiOiI1ZTQzMTBjMS0yODg2LTRkZWYtYTI3Ny1iMDNjZGQzMmIxMjYiLCJ1c2VybmFtZSI6InNhbXNvbmJhYnVqaSJ9.llxpwm3qwd_MLq0rgMefOahzxBUN3fo0TzQbEU2B6ByDTax2Ctt97-zxfujH9rhe-RYE5AF6h3ROfaaLrz2uHU46czAHiT-Mz1AUUj83ErvuYtCj0NgJw68zJlODddjI0OS5I2-t-FFdl8840_NoZRsIRUlchNDlJIqvi15R5aMFFqgBPtnN_mhKhs0Virdahs3d_LKZ0Li9PcXshomG4Zu_kJjMLj54qJyXRFvYhMwj6k8TM-yrod60wkRrt28tyo1gpvs2JsYkRQGGUNljr7fbw96LXLHY_3y6JQdCiKFxcYwQjSD7XfUY_Z3G-bcZ_fz6t-uNyNExQ7bYPEEsWw"
event_0 = {
    "httpMethod": "POST",
    "body": json.dumps({"requestMethod": "/home", "userId": "samsonbabuji"}),
    "headers": {
        "Authorization": authorization}}
event_1 = {
    "httpMethod": "POST",
    "body": json.dumps({"requestMethod": "/topics", "userId": "samsonbabuji"}),
    "headers": {
        "Authorization": authorization}}


if __name__ == "__main__":
    print(lambda_handler(event_0, None))
    print(lambda_handler(event_1, None))
