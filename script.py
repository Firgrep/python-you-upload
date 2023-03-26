# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.insert
# NOTES:
# 1. This sample code uploads a file and can't be executed via this interface.
#    To test this code, you must run it locally using your own API credentials.
#    See: https://developers.google.com/explorer-help/code-samples#python
# 2. This example makes a simple upload request. We recommend that you consider
#    using resumable uploads instead, particularly if you are transferring large
#    files or there's a high likelihood of a network interruption or other
#    transmission failure. To learn more about resumable uploads, see:
#    https://developers.google.com/api-client-library/python/guide/media_upload

import os
import pickle
import datetime
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

S_TITLE = "Example title"
F_UPLOAD_MEDIA = "sample.mp4"
F_THUMBNAIL = "thumbnail.png"
DATETIME_PUBLISH_DATE = "2023-04-10T19:20+01:00"
S_UNIQUE_DESCRIPTION = "This is the test video."

S_PRIVACY_STATUS = "private"
L_TAGS = ["Philosophy","hegel","logic","ontology","metaphysics","german" "idealism","existence","freedom","categories","Houlgate","thinking","thought","speculative" "thinking","conceptual" "thinking","conceptual" "analysis","concepts","world history", "history"]
S_DESCRIPTION = f"""
{S_UNIQUE_DESCRIPTION}

📘 The text used is GWF Hegel, Lectures on the Philosophy of World Hisory Volume 1: Manuscripts of the Introduction and The Lectures of 1822-3, Edited and Translated by Robert F. Brown and Peter C. Hodgson, with the assistance of William G. Geuss. CLARENDON PRESS • OXFORD, 2011. ISBN 978-0-19-960170-7.
=======================================

AHILLEAS ROKNI completed his PhD thesis in philosophy in 2022, under the supervision of Professor Stephen Houlgate, at the University of Warwick. His thesis aimed to give an account of the much-debated move from the Science of Logic to the Philosophy of Nature in Hegel’s system. Ahilleas’s main research concerns are Hegel’s Logic, philosophy of nature, philosophy of science, and aesthetics. Ahilleas’ overarching interest is in the cohesiveness of Hegel’s systematic philosophy. Hegel’s philosophy is not just the Science of Logic or the Philosophy of Right but is an account of how abstract metaphysics immanently develops into concrete reality This was the impetus behind his PhD research and it is the impetus behind his interest in sPhil: to continue to interrogate whether Hegel’s systematic philosophy is coherent.
"""

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    credentials = None

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # AUTHENTICATION
    # token.pickle stores the user's credentials from previously successful logins.
    if os.path.exists("token.pickle"):
        print("Loading Credentials From File...")
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    # If no valid credentials availale, refresh token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Refreshing Access Token...")
            credentials.refresh(Request())
            with open("token.pickle", "wb") as f:
                print("Saving Refreshed Credentials for Future Use...")
                pickle.dump(credentials, f)

        else: 
            print("Fetching New Tokens...")
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    client_secrets_file, scopes)
            credentials = flow.run_console()
            with open("token.pickle", "wb") as f:
                print("Saving Credentials for Future Use...")
                pickle.dump(credentials, f)

    # FILE UPLOAD
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
          "snippet": {
            "categoryId": "27",
            "description": S_DESCRIPTION,
            "title": S_TITLE,
            "tags": L_TAGS,
          },
          "status": {
            "privacyStatus": S_PRIVACY_STATUS,
            "publishAt": DATETIME_PUBLISH_DATE,
            "selfDeclaredMadeForKids": False
          }
        },
        media_body=MediaFileUpload(F_UPLOAD_MEDIA)
    )
    response = request.execute()

    videoId = response["id"]
    print(videoId)
    print("Video Upload Complete.")

    request_second = youtube.thumbnails().set(
        videoId=videoId,
        media_body=MediaFileUpload(F_THUMBNAIL)
    )
    request_second.execute()
    print("Thumbnail Upload Complete.")

if __name__ == "__main__":
    main()