# -*- coding: utf-8 -*-

import instaloader

# Custom exceptions
class EmptyFieldError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        


def instagram_login(username, password):
    
    try:
        if not username or not password:
            raise EmptyFieldError("Please enter both username and password.")
            
        # Log in to Instagram
        global USER
        USER = username
        global PASSWORD
        PASSWORD = password
        loader.login(username, password)
        
    except instaloader.exceptions.ProfileNotExistsException as e:
        raise instaloader.exceptions.ProfileNotExistsException("Profile does not exist") from e
        
    except instaloader.exceptions.ConnectionException as e:
        raise instaloader.exceptions.ConnectionException("Verification required") from e
        
        
def get_profile(user='self'):
    if user=='self':
        return instaloader.Profile.from_username(loader.context, loader.context.username)
    else:
        return instaloader.Profile.from_username(loader.context, user)
        
    
def get_non_followers(profile):
    
    # Get the list of followers
    print("Getting followers...")
    followers = set(profile.get_followers())
    
    instagram_login(USER, PASSWORD)
    
    # Get the list of followees (accounts the user is following)
    print("Getting followees...")
    followees = set(profile.get_followees())
    print("Done!")

    # Get the list of users not following back
    not_following_back = followees - followers

    return [user.username for user in not_following_back]
    
    
    


# Create an instance of Instaloader
loader = instaloader.Instaloader()