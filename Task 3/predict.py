import requests
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
from tensorflow.keras.models import load_model
import logging
from typing import Optional, Dict, Any, List, Union
from tensorflow.keras.losses import MeanSquaredError
import time
from datetime import datetime, timezone
import random
# Configure logging with debug level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('prediction_pipeline.log')
    ]
)
logger = logging.getLogger(__name__)

# Configuration
API_BASE_URL = "http://localhost:8000"
MODEL_DIR = "C:/Users/HP/Database-Prediction-Pipeline/models/models"
MODEL_PATH = f"{MODEL_DIR}/student_performance_nn_model.h5"
SCALER_PATH = f"{MODEL_DIR}/scaler.pkl"
ENCODER_PATH = f"{MODEL_DIR}/encoder.pkl"
FEATURE_NAMES_PATH = f"{MODEL_DIR}/feature_names.pkl"

class PredictionClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        logger.debug("PredictionClient initialized")

    def fetch_latest_student(self) -> Optional[Dict[str, Any]]:
        """Fetch the most recent student record with robust error handling"""
        try:
            logger.debug(f"Making request to {API_BASE_URL}/students")
            response = self.session.get(f"{API_BASE_URL}/students")
            response.raise_for_status()
            
            students = response.json()
            logger.debug(f"Received {len(students)} student records")
            
            if not students:
                logger.warning("No student data available")
                return None
            
            # Validate and filter students
            valid_students = []
            for student in students:
                if not isinstance(student, dict):
                    logger.warning(f"Invalid student record type: {type(student)}")
                    continue
                
                if 'student_id' not in student:
                    logger.warning("Student record missing student_id")
                    continue
                
                valid_students.append(student)
            
            if not valid_students:
                logger.error("No valid student records found")
                return None
            
            # Sort by creation date (newest first)
            valid_students.sort(
                key=lambda x: x.get("created_at", "1970-01-01T00:00:00"),
                reverse=True
            )
            
            latest_student = valid_students[0]
            logger.info(f"Selected student ID: {latest_student.get('student_id')}")
            logger.debug(f"Student data: {latest_student}")
            
            return latest_student
        
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching student: {str(e)}")
            return None

    def normalize_student_data(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize student data structure with defaults and validation"""
        logger.debug("Normalizing student data")
        
        if not student_data:
            logger.warning("Received empty student data")
            return {}
        
        # Set default values for all required fields
        normalized = {
            'student_id': student_data.get('student_id'),
            'gender': student_data.get('gender', 'unknown'),
            'race_ethnicity': student_data.get('race_ethnicity', 'unknown'),
            'parental_level_of_education': student_data.get('parental_level_of_education', 'unknown'),
            'lunch': student_data.get('lunch', 'standard'),
            'test_preparation': {'status': 'none'},  # Default value
            'exams': {}  # Default empty exam data
        }
        
        # Handle test preparation data
        if 'test_preparation' in student_data:
            if student_data['test_preparation'] is None:
                normalized['test_preparation'] = {'status': 'none'}
            elif isinstance(student_data['test_preparation'], dict):
                normalized['test_preparation'] = {
                    'status': student_data['test_preparation'].get('status', 'none')
                }
        
        # Handle exam data
        if 'exams' in student_data:
            exams = student_data['exams']
            if isinstance(exams, list) and exams:
                normalized['exams'] = exams[0] if isinstance(exams[0], dict) else {}
            elif isinstance(exams, dict):
                normalized['exams'] = exams
        
        logger.debug(f"Normalized data: {normalized}")
        return normalized
    
    def save_prediction(self, student_id: int, prediction: float, max_retries: int = 3) -> bool:
        """Save prediction to API with robust retry logic and comprehensive error handling.
        
        Args:
            student_id: ID of the student being predicted
            prediction: The prediction value to save
            max_retries: Maximum number of retry attempts
            
        Returns:
            bool: True if successful, False if all attempts failed
        """
        payload = {
            'student_id': student_id,
            'prediction': float(prediction),
            'prediction_date': datetime.now(timezone.utc).isoformat()  # Use UTC timezone
        }
        
        last_error = None  # Track the last error for final reporting
        
        for attempt in range(max_retries):
            try:
                logger.debug(f"Attempt {attempt + 1}/{max_retries}: Saving prediction for student {student_id}")
                
                response = self.session.post(
                    f"{API_BASE_URL}/predictions/",
                    json=payload,
                    timeout=(3.05, 10)  # Connect timeout 3.05s, read timeout 10s
                )
                
                # Successful creation (201) or update (200)
                if response.status_code in (200, 201):
                    logger.info(f"Successfully saved prediction for student {student_id}")
                    try:
                        response_data = response.json()
                        logger.debug(f"API response: {response_data}")
                    except ValueError:
                        logger.debug("API returned no JSON content")
                    return True
                
                # Handle specific error cases
                if 400 <= response.status_code < 500:
                    try:
                        error_detail = response.json().get('detail', response.text[:500])
                        last_error = f"Client error ({response.status_code}): {error_detail}"
                    except ValueError:
                        last_error = f"Client error ({response.status_code}): {response.text[:500]}"
                    logger.error(last_error)
                    
                    # Don't retry on client errors (4xx) except 429 (Too Many Requests)
                    if response.status_code != 429:
                        break
                
                elif response.status_code >= 500:
                    last_error = f"Server error ({response.status_code}): {response.text[:500]}"
                    logger.error(last_error)
                
            except requests.exceptions.Timeout as e:
                last_error = f"Request timeout: {str(e)}"
                logger.error(f"Timeout (attempt {attempt + 1}): {last_error}")
                
            except requests.exceptions.RequestException as e:
                last_error = f"Request failed: {str(e)}"
                logger.error(f"Network error (attempt {attempt + 1}): {last_error}")
            
            # Exponential backoff with jitter
            if attempt < max_retries - 1:
                sleep_time = min((2 ** attempt) + random.uniform(0, 1), 10)  # Max 10 seconds
                logger.debug(f"Waiting {sleep_time:.2f} seconds before retry...")
                time.sleep(sleep_time)
        
        logger.error(f"Failed to save prediction after {max_retries} attempts. Last error: {last_error}")
        return False

def save_prediction(self, student_id: int, prediction: float) -> bool:
    try:
        # Create the prediction payload
        payload = {
            'student_id': student_id,
            'prediction': prediction,
            'prediction_date': datetime.now().isoformat()
        }
        
        # Print out the request payload and headers
        print("Request Payload:", payload)
        print("Request Headers:", self.session.headers)
        
        # Send the request to the endpoint
        response = self.session.post(f"{API_BASE_URL}/predictions/", json=payload)
        
        # Check the response status code
        if response.status_code == 201:
            return True
        else:
            return False
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to save prediction: {str(e)}")
        return False

class NeuralNetworkPredictor:
    def __init__(self, api_client: PredictionClient):
        self.model = None
        self.scaler = None
        self.encoder = None
        self.feature_names = None
        self.api_client = api_client  # Store reference to API client
        self.load_artifacts()
        logger.debug("NeuralNetworkPredictor initialized")

    def load_artifacts(self):
        """Load all required model artifacts with validation"""
        try:
            logger.info("Loading model artifacts")
            
            logger.debug(f"Loading model from {MODEL_PATH}")
            self.model = load_model(MODEL_PATH, custom_objects={'mse': MeanSquaredError()})
            
            logger.debug(f"Loading scaler from {SCALER_PATH}")
            self.scaler = joblib.load(SCALER_PATH)
            
            logger.debug(f"Loading encoder from {ENCODER_PATH}")
            self.encoder = joblib.load(ENCODER_PATH)
            
            logger.debug(f"Loading feature names from {FEATURE_NAMES_PATH}")
            self.feature_names = joblib.load(FEATURE_NAMES_PATH)
            
            if None in [self.model, self.scaler, self.encoder, self.feature_names]:
                raise ValueError("One or more artifacts failed to load")
                
            logger.info("All model artifacts loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load model artifacts: {str(e)}")
            raise

    def prepare_features(self, student_data: Dict[str, Any]) -> np.ndarray:
        """Prepare student data for prediction with robust error handling"""
        logger.info("Preparing features for prediction")
        logger.debug(f"Input student data: {student_data}")
        
        try:
            if not student_data:
                raise ValueError("Empty student data provided")
            
            # Normalize the data structure first using the API client's method
            student_data = self.api_client.normalize_student_data(student_data)
            
            # Extract nested data with defaults
            exam_data = student_data.get('exams', {})
            prep_data = student_data.get('test_preparation', {})
            
            # Create DataFrame with expected feature names
            data = {
                'gender': [student_data.get('gender', 'unknown')],
                'race/ethnicity': [student_data.get('race_ethnicity', 'unknown')],
                'parental level of education': [student_data.get('parental_level_of_education', 'unknown')],
                'lunch': [student_data.get('lunch', 'standard')],
                'test preparation course': [prep_data.get('status', 'none')],
                'math score': [float(exam_data.get('math_score', 0))],
                'reading score': [float(exam_data.get('reading_score', 0))],
                'writing score': [float(exam_data.get('writing_score', 0))]
            }
            
            logger.debug(f"Constructed feature dict: {data}")
            
            # Create DataFrame ensuring correct column order
            df = pd.DataFrame(data, columns=self.feature_names)
            logger.debug(f"Feature DataFrame:\n{df}")
            
            # Preprocess numerical features
            numerical_cols = ['math score', 'reading score', 'writing score']
            scaled_numerical = self.scaler.transform(df[numerical_cols])
            logger.debug(f"Scaled numerical features: {scaled_numerical}")
            
            # Preprocess categorical features
            categorical_cols = ['gender', 'race/ethnicity', 'parental level of education', 
                              'lunch', 'test preparation course']
            encoded_categorical = self.encoder.transform(df[categorical_cols])
            
            if hasattr(encoded_categorical, 'toarray'):
                encoded_categorical = encoded_categorical.toarray()
            
            logger.debug(f"Encoded categorical features shape: {encoded_categorical.shape}")
            
            # Combine features
            features = np.concatenate([scaled_numerical, encoded_categorical], axis=1)
            logger.debug(f"Final feature array shape: {features.shape}")
            
            return features
            
        except Exception as e:
            logger.error(f"Feature preparation failed: {str(e)}", exc_info=True)
            raise

    def predict(self, features: np.ndarray) -> float:
        """Make prediction with validation and debugging"""
        try:
            if features is None:
                raise ValueError("No features provided for prediction")
            if features.size == 0:
                raise ValueError("Empty feature array provided")
                
            logger.info("Making prediction")
            logger.debug(f"Input features shape: {features.shape}")
            
            prediction = self.model.predict(features)
            logger.debug(f"Raw prediction output: {prediction}")
            
            if prediction is None or len(prediction) == 0:
                raise ValueError("Model returned empty prediction")
                
            result = float(prediction[0][0])
            logger.info(f"Prediction result: {result:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}", exc_info=True)
            raise

def main():
    try:
        logger.info("Starting prediction pipeline")
        
        # Initialize clients and predictor
        logger.debug("Initializing components")
        api_client = PredictionClient()
        predictor = NeuralNetworkPredictor(api_client)  # Pass the API client
        
        # Fetch latest student
        logger.debug("Fetching latest student record")
        student = api_client.fetch_latest_student()
        if not student:
            logger.error("No valid student data available for prediction")
            return
        
        logger.info(f"Processing student ID: {student.get('student_id')}")
        logger.debug(f"Raw student record: {student}")
    
        # Prepare and predict
        logger.debug("Preparing features")
        features = predictor.prepare_features(student)
        
        logger.debug("Making prediction")
        prediction = predictor.predict(features)
        
        # Save prediction
        logger.debug("Saving prediction results")
        if not api_client.save_prediction(student['student_id'], prediction):
            logger.error("Failed to save prediction to database")
        else:
            logger.info("Prediction pipeline completed successfully")
            
    except Exception as e:
        logger.error(f"Prediction pipeline failed: {str(e)}", exc_info=True)
        # Consider adding notification/alerting here

if __name__ == "__main__":
    main()
