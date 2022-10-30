import requests as requests
from flask import Blueprint, make_response, render_template, request, flash
from flask_login import current_user

from .models import Nft

nft = Blueprint('nft', __name__)


@nft.route('/nft_search', methods=['GET'])
def nft_search():
    global payload
    args = request.args['nft']

    url = f"https://solana-gateway.moralis.io/nft/mainnet/{args}/metadata"

    headers = {

        "accept": "application/json",

        "X-API-Key": "mExR5fyAxWjT4qVSLGVukSJ9c33mrx7iUekmzoaSxqfIEmJWsdiicigP4FQ71QFn"

    }

    nft = Nft()
    dbExist = nft.checkInDb(args)

    if dbExist:
        payload = dbExist
        return make_response(render_template('nft_result.html', payload=payload, user=current_user))
    else:
        try:
            response = requests.get(url, headers=headers)
            response2 = response.json()

            payload = {
                "name": response2["name"],
                "description": response2["metaplex"]["metadataUri"],
                "address": response2["mint"]

            }

            nft1 = Nft(**payload)

            nft1.addToDb()
        except KeyError or TypeError or NameError:
            flash('Invalid address', category='error')

        return make_response(render_template('nft_result.html', payload=payload, user=current_user))
