def log(id,log):
    """Takes info, prints to correct document depending on ID
            log id 0 is ALWAYS serverlogs
      Args:
        log (string):
        id (int):  
    """
    log = log + "\n\n" 
    if id != 0:
        log_name = "HMI/frontend/datalogger/logs/bs_log_"+str(id)+".txt"
    else:
        log_name = "HMI/frontend/datalogger/logs/system_log.txt"
    with open(log_name, "a", encoding = "utf-8") as file:
        file.write(log) #Prints the logs into the file


def read_log(id):
    """Takes id, reads their doc, returns string
        log id 0 is ALWAYS serverlogs (pythonflask /)
    Args:
        id (int):  
    """
    if id != 0:
        log_name = "HMI/frontend/datalogger/logs/bs_log_"+str(id)+".txt"
    else:
        log_name = "HMI/frontend/datalogger/logs/system_log.txt"
    file = open(log_name, "r", encoding = "utf-8")
    log = file.read()
    log = log.replace("INFO:werkzeug:127.0.0.1 - - ","") #Remove some of the uninformal text
    log = log.replace("INFO:werkzeug:","")
    file.close()
    return log
