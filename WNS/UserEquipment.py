import random
import math

from datalogger import logger


import WNS.util as util

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

        self.bs_bitrate_allocation = {}
        self.wardrop_sigma = 0

        # number of users counted to this UE
        self.users = users
        self.original_users = users


    def connect_to_bs_id(self, bs_id):
        available_bs = self.env.discover_bs(self.ue_id)
        data_rate = None

        if bs_id not in available_bs:
            print("[NO BASE STATION FOUND]: User ID %s has not found the selected base station (BS %s)" %(self.ue_id, bs_id))
            log = "[NO BASE STATION FOUND]: User ID %s has not found the selected base station (BS %s)" %(self.ue_id, bs_id)
            logger.log(bs_id,log)
            return False
        else:
            if bs_id not in self.bs_bitrate_allocation:
                print("[NO ALLOCATION FOR THIS BASE STATION FOUND]: User ID %s has not found any bitrate allocation for the selected base station (BS %s)" %(self.ue_id, bs_id))
                log = "[NO ALLOCATION FOR THIS BASE STATION FOUND]: User ID %s has not found any bitrate allocation for the selected base station (BS %s)" %(self.ue_id, bs_id)
                logger.log(bs_id,log)
                return False
            
            self.bs_id = bs_id
            data_rate = util.find_bs_by_id(bs_id).request_connection(self.ue_id, self.bs_bitrate_allocation[bs_id], available_bs)
            self.current_bs[bs_id] = data_rate
        print("[CONNECTION_ESTABLISHED]: Users ID %s is now connected to base_station %s with a data rate of %s/%s Mbps" %(self.ue_id, bs_id, data_rate, self.requested_bitrate))
        log = "[CONNECTION_ESTABLISHED]: Users ID %s is now connected to base_station %s with a data rate of %s/%s Mbps" %(self.ue_id, bs_id, data_rate, self.requested_bitrate)
        logger.log(bs_id,log)

        return True

    def disconnect_from_bs(self, bs_id):
        if bs_id in self.current_bs:
            util.find_bs_by_id(bs_id).request_disconnection(self.ue_id)
            print("[CONNECTION_TERMINATED]: Users ID %s is now disconnected from base_station %s" %(self.ue_id, bs_id))
            log = "[CONNECTION_TERMINATED]: Users ID %s is now disconnected from base_station %s" %(self.ue_id, bs_id)
            logger.log(bs_id,log)
            del self.current_bs[bs_id]
            del self.bs_bitrate_allocation[bs_id]
            return True
        return False
    
    def update_connection(self):
        if len(self.current_bs) == 0:
            print("UE_ID: ", self.ue_id, " NO CURRENT BS")
            log = "UE_ID: ", self.ue_id, " NO CURRENT BS"
            logger.log(self.ue_id,log)
            return False

        available_bs = self.env.discover_bs(self.ue_id)
        #print("UE_ID: ", self.ue_id, " AVAILABLE BS: ", available_bs)
        if len(self.bs_bitrate_allocation) == 0:
            print("[NO BASE STATION FOUND]: Users ID %s has not found any base station during connection update" %(self.ue_id))
            log = "[NO BASE STATION FOUND]: Users ID %s has not found any base station during connection update" %(self.ue_id)
            logger.log(self.ue_id,log)
            #print("UE_ID: ", self.ue_id, " NO BS AVAILABLE")
            return False

        if self.bs_id in available_bs:
            if self.current_bs[self.bs_id] == 0:
                print("UE_ID: ", self.ue_id, " NO CONNECTION TO BS: ", self.bs_id)
                log = "UE_ID: ", self.ue_id, " NO CONNECTION TO BS: ", self.bs_id
                logger.log(self.bs_id,log)
                self.connect_to_bs_id(self.bs_id)
                return False
            
            data_rate = util.find_bs_by_id(self.bs_id).update_connection(self.ue_id, self.current_bs[self.bs_id], available_bs)
            self.current_bs[self.bs_id] = data_rate
            return True
        else:
            #in this case no current base station is anymore visible
            print("[BASE_STATION_LOST]: Users ID %s has not found their base station during connection update" %(self.ue_id))
            log = "[BASE_STATION_LOST]: Users ID %s has not found their base station during connection update" %(self.ue_id)
            logger.log(self.ue_id,log)
            self.disconnect_from_bs(self.bs_id)
            #print("[CONNECTION_UPDATE]: User ID %s has updated its connection to base_station %s with a data rate of %s/%s Mbps" %(self.ue_id, elem, self.current_bs[elem], self.bs_bitrate_allocation[elem]))
            return False
        
    def initial_timestep(self):
        rsrp = self.env.discover_bs(self.ue_id)

        # for elem in rsrp:
        #     if util.find_bs_by_id(elem).bs_type == "nr":
        #         path_loss = util.compute_path_loss_cost_hata(self, util.find_bs_by_id(elem), self.env)
        #         if path_loss < 100:
        #             self.bs_bitrate_allocation[elem] = self.requested_bitrate/(path_loss/(path_loss*0.9))
        #     # self.bs_bitrate_allocation[elem] = self.requested_bitrate/(rsrp[elem]/(rsrp[elem]*0.9))

        # #auto connect
        # if len(self.bs_bitrate_allocation) != 0:
        #     self.connect_to_bs_id(list(self.bs_bitrate_allocation.keys())[0])

        if self.ue_id in rsrp:
            if util.find_bs_by_id(self.ue_id).bs_type == "nr":
                path_loss = util.compute_path_loss_cost_hata(self, util.find_bs_by_id(self.ue_id), self.env)
                self.bs_bitrate_allocation[self.ue_id] = self.requested_bitrate/(path_loss/(path_loss*0.9))
                self.connect_to_bs_id(self.ue_id)

        #compute wardrop sigma
        #self.wardrop_sigma = (self.env.wardrop_epsilon)/(2*self.env.sampling_time*self.env.wardrop_beta*self.requested_bitrate*(len(rsrp)-1)*len(self.env.ue_list))

        return True

    def next_timestep(self):
        rsrp = self.env.discover_bs(self.ue_id)

        if self.ue_id not in rsrp and self.ue_id in self.bs_bitrate_allocation:
            del self.bs_bitrate_allocation[self.ue_id]
            if self.ue_id in self.current_bs:
                del self.current_bs[self.ue_id]
        elif self.ue_id in rsrp and self.ue_id not in self.bs_bitrate_allocation:
            if util.find_bs_by_id(self.ue_id).bs_type == "nr":
                path_loss = util.compute_path_loss_cost_hata(self, util.find_bs_by_id(self.ue_id), self.env)
                self.bs_bitrate_allocation[self.ue_id] = self.requested_bitrate/(path_loss/(path_loss*0.9))
                self.connect_to_bs_id(self.ue_id)

        # #remove the old BSs that are out of visibility
        # for elem in list(self.bs_bitrate_allocation):
        #     if elem not in rsrp:
        #         del self.bs_bitrate_allocation[elem]

        # #add the new BSs 
        # for elem in rsrp:
        #     if util.find_bs_by_id(elem).bs_type == "nr":
        #         if elem not in self.bs_bitrate_allocation:
        #             path_loss = util.compute_path_loss_cost_hata(self, util.find_bs_by_id(elem), self.env)
        #             if path_loss < 100:
        #                 self.bs_bitrate_allocation[elem] = self.requested_bitrate/(path_loss/(path_loss*0.9))
        #             # self.bs_bitrate_allocation[elem] = self.requested_bitrate/(rsrp[elem]/(rsrp[elem]*0.9))

        # #auto connect
        # if len(self.bs_bitrate_allocation) == 0 and len(self.current_bs) != 0:
        #     del self.current_bs[self.bs_id]
        # elif len(self.current_bs) == 0 and len(self.bs_bitrate_allocation) != 0:
        #     self.connect_to_bs_id(list(self.bs_bitrate_allocation.keys())[0])
        
        randomizer = random.randint(98,102)
        randomizer = randomizer / 100
        self.users = self.users*randomizer
        if self.users < self.original_users*0.8:
            self.users += self.original_users*0.05
        elif self.users > self.original_users*1.2:
            self.users -= self.original_users*0.05
        self.users = int(self.users)
                
        return True

    def get_users(self):
        # if len(self.current_bs) == 0:
        #     return 0
        return self.users

    def reset(self):
        self.disconnect_from_bs(self.bs_id)
        del self.current_bs[self.bs_id]
        del self.bs_bitrate_allocation[self.bs_id]
        return True
