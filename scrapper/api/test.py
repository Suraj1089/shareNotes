import requests

def get_github_profile_info(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        profile_data = response.json()
        print(profile_data)
        profile_info = {
            'username': profile_data['login'],
            'name': profile_data['name'],
            'photo': profile_data['avatar_url'],
            'about': profile_data['bio'],
            'location': profile_data['location'],
            'public_repos': profile_data['public_repos'],
            'followers': profile_data['followers'],
            'following': profile_data['following'],
            'blog': profile_data['blog'],
            'twitter': profile_data['twitter_username'],
            'company': profile_data['company']
        }
        # print(profile_info)
        return profile_info
    else:
        return None


get_github_profile_info("sachin-404")