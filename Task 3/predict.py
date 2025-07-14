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

