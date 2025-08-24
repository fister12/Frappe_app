# Copyright (c) 2024, Your Name and contributors
# For license information, please see license.txt

import frappe
import requests
import json
import base64
import os
from frappe import _

@frappe.whitelist()
def analyze_image(docname):
    """
    Analyze material image using Ollama AI model
    """
    try:
        # Get the Material Quality Inspection document
        doc = frappe.get_doc('Material Quality Inspection', docname)
        
        if not doc.material_image:
            frappe.throw(_("No image attached to analyze"))
        
        # Get the file path
        file_doc = frappe.get_doc("File", {"file_url": doc.material_image})
        file_path = file_doc.get_full_path()
        
        if not os.path.exists(file_path):
            frappe.throw(_("Image file not found on server"))
        
        # Read and encode image to base64
        with open(file_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Ollama API configuration
        ollama_url = frappe.get_site_config().get('ollama_url', 'http://localhost:11434/api/generate')
        
        # Construct the prompt for quality inspection
        prompt = """Analyze this image of a raw material for quality inspection. 
        Look for any visual defects such as:
        - Cracks or fractures
        - Discoloration or staining
        - Rust or corrosion
        - Impurities or foreign objects
        - Surface irregularities
        - Dimensional inconsistencies
        
        Based on your analysis, provide:
        1. A quality assessment: "Pass" or "Fail"
        2. A confidence score from 0.0 to 1.0
        3. Brief remarks explaining your findings
        
        Structure your response as a JSON object with keys 'assessment', 'score', and 'remarks'."""
        
        # Prepare the payload for Ollama API
        payload = {
            "model": "llava",
            "prompt": prompt,
            "images": [image_data],
            "stream": False,
            "format": "json"
        }
        
        # Make request to Ollama API
        response = requests.post(
            ollama_url,
            json=payload,
            timeout=60,  # 60 second timeout
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            frappe.throw(_("Error communicating with Ollama API: {0}").format(response.text))
        
        # Parse the response
        ollama_response = response.json()
        
        # Extract the response content
        if 'response' in ollama_response:
            try:
                # Parse the JSON response from the AI
                ai_result = json.loads(ollama_response['response'])
                
                # Extract values with fallbacks
                assessment = ai_result.get('assessment', 'Fail').strip()
                confidence_score = float(ai_result.get('score', 0.0))
                remarks = ai_result.get('remarks', 'AI analysis completed')
                
                # Ensure assessment is valid
                if assessment not in ['Pass', 'Fail']:
                    assessment = 'Fail'  # Default to Fail for safety
                
                # Ensure confidence score is within valid range
                confidence_score = max(0.0, min(1.0, confidence_score))
                
            except (json.JSONDecodeError, ValueError, TypeError) as e:
                frappe.log_error(f"Error parsing AI response: {e}")
                # Fallback values
                assessment = 'Fail'
                confidence_score = 0.0
                remarks = f"Error parsing AI response: {str(e)}"
        else:
            frappe.throw(_("Invalid response format from Ollama API"))
        
        # Update the document with AI results
        doc.db_set('status', assessment)
        doc.db_set('ai_confidence_score', confidence_score)
        doc.db_set('ai_remarks', remarks)
        
        # Commit the changes
        frappe.db.commit()
        
        return f"Analysis completed. Status: {assessment}, Confidence: {confidence_score:.2f}"
        
    except requests.exceptions.Timeout:
        frappe.throw(_("Timeout waiting for AI analysis. Please try again."))
    except requests.exceptions.ConnectionError:
        frappe.throw(_("Could not connect to Ollama API. Please ensure Ollama is running."))
    except Exception as e:
        frappe.log_error(f"Error in AI analysis: {str(e)}")
        frappe.throw(_("Error during AI analysis: {0}").format(str(e)))


@frappe.whitelist()
def get_inspection_stats():
    """
    Get statistics for quality inspections
    """
    stats = {}
    
    # Total inspections
    stats['total'] = frappe.db.count('Material Quality Inspection')
    
    # Status breakdown
    stats['pending'] = frappe.db.count('Material Quality Inspection', {'status': 'Pending'})
    stats['pass'] = frappe.db.count('Material Quality Inspection', {'status': 'Pass'})
    stats['fail'] = frappe.db.count('Material Quality Inspection', {'status': 'Fail'})
    
    # Average confidence score
    avg_confidence = frappe.db.sql("""
        SELECT AVG(ai_confidence_score) as avg_confidence
        FROM `tabMaterial Quality Inspection`
        WHERE ai_confidence_score IS NOT NULL AND ai_confidence_score > 0
    """)[0][0]
    
    stats['avg_confidence'] = round(float(avg_confidence or 0), 2)
    
    return stats


@frappe.whitelist()
def test_ollama_connection():
    """
    Test connection to Ollama API
    """
    try:
        ollama_url = frappe.get_site_config().get('ollama_url', 'http://localhost:11434/api/tags')
        
        # Test with a simple API call to list models
        response = requests.get(ollama_url.replace('/api/generate', '/api/tags'), timeout=10)
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            llava_available = any('llava' in model.get('name', '').lower() for model in models)
            
            return {
                'status': 'Connected',
                'models_available': len(models),
                'llava_available': llava_available
            }
        else:
            return {
                'status': 'Error',
                'message': f"HTTP {response.status_code}: {response.text}"
            }
            
    except requests.exceptions.ConnectionError:
        return {
            'status': 'Connection Error',
            'message': 'Could not connect to Ollama API'
        }
    except Exception as e:
        return {
            'status': 'Error',
            'message': str(e)
        }
