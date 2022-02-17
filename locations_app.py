"""
Flask app to display twitter friends locations.
"""

import tweepy
import folium

from flask import Flask, render_template, Markup, flash
from flask import request

from geopy.geocoders import Nominatim

consumer_key = "enter_yourself"
consumer_secret = "enter_yourself"
access_token_key = "enter_yourself"
access_token_secret = "enter_yourself"


app = Flask(__name__)
app.config['SECRET_KEY'] = 'enter_yourself'


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Rendering the webpage.
    """

    folium_map = folium.Map(zoom_start=1)

    if request.method == 'POST':
        username = request.form.get('username')

        if username:
            locations_data = get_users_locations(username)

            for user in locations_data:
                if user[2]:
                    folium.Marker(
                        [user[2].latitude, user[2].longitude],
                        popup="<p><b>" + user[0] +
                        "</b><br>" + user[1] + "</p>",
                    ).add_to(folium_map)

    map_html = Markup(folium_map._repr_html_())
    flash(map_html)

    return render_template('index.html')


def get_users_locations(user_name: str):
    """
    Get data using tweepy.
    """

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    api = tweepy.API(auth)

    geolocator = Nominatim(user_agent="geomap-app")

    users_data = []

    try:
        followers = api.friends(screen_name=user_name)

        if followers:
            for follower in followers:
                users_location = geolocator.geocode(follower.location)

                users_data.append(
                    (follower.screen_name, follower.location, users_location))
    except Exception:
        return []

    return users_data


if __name__ == '__main__':
    app.run(debug=True)
