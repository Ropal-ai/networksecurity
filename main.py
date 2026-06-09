from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import  logging
from networksecurity.entity.config_entity import DataIngetionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

import sys 

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngetionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)

        logging.info("Initate the data ingestion config")

        dataingestion_artifact = data_ingestion.Initiate_data_ingestion()

        print(dataingestion_artifact)
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)
        
