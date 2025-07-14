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
ENCODER_PATH = f"{MODEL_DIR}/encoder.pk
