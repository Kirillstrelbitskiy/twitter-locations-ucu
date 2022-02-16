import tweepy

from flask import Flask, render_template, Markup, flash
from flask import request
import folium

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from geopy.geocoders import Nominatim

consumer_key = "v5a1250pNEYgNsD3J9MFiicxm"
consumer_secret = "15OOiUz5T1yfho9zmFn9KJCtu9ZJRq13Rl86vhD0dhuUX6sH3g"
access_token_key = "950059146715582465-7ewp0GPlLVmYeq8IgCkGYlqk1N4s5GS"
access_token_secret = "9WQZ4UW7HjDG4Q0zbbbGMsvsE5HTFfacMREEwQt03i5e3"


app = Flask(__name__)
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'


@app.route('/', methods=['GET', 'POST'])
def index():
    folium_map = folium.Map(zoom_start=1)

    if request.method == 'POST':
        username = request.form.get('username')

        if username:
            locations_data = get_users_locations(username)

            for user in locations_data:
                if user[2]:
                    folium.Marker(
                        [user[2].latitude, user[2].longitude],
                        popup="<p><b>" + user[0] + "</b><br>" + user[1] + "</p>",
                    ).add_to(folium_map)

    map_html = Markup(folium_map._repr_html_())
    flash(map_html)

    return render_template('index.html')


def get_users_locations(user_name: str):
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
