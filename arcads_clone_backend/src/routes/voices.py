from flask import Blueprint, request, jsonify

voices_bp = Blueprint('voices', __name__)

@voices_bp.route('/', methods=['GET'])
def get_voices():
    """Get available voices"""
    try:
        # Mock voices data for demo
        mock_voices = [
            {
                'id': 'voice_1',
                'name': 'Emma (Professional)',
                'language': 'English',
                'accent': 'American',
                'gender': 'Female',
                'age_range': '25-35',
                'style': 'Professional',
                'description': 'Clear, professional voice perfect for business presentations',
                'sample_url': 'https://demo-voices.elevenlabs.io/emma_professional.mp3',
                'quality_rating': 4.9,
                'usage_count': 2150
            },
            {
                'id': 'voice_2',
                'name': 'James (Narrator)',
                'language': 'English',
                'accent': 'British',
                'gender': 'Male',
                'age_range': '35-45',
                'style': 'Narrative',
                'description': 'Rich, authoritative voice ideal for storytelling and documentaries',
                'sample_url': 'https://demo-voices.elevenlabs.io/james_narrator.mp3',
                'quality_rating': 4.8,
                'usage_count': 1890
            },
            {
                'id': 'voice_3',
                'name': 'Sofia (Warm)',
                'language': 'English',
                'accent': 'American',
                'gender': 'Female',
                'age_range': '20-30',
                'style': 'Friendly',
                'description': 'Warm, approachable voice great for lifestyle and wellness content',
                'sample_url': 'https://demo-voices.elevenlabs.io/sofia_warm.mp3',
                'quality_rating': 4.7,
                'usage_count': 1650
            },
            {
                'id': 'voice_4',
                'name': 'Alex (Tech)',
                'language': 'English',
                'accent': 'American',
                'gender': 'Male',
                'age_range': '25-35',
                'style': 'Technical',
                'description': 'Clear, precise voice perfect for technical explanations and tutorials',
                'sample_url': 'https://demo-voices.elevenlabs.io/alex_tech.mp3',
                'quality_rating': 4.6,
                'usage_count': 1420
            },
            {
                'id': 'voice_5',
                'name': 'Isabella (Elegant)',
                'language': 'English',
                'accent': 'American',
                'gender': 'Female',
                'age_range': '30-40',
                'style': 'Elegant',
                'description': 'Sophisticated, refined voice ideal for luxury brands and premium content',
                'sample_url': 'https://demo-voices.elevenlabs.io/isabella_elegant.mp3',
                'quality_rating': 4.8,
                'usage_count': 980
            },
            {
                'id': 'voice_6',
                'name': 'Marcus (Casual)',
                'language': 'English',
                'accent': 'American',
                'gender': 'Male',
                'age_range': '20-30',
                'style': 'Casual',
                'description': 'Relaxed, conversational voice perfect for informal content and social media',
                'sample_url': 'https://demo-voices.elevenlabs.io/marcus_casual.mp3',
                'quality_rating': 4.5,
                'usage_count': 1200
            }
        ]
        
        # Apply filters if provided
        gender_filter = request.args.get('gender')
        accent_filter = request.args.get('accent')
        style_filter = request.args.get('style')
        language_filter = request.args.get('language')
        
        filtered_voices = mock_voices
        
        if gender_filter:
            filtered_voices = [v for v in filtered_voices if v['gender'].lower() == gender_filter.lower()]
        
        if accent_filter:
            filtered_voices = [v for v in filtered_voices if v['accent'].lower() == accent_filter.lower()]
        
        if style_filter:
            filtered_voices = [v for v in filtered_voices if style_filter.lower() in v['style'].lower()]
        
        if language_filter:
            filtered_voices = [v for v in filtered_voices if v['language'].lower() == language_filter.lower()]
        
        # Get filter options
        filters = {
            'genders': list(set([v['gender'] for v in mock_voices])),
            'accents': list(set([v['accent'] for v in mock_voices])),
            'styles': list(set([v['style'] for v in mock_voices])),
            'languages': list(set([v['language'] for v in mock_voices]))
        }
        
        return jsonify({
            'success': True,
            'data': {
                'voices': filtered_voices,
                'total_count': len(filtered_voices),
                'filters': filters,
                'pagination': {
                    'page': 1,
                    'limit': 50,
                    'total': len(filtered_voices),
                    'total_pages': 1
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@voices_bp.route('/<voice_id>', methods=['GET'])
def get_voice(voice_id):
    """Get specific voice details"""
    try:
        # Mock voice data - in production, this would fetch from database
        voices = {
            'voice_1': {
                'id': 'voice_1',
                'name': 'Emma (Professional)',
                'language': 'English',
                'accent': 'American',
                'gender': 'Female',
                'age_range': '25-35',
                'style': 'Professional',
                'description': 'Clear, professional voice perfect for business presentations',
                'sample_url': 'https://demo-voices.elevenlabs.io/emma_professional.mp3',
                'quality_rating': 4.9,
                'usage_count': 2150,
                'supported_languages': ['English'],
                'voice_characteristics': 'Clear, professional, confident tone',
                'best_use_cases': ['Business presentations', 'Corporate videos', 'Training materials']
            }
        }
        
        voice = voices.get(voice_id)
        if not voice:
            return jsonify({
                'success': False,
                'message': 'Voice not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'voice': voice
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@voices_bp.route('/generate', methods=['POST'])
def generate_voice():
    """Generate speech from text using ElevenLabs"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['text', 'voice_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Mock voice generation - in production, this would call ElevenLabs API
        audio_id = f"audio_{int(datetime.utcnow().timestamp())}"
        
        return jsonify({
            'success': True,
            'data': {
                'audio_id': audio_id,
                'audio_url': f'https://demo-audio.elevenlabs.io/{audio_id}.mp3',
                'duration': len(data['text']) * 0.1,  # Mock duration calculation
                'voice_id': data['voice_id'],
                'text': data['text']
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@voices_bp.route('/clone', methods=['POST'])
def clone_voice():
    """Clone a voice from audio samples"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Mock voice cloning - in production, this would call ElevenLabs API
        voice_id = f"cloned_voice_{int(datetime.utcnow().timestamp())}"
        
        return jsonify({
            'success': True,
            'data': {
                'voice_id': voice_id,
                'name': data['name'],
                'description': data['description'],
                'status': 'processing',
                'estimated_completion': '2025-08-13T10:45:00Z'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

