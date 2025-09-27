import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting sematic-search-implementation-rag application")
    print("Hello from sematic-search-implementation-rag!")
    logger.info("Application completed successfully")


if __name__ == "__main__":
    logger.info("Running main.py as standalone script")
    main()
