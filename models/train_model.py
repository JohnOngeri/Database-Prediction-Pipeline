import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import joblib
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
DATA_PATH = r"C:\Users\HP\Database-Prediction-Pipeline\StudentsPerformance.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "student_performance_nn_model.h5")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "encoder.pkl")
RANDOM_STATE = 42
TEST_SIZE = 0.2
EPOCHS = 100
BATCH_SIZE = 32

def load_and_preprocess_data():
    """Load and preprocess the dataset"""
    logger.info("Loading dataset")
    df = pd.read_csv(DATA_PATH)
    
    # Define features and target
    categorical_features = ['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']
    numerical_features = ['math score', 'reading score', 'writing score']
    
    # Create target (average score)
    df['average_score'] = df[['math score', 'reading score', 'writing score']].mean(axis=1)
    
    X = df[categorical_features + numerical_features]
    y = df['average_score']
    
    return X, y, categorical_features, numerical_features

def create_preprocessor(categorical_features, numerical_features):
    """Create preprocessing pipeline"""
    logger.info("Creating preprocessing pipeline")
    
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    return preprocessor

def build_model(input_shape):
    """Build neural network model"""
    logger.info("Building neural network model")
    
    model = Sequential([
        Dense(64, activation='relu', input_shape=(input_shape,)),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dense(1)  # Regression output
    ])
    
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='mse',
        metrics=['mae']
    )
    
    return model

def save_artifacts(model, preprocessor, X_train):
    """Save model and preprocessing artifacts"""
    logger.info("Saving model and preprocessing artifacts")
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Save neural network model
    model.save(MODEL_PATH)
    
    # Save scaler for numerical features
    scaler = preprocessor.named_transformers_['num'].named_steps['scaler']
    joblib.dump(scaler, SCALER_PATH)
    
    # Save encoder for categorical features
    encoder = preprocessor.named_transformers_['cat'].named_steps['onehot']
    joblib.dump(encoder, ENCODER_PATH)
    
    # Save feature names for reference
    joblib.dump(list(X_train.columns), os.path.join(MODEL_DIR, "feature_names.pkl"))

def main():
    try:
        # Load and preprocess data
        X, y, categorical_features, numerical_features = load_and_preprocess_data()
        
        # Create preprocessing pipeline
        preprocessor = create_preprocessor(categorical_features, numerical_features)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )
        
        # Preprocess data
        X_train_preprocessed = preprocessor.fit_transform(X_train)
        X_test_preprocessed = preprocessor.transform(X_test)
        
        # Convert sparse matrix to dense if needed
        if hasattr(X_train_preprocessed, 'toarray'):
            X_train_preprocessed = X_train_preprocessed.toarray()
            X_test_preprocessed = X_test_preprocessed.toarray()
        
        # Build and train model
        model = build_model(X_train_preprocessed.shape[1])
        
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        logger.info("Training model")
        history = model.fit(
            X_train_preprocessed, y_train,
            validation_data=(X_test_preprocessed, y_test),
            epochs=EPOCHS,
            batch_size=BATCH_SIZE,
            callbacks=[early_stopping],
            verbose=1
        )
        
        # Save artifacts
        save_artifacts(model, preprocessor, X_train)
        
        logger.info(f"Model training complete. Artifacts saved to {MODEL_DIR}")
        
    except Exception as e:
        logger.error(f"Error during model training: {str(e)}")
        raise

if __name__ == "__main__":
    main()