from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import  logging
from networksecurity.entity.config_entity import DataIngetionConfig,DataValidationConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import TrainingPipelineConfig

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

        
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)
        
