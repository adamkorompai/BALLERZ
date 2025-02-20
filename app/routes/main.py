from flask import Blueprint, render_template, redirect, url_for, current_app, jsonify, request
from flask_login import login_required, current_user
import requests
import json

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.courts'))
    return redirect(url_for('auth.login'))

@main_bp.route('/courts')
@login_required
def courts():
    return render_template('main/courts.html', 
                         api_key=current_app.config['GOOGLE_MAPS_API_KEY'])

@main_bp.route('/api/courts')
@login_required
def get_nearby_courts():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    api_key = current_app.config['GOOGLE_MAPS_API_KEY']
    
    if not lat or not lng:
        return jsonify({'error': 'Location not provided'}), 400

    try:
        # Google Places API endpoint
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        
        # Parameters for the API request
        params = {
            'location': f'{lat},{lng}',
            'radius': '5000',
            'keyword': 'basketball court',
            'key': api_key
        }
        
        # Print debug information
        print("Making request with params:", json.dumps(params, indent=2))
        
        # Make the request
        response = requests.get(url, params=params)
        
        # Print response details
        print("Response status:", response.status_code)
        print("Response headers:", dict(response.headers))
        print("Response content:", response.text)
        
        # Parse the response
        data = response.json()
        
        if response.status_code != 200:
            return jsonify({
                'error': f"API Error: {data.get('status', 'Unknown error')} - {data.get('error_message', 'No message')}"
            }), response.status_code
            
        if data.get('status') == 'REQUEST_DENIED':
            error_msg = data.get('error_message', 'Request was denied by the API')
            print(f"API Request Denied: {error_msg}")
            return jsonify({'error': f"API Error: {error_msg}"}), 403
            
        if not data.get('results'):
            print("No results found in API response")
            return jsonify({'results': [], 'status': 'ZERO_RESULTS'})
            
        return jsonify(data)
        
    except Exception as e:
        import traceback
        print("Exception occurred:")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@main_bp.route('/test-map')
def test_map():
    return render_template('main/test_map.html', 
                         api_key=current_app.config['GOOGLE_MAPS_API_KEY']) 