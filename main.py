from FacebookPostsScraper import FacebookPostsScraper as FPS
from pprint import pprint as pp
import configparser

config = configparser.ConfigParser()
config.read("config")

def main():
    # Enter your Facebook email and password
    email = config["DEFAULT"]["EMAIL"]
    password = config["DEFAULT"]["PASSWORD"]

    # Instantiate an object
    fps = FPS(email, password)

    # Example with single profile
    single_profile = 'https://m.facebook.com/groups/HarvardMITHousing'
    data = fps.get_posts_from_list([single_profile])
    pp(data)


if __name__ == '__main__':
    main()
