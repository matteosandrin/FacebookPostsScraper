from FacebookPostsScraper import FacebookPostsScraper as Fps
from pprint import pprint as pp

def main():
    # Enter your Facebook email and password
    email = ''
    password = ''

    # Instantiate an object
    fps = Fps(email, password)

    # Example with single profile
    single_profile = 'https://m.facebook.com/groups/HarvardMITHousing'
    data = fps.get_posts_from_list([single_profile])
    pp(data)


if __name__ == '__main__':
    main()
