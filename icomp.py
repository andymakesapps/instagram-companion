###IMPORTS###

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from itertools import islice
import instaloader
import getpass
import random
import time

###CLASSES###

class InstagramCompanion():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def auth(self):
        #Accepting the Data Usage Pop-Up, in try-block in case it does not appear
        try:
            driver.find_element(By.XPATH, '//button[text()="Accept"]').click()
        except:
            pass
        
        ig_username = driver.find_element_by_name("username")
        ig_password = driver.find_element_by_name("password")
        
        ig_username.send_keys(self.username)
        ig_password.send_keys(self.password)
        ig_password.send_keys(Keys.ENTER)
        
        time.sleep(5)
        
    def two_fauth(self, active=False):
        #In case user has 2FA, active should be set to True
        if active is True:
            two_factor_auth = input("2FA Code: ")        
            actions = ActionChains(driver)
            actions.send_keys(two_factor_auth).perform()
            actions.send_keys(Keys.ENTER).perform()
        else:
            pass
        
    
    def follow_user(self, user):
        driver.get('https://www.instagram.com/{}/'.format(user))
        time.sleep(2)
        followButton = driver.find_element_by_css_selector('button')
        followButton.click()
    
    def unfollow_user(self, user):
        driver.get('https://www.instagram.com/{}/'.format(user))
        time.sleep(2)
        unfollowButton = driver.find_element_by_css_selector('[aria-label=Following]')
        unfollowButton.click()
        time.sleep(2)
        confirmButton = driver.find_element_by_xpath('//button[text() = "Unfollow"]')
        confirmButton.click()
    
    def instaloader_init(self):
        L = instaloader.Instaloader()
        L.login(self.username, self.password)
        return L
    
    def get_followers_list(self, user, count=10):
        L = self.instaloader_init()
        profile = instaloader.Profile.from_username(L.context, user)
        follower_list = []
        for follower in set(islice(profile.get_followers(), count)):
            follower_list.append(follower.username)
        return follower_list
        
    def get_following_list(self, user, count=10):
        L = self.instaloader_init()
        profile = instaloader.Profile.from_username(L.context, user)
        following_list = []
        for following in set(islice(profile.get_followees(), count)):
            following_list.append(following.username)
        return following_list
        
        
    
    def add_comment(self):
        comment_bank = ["Cool!", "This is really awesome!", "Love this!", "🔥🔥🔥"]
        driver.find_element_by_css_selector('[aria-label=Comment]').click()
        time.sleep(2)
        actions = ActionChains(driver)
        actions.send_keys(random.choice(comment_bank)).perform()
        actions.send_keys(Keys.ENTER).perform()

    
    def like_photots(self, user):
        c = 0
        driver.get('https://www.instagram.com/{}/'.format(user))
        driver.find_element_by_class_name("_9AhH0").click()
        time.sleep(2)
        driver.find_element_by_css_selector('[aria-label=Like]').click()
        time.sleep(1)
        self.add_comment()
        driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a').click()
        while c <= 5:
            time.sleep(5)
            driver.find_element_by_css_selector('[aria-label=Like]').click()
            time.sleep(2)
            driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a[2]').click()
            c += 1

###FUNCTIONS###

def driver_init():
    global driver
    driver = webdriver.Chrome('/opt/anaconda3/lib/python3.8/site-packages/selenium/webdriver/chrome/chromedriver')
    url = "https://www.instagram.com/?hl=en"
    driver.get(url) 
    time.sleep(2)
    
###MAIN###

def main():
    try:    
        username = input("Username: ")
        password = getpass.getpass(prompt="Password: ")
        
        driver_init()
        
        igcomp = InstagramCompanion(username, password)
        igcomp.auth()
        igcomp.two_fauth()
        
        for user_to_unfollow in igcomp.get_following_list(username):
            try:
                igcomp.unfollow_user(user_to_unfollow)
            except:
                pass
        
        for user_to_follow in igcomp.get_followers_list("artofvisuals"):
            try:
                igcomp.follow_user(user_to_follow)
                igcomp.like_photots(user_to_follow)
            except:
                pass
            


    
    except Exception as e:
        print(e)
        driver.close()
    
    
if __name__ == "__main__":
    main()
#TO-DO: Add messages to new followers, make this act as a human, Jenkins
        
