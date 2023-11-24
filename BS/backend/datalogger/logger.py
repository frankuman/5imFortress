#This file is currently unused
def log(id,log):
    """Takes info, prints to correct document depending on ID
            log id 0 is ALWAYS serverlogs
      Args:
        log (string):
        id (int):  
    """
    log = log + "\n\n"
    if id != 0:
        log_name = "BS/backend/datalogger/logs/bs_log_"+str(id)+".txt"
    else:
        log_name = "BS/backend/datalogger/logs/system_log.txt"
    with open(log_name, "a", encoding = "utf-8") as file:
        file.write(log)


def read_log(id):
    """Takes id, reads their doc, returns string
        log id 0 is ALWAYS serverlogs (pythonflask /)
    Args:
        id (int):  
    """
    if id != 0:
        log_name = "BS/backend/datalogger/logs/bs_log_"+str(id)+".txt"
    else:
        log_name = "BS/backend/datalogger/logs/system_log.txt"
    file = open(log_name, "r", encoding = "utf-8")
    log = file.read()
    log = log.replace("INFO:werkzeug:127.0.0.1 - - ","")
    log = log.replace("INFO:werkzeug:","")
    file.close()
    return log
