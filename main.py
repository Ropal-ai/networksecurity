from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import  logging
from networksecurity.entity.config_entity import DataIngetionConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import ModelTrainerConfig

import sys 

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngetionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Initate the data ingestion config")
        dataingestion_artifact = data_ingestion.Initiate_data_ingestion()
        logging.info("Data ingestion completed")
        print(dataingestion_artifact)
        


        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestion_artifact,data_validation_config)
        logging.info("Initate the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("data validation completed")
        print(data_validation_artifact)


        logging.info("Initate the data trasnformation")
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        data_transfomration = DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact = data_transfomration.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("data transformation completed")

        logging.info("Model Training started")
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        logging.info("Model Training artifact created")

        
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)
        
