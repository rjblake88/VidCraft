from flask import Blueprint, request, jsonify, current_app
from flask import Response
import os
from urllib.parse import urlparse
import requests
from datetime import datetime
from pathlib import Path

ELEVEN_API_BASE = 'https://api.elevenlabs.io/v1'
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')

voices_bp = Blueprint('voices', __name__)

@voices_bp.route('/', methods=['GET'])
def get_voices():
    """Get available voices"""
    try:
        if ELEVENLABS_API_KEY:
            try:
                r = requests.get(f"{ELEVEN_API_BASE}/voices", headers={'xi-api-key': ELEVENLABS_API_KEY})
                if r.ok:
                    payload = r.json()
                    items = payload.get('voices') or []
                    mapped = []
                    for v in items:
                        mapped.append({
                            'id': v.get('voice_id') or v.get('id'),
                            'name': v.get('name'),
                            'language': 'English',
                            'accent': '',
                            'gender': '',
                            'age_range': '',
                            'style': '',
                            'description': v.get('description') or '',
                            'sample_url': v.get('preview_url') or '',
                            'quality_rating': None,
                            'usage_count': None
                        })
                    return jsonify({
                        'success': True,
                        'data': {
                            'voices': mapped,
                            'total_count': len(mapped),
                            'filters': {'genders': [], 'accents': [], 'styles': [], 'languages': []},
                            'pagination': {'page': 1, 'limit': 50, 'total': len(mapped), 'total_pages': 1},
                        }
                    })
            except Exception as ex:
                if current_app:
                    current_app.logger.error(f"ElevenLabs voices fetch failed: {ex}")

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

# ---------------------------------------------------------------------------
# Preview proxy – stream remote ElevenLabs sample audio to workaround CORS
# ---------------------------------------------------------------------------

@voices_bp.route('/preview', methods=['GET'])
def preview_proxy():
    """
    Proxy remote preview audio files (e.g. ElevenLabs samples) so the frontend
    can fetch them from the same origin and avoid CORS / mixed-content issues.

    Query params:
        url – full HTTPS URL of the audio file to proxy
    """
    try:
        url = request.args.get('url')
        if not url:
            return jsonify({'success': False, 'message': 'Missing url parameter'}), 400

        parsed = urlparse(url)

        # Allow only known safe hosts to mitigate open proxy abuse
        allowed_hosts = {
            'storage.googleapis.com',
            'eleven-public-prod.storage.googleapis.com',
            'cdn.elevenlabs.io',
            'api.elevenlabs.io',
            'elevenlabs.io',
        }
        if parsed.hostname not in allowed_hosts and not parsed.hostname.endswith('googleapis.com'):
            return jsonify({'success': False, 'message': 'Host not allowed'}), 400

        r = requests.get(url, stream=True, timeout=30)
        if not r.ok:
            return jsonify({'success': False, 'message': f'Upstream error: {r.status_code}'}), r.status_code

        def generate():
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk

        content_type = r.headers.get('Content-Type', 'audio/mpeg')
        return Response(generate(), content_type=content_type)

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

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
        
        if not ELEVENLABS_API_KEY:
            return jsonify({'success': False, 'message': 'ELEVENLABS_API_KEY not set on server'}), 400
        endpoint = f"{ELEVEN_API_BASE}/text-to-speech/{data['voice_id']}/stream"
        headers = {'xi-api-key': ELEVENLABS_API_KEY, 'Content-Type': 'application/json'}
        payload = {'text': data['text'], 'model_id': data.get('model_id', 'eleven_monolingual_v1')}
        if data.get('voice_settings'):
            payload['voice_settings'] = data['voice_settings']
        resp = requests.post(endpoint, headers=headers, json=payload, stream=True)
        if not resp.ok:
            return jsonify({'success': False, 'message': resp.text}), resp.status_code
        static_dir = (Path(__file__).resolve().parent.parent / 'static').resolve()
        audio_dir = static_dir / 'audio'
        audio_dir.mkdir(parents=True, exist_ok=True)
        filename = f"tts_{int(datetime.utcnow().timestamp())}_{data['voice_id']}.mp3"
        with open(audio_dir / filename, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        # build absolute url so frontend on different origin can stream audio directly
        base = request.host_url.rstrip('/')
        return jsonify({
            'success': True,
            'data': {
                'audio_id': filename[:-4],
                'audio_url': f"/audio/{filename}",
                'audio_url_absolute': f"{base}/audio/{filename}",
                'duration': None,
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
    """
    Clone a new voice in ElevenLabs.

    Supports two request types:
      • multipart/form-data  -> real cloning (needs audio files)
      • application/json     -> mock path retained for backward-compat tests
    """
    try:
        if not ELEVENLABS_API_KEY:
            return jsonify({'success': False, 'message': 'ELEVENLABS_API_KEY not set on server'}), 400

        # ------------------------------------------------------------------
        # Real cloning – multipart form with files
        # ------------------------------------------------------------------
        if request.content_type and 'multipart/form-data' in request.content_type:
            name = request.form.get('name')
            description = request.form.get('description', '')
            files = request.files.getlist('files') or []

            if not name:
                return jsonify({'success': False, 'message': 'Missing required field: name'}), 400
            if not files:
                return jsonify({'success': False, 'message': 'Please upload at least one audio file'}), 400

            # Build multipart payload for ElevenLabs
            upstream_files = []
            for f in files:
                # read may exhaust stream; try stream.read first else f.read
                try:
                    upstream_files.append(
                        ('files', (f.filename, f.stream.read(), f.mimetype or 'audio/mpeg'))
                    )
                except Exception:
                    upstream_files.append(
                        ('files', (f.filename, f.read(), f.mimetype or 'audio/mpeg'))
                    )

            data = {'name': name}
            if description:
                data['description'] = description

            r = requests.post(
                f"{ELEVEN_API_BASE}/voices/add",
                headers={'xi-api-key': ELEVENLABS_API_KEY},
                data=data,
                files=upstream_files,
                timeout=60,
            )

            if not r.ok:
                return jsonify({'success': False, 'message': r.text}), r.status_code

            payload = r.json()
            voice_id = payload.get('voice_id') or payload.get('id')

            return jsonify({
                'success': True,
                'data': {
                    'voice_id': voice_id,
                    'name': name,
                    'status': payload.get('status', 'created')
                }
            })

        # ------------------------------------------------------------------
        # Fallback JSON mock cloning (kept for earlier callers / tests)
        # ------------------------------------------------------------------
        data = request.get_json(silent=True) or {}

        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400

        voice_id = f"cloned_voice_{int(datetime.utcnow().timestamp())}"
        return jsonify({
            'success': True,
            'data': {
                'voice_id': voice_id,
                'name': data['name'],
                'description': data['description'],
                'status': 'processing'
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
