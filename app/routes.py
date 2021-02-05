import json
from flask import request
from datetime import date
from dateutil.relativedelta import relativedelta

from app import app
from app.utils import read_json, distance


@app.route('/discovery')
def discovery():
    lat = request.args.get('lat', type=float, default=None)
    lon = request.args.get('lon', type=float, default=None)
    data = {"sections": [{"title": "Popular Restaurants", "restaurants": []},
                         {"title": "New Restaurants", "restaurants": []},
                         {"title": "Nearby Restaurants", "restaurants": []}]}

    try:
        if lat is None or lon is None or lat < -180. or lat > 180. or lon < -180. or lon > 180.:
            app.logger.info('Invalid arguments'.format(lon, lat))
            raise ValueError()

        restaurants = read_json('restaurants.json')['restaurants']  # db select

        # select restaurant in range
        in_range = [[r, dist] for r in restaurants if (dist := distance(lat, lon, r['location'][1], r['location'][0])) < 1.5]

        if not in_range:
            app.logger.info('No restaurant around [{:.4f}, {:.4f}]'.format(lon, lat))
            raise ValueError()

        # get nearby restaurant
        nearby = [r for r, _ in sorted(in_range, key=lambda rest_dist: (rest_dist[0]['online'], rest_dist[1]))][:10]
        # transpose
        in_range = list(map(list, zip(*in_range)))

        popular = sorted(in_range[0], key=lambda x: (x['online'], x['popularity']), reverse=True)[:10]
        new_rest = sorted(in_range[0], key=lambda x: (x['online'], date.fromisoformat(x['launch_date'])), reverse=True)[:10]

        # remove restaurants opened earlier then 4 months ago
        idx = len(new_rest)
        today_minus_4months = date.today() - relativedelta(months=4)
        while idx > 0 and date.fromisoformat(new_rest[idx - 1]['launch_date']) < today_minus_4months:
            idx -= 1

        data['sections'][0]['restaurants'] += popular
        data['sections'][1]['restaurants'] += new_rest[:idx]
        data['sections'][2]['restaurants'] += nearby

    except ValueError:
        pass
    finally:
        return json.dumps(data, indent=2)




