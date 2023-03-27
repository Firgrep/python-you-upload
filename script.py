# -*- coding: utf-8 -*-
import os
import pickle

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# Path-related top-level
ABSOLUTE_PATH = os.path.dirname(__file__)
RELATIVE_PATH = "../../payload"
FULL_PATH = os.path.join(ABSOLUTE_PATH, RELATIVE_PATH)

# Instance-related data - information unique to this video upload.
S_TITLE = "Test no 3 - March 27"
S_PUBLISH_DATE = "2023-04-10T19:20+01:00"
S_UNIQUE_DESC_START = "This is the third test video for March 27."
S_UNIQUE_DESC_END = ""

# Generic-related data - information shared between videos of which this is an instance.
F_UPLOAD_MEDIA = "vid.mp4" #Easier to leave these as is and alter the name of the files instead.
F_THUMBNAIL = "t.png"
S_PRIVACY_STATUS = "private"
S_CATEGORY_ID = "27"
B_FOR_KIDS = False
S_DESCRIPTION = f"""
{S_UNIQUE_DESC_START}

📘 The text used is GWF Hegel, Lectures on the Philosophy of World Hisory Volume 1: Manuscripts of the Introduction and The Lectures of 1822-3, Edited and Translated by Robert F. Brown and Peter C. Hodgson, with the assistance of William G. Geuss. CLARENDON PRESS • OXFORD, 2011. ISBN 978-0-19-960170-7.

=======================================

AHILLEAS ROKNI completed his PhD thesis in philosophy in 2022, under the supervision of Professor Stephen Houlgate, at the University of Warwick. His thesis aimed to give an account of the much-debated move from the Science of Logic to the Philosophy of Nature in Hegel’s system. Ahilleas’s main research concerns are Hegel’s Logic, philosophy of nature, philosophy of science, and aesthetics. Ahilleas’ overarching interest is in the cohesiveness of Hegel’s systematic philosophy. Hegel’s philosophy is not just the Science of Logic or the Philosophy of Right but is an account of how abstract metaphysics immanently develops into concrete reality This was the impetus behind his PhD research and it is the impetus behind his interest in sPhil: to continue to interrogate whether Hegel’s systematic philosophy is coherent.

🎙️ Ahilleas also hosts the podcast Please Expand that centers on interviews of authors of non-fiction books on topics ranging from history to philosophy, and science to religion, which you can find here: https://www.pleaseexpand.com/

💫 Along with Filip and others, Ahilleas has organized the Hegel at Warwick conference series. https://hegelwarwick.wordpress.com/


FILIP NIKLAS completed his PhD in philosophy in 2022, under the supervision of Professor Stephen Houlgate, at the University of Warwick. The title of his thesis was Hegel’s Critique of Determinism: Justifying Unfreedom as a Moment of Freedom.

👨🏻‍🏫 Filip gives online courses at the Halkyon Academy. You can check out his and other courses in the Cathedral of Learning here: https://www.halkyonguild.org/

📗 For his course on Hegel’s PHENOMENOLOGY OF SPIRIT, please go to: https://halkyonacademy.teachable.com/p/hegel-s-phenomenology-of-spirit
📚 For his course on Hegel’s SYSTEM more broadly, please go to:
https://halkyonacademy.teachable.com/p/hegel-masterclass
📘 For his course on WHAT IS PHILOSOPHY – an introduction to philosophy through R. G. Collingwood and others – please go to: 
https://halkyonacademy.teachable.com/p/what-is-philosophy

Filip also enjoys ensnaring words in poetic thought-patterns: You can find some of his work here:
📒 https://tinyurl.com/saedah-poem

📲 http://www.filipniklas.com/
🐦@FilipNiklas
=======================================

{S_UNIQUE_DESC_END}
"""

L_TAGS = ["Philosophy","hegel","logic","ontology","metaphysics","german idealism", "idealism", "existence","freedom","categories","Houlgate","thinking","thought","speculative" "thinking","conceptual" "thinking","conceptual" "analysis","concepts","world history", "history"]
S_PLAYLIST_ID = os.environ.get("SPHIL_WORLDHISTORY_PLAYLIST_ID")

# Scopes - part of authentication call.
scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]

def main():
    credentials = None

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # AUTHENTICATION
    # First retrieve token.pickle, which stores the user's credentials from previously successful logins.
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

    # YOUTUBE OBJECT BUILD
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # Video upload.
    request = youtube.videos().insert(
        part="snippet,status",
        body={
          "snippet": {
            "categoryId": S_CATEGORY_ID,
            "description": S_DESCRIPTION,
            "title": S_TITLE,
            "tags": L_TAGS,
          },
          "status": {
            "privacyStatus": S_PRIVACY_STATUS,
            "publishAt": S_PUBLISH_DATE,
            "selfDeclaredMadeForKids": B_FOR_KIDS
          }
        },
        media_body=MediaFileUpload(os.path.join(FULL_PATH, F_UPLOAD_MEDIA))
    )
    response = request.execute()

    videoId = response["id"]
    print("Video Upload Complete.")

    # Thumbnail upload.
    request_second = youtube.thumbnails().set(
        videoId=videoId,
        media_body=MediaFileUpload(os.path.join(FULL_PATH, F_THUMBNAIL))
    )
    request_second.execute()
    print("Thumbnail Upload Complete.")

    # If playlist detected, add to playlist.
    if S_PLAYLIST_ID:
        print("Playlist detected. Adding video to playlist...")
        request_third = youtube.playlistItems().insert(
            part="snippet",
            body={
              "snippet": {
                "playlistId": S_PLAYLIST_ID,
                "resourceId": {
                  "kind": "youtube#video",
                  "videoId": videoId
                }
              }
            }
        )

        request_third.execute()
        print("Video Added To Playlist Complete.")
    
    print(f"Script Done. {S_TITLE} has been uploaded to YouTube.")

if __name__ == "__main__":
    main()