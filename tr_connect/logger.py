import sys
import logging
import logging.handlers

# hack to hide messages if we log before setting up handler
logging.root.manager.emittedNoHandlerWarning = True

def setup_logging(filename=None, log_level=logging.DEBUG, max_size=100000, rollovers=3):
    """Easy to use logging - on reload it will not add multiple stdout handlers
    @param filename: full path to log file or None to indicate stdout
    """
    root_logger = logging.getLogger("")
    root_logger.setLevel(log_level)
    
    if filename:
      handler = logging.handlers.RotatingFileHandler(filename, 'a', max_size, rollovers)
    else:
      handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter("%(asctime)s:%(levelname)9s:%(name)20s: %(message)s")
    handler.setFormatter(formatter)

    add_handler = True
    for handle in root_logger.handlers:
        try:
            if handle.baseFilename == handler.baseFilename:
                add_handler = False
                duplicate_handler = handler.baseFilename
                break
        except AttributeError, e:
            # handlers without baseFilename
            root_logger.debug(str(e))
            pass
    
    if add_handler:
        root_logger.debug("Added handler to the root logger.")
        root_logger.addHandler(handler)
    else:
        root_logger.debug("Duplicate logging handler: %s" % (duplicate_handler,))
        

def main():
    """
    Example showing how to initialize the root logger and then declare additional loggers
    """
    
    # Initialze the Root logger.
    setup_logging()
    
    logger = logging.getLogger("loggerName")
    logger.setLevel(logging.DEBUG)
    
    # Use the logger
    logger.debug("First log message.")
    logger.debug("Second log message.")

if __name__ == "__main__":
    main()