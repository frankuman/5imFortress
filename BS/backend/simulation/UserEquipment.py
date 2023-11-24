import random
import math
import datetime
from BS.backend.datalogger import logger

from BS.backend.simulation import util

#import matlab.engine

# service classes for UEs, "class: Mbps"
ue_class = {
    0: 50,
    1: 3
}
ue_class_lambda = {
    0: 1/4000,
    1: 1/15
}

class user_equipment:
    MATLAB = 0
    RANDOM = 0
    epsilon = -1

    def __init__ (self, requested_bitrate, service_class, ue_id, starting_position, users, env):
        self.ue_id = ue_id
        self.requested_bitrate = requested_bitrate
        self.current_position = (starting_position[0], starting_position[1])
        self.h_m = starting_position[2]
        self.env = env
        self.service_class = service_class
        self.lambda_exp = ue_class_lambda[self.service_class]

        self.bs_id = None
        self.current_bs = {}
        
        self.wardrop_sigma = 0

        # number of users counted to this UE
        self.users = users
        self.original_users = users

    def connect_to_bs_id(self, bs_id):
        """
        Try to connect to BS with bs_id
        """
        available_bs = self.env.discover_bs(self.ue_id)
        data_rate = None
        current_time = datetime.datetime.now()

        time_string = current_time.strftime('%H:%M:%S')
        if bs_id not in available_bs:
            #No active BS with id, bs_id found
            print("[NO BASE STATION FOUND]: User ID %s has not found the selected base station (BS %s)" %(self.ue_id, bs_id))
            log = f"({time_string})-[NO BASE STATION FOUND]: User ID %s has not found the selected base station (BS %s)" %(self.ue_id, bs_id)
            #logger.log(bs_id,log)
            print(log)
            return False
        else:
            self.bs_id = bs_id
            data_rate = util.find_bs_by_id(bs_id).request_connection(self.ue_id, self.requested_bitrate, available_bs)
            #Save data rate allocated from BS to one user
            self.current_bs[bs_id] = data_rate
            #Update connected users for BS
            util.find_bs_by_id(bs_id).update_users(self.users)

        print("[CONNECTION_ESTABLISHED]: Users ID %s is now connected to base_station %s with a data rate of %s/%s Mbps" %(self.ue_id, bs_id, data_rate, self.requested_bitrate))
        log = f"({time_string})-[CONNECTION_ESTABLISHED]: Users ID %s is now connected to base_station %s with a data rate of %s/%s Mbps" %(self.ue_id, bs_id, data_rate, self.requested_bitrate)
        #logger.log(bs_id,log)
        print(log)
        return True

    def disconnect_from_bs(self, bs_id):
        """
        Try to disconnect from BS
        """
        if bs_id in self.current_bs:
            #Log
            current_time = datetime.datetime.now()
            time_string = current_time.strftime('%H:%M:%S')
            check = util.find_bs_by_id(bs_id).request_disconnection(self.ue_id)
            #Check if UE was disconnected from BS
            if check:
                print("[CONNECTION_TERMINATED]: Users ID %s is now disconnected from base_station %s" %(self.ue_id, bs_id))
                log = f"({time_string})-[CONNECTION_TERMINATED]: Users ID %s is now disconnected from base_station %s" %(self.ue_id, bs_id)
                #logger.log(bs_id,log)
                print(log)

                del self.current_bs[bs_id]
                self.bs_id = None
                return True
        return False

    def update_connection(self):
        """
        Update connection to BS
        """
        if len(self.current_bs) == 0:
            print("UE_ID: ", self.ue_id, " NO CURRENT BS")
            log = "UE_ID: ", self.ue_id, " NO CURRENT BS"
            #logger.log(self.ue_id,log)
            print(log)
            return False
        
        current_time = datetime.datetime.now()
        time_string = current_time.strftime('%H:%M:%S')
        available_bs = self.env.discover_bs(self.ue_id)

        if self.bs_id in available_bs:
            if self.current_bs[self.bs_id] == 0:
                print("UE_ID: ", self.ue_id, " NO CONNECTION TO BS: ", self.bs_id)
                log = f"({time_string})-UE_ID: ", self.ue_id, " NO CONNECTION TO BS: ", self.bs_id
                #logger.log(self.bs_id,log)
            
            data_rate = util.find_bs_by_id(self.bs_id).update_connection(self.ue_id, self.current_bs[self.bs_id], available_bs)
            self.current_bs[self.bs_id] = data_rate
            util.find_bs_by_id(self.bs_id).update_users(self.users)
            return True
        else:
            #In this case no current base station is anymore visible
            print("[BASE_STATION_LOST]: Users ID %s has not found their base station during connection update" %(self.ue_id))
            log = f"({time_string})-[BASE_STATION_LOST]: Users ID %s has not found their base station during connection update" %(self.ue_id)
            #logger.log(self.ue_id,log)

            self.disconnect_from_bs(self.bs_id)
            self.bs_id = None
            return False

    def initial_timestep(self):
        rsrp = self.env.discover_bs(self.ue_id)

        if self.ue_id in rsrp:
            if util.find_bs_by_id(self.ue_id).bs_type == "nr":
                self.connect_to_bs_id(self.ue_id)
        return True

    def next_timestep(self):
        rsrp = self.env.discover_bs(self.ue_id)

        if self.ue_id not in rsrp and self.ue_id in self.current_bs:
            del self.current_bs[self.ue_id]

        elif self.ue_id in rsrp and self.ue_id not in self.current_bs:
            if util.find_bs_by_id(self.ue_id).bs_type == "nr":
                self.connect_to_bs_id(self.ue_id)

        randomizer = random.randint(98,102)
        randomizer = randomizer / 100
        self.users = self.users*randomizer
        if self.users < self.original_users*0.8:
            self.users += self.original_users*0.05
        elif self.users > self.original_users*1.2:
            self.users -= self.original_users*0.05
        self.users = int(self.users)
        if self.bs_id is not None:
            util.find_bs_by_id(self.bs_id).update_users(self.users)
        return True

    def get_users(self):
        return self.users

    def reset(self):
        self.disconnect_from_bs(self.bs_id)
        del self.current_bs[self.bs_id]
        self.bs_id = None
        return True
