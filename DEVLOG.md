# DEVLOG

Educational notes to self.

* When adding requests that require new/modified scopes, make sure to completely restart the authentication process. I wanted to get the playlist resource but I kept getting error 403 "Request had insufficient authentication scopes."
    - Fix: delete the pickle file and run the program again to re-authenticate with the latest scopes from the beginning. 

* os.environ.get() was returning None even though other older environ variables were being returned fine, and I double-checked the name. Since the old ones were working but any new ones I made were not, I suspected that a refresh somewhere in the system was needed. 
    - Fix: Restarting the code editor wasn't sufficient, but closing down bash, code editor and restarting the computer did the trick.