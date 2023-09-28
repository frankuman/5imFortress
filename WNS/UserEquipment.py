import random
import math

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


    def connect_to_bs_id(self, bs_id):
        available_bs = self.env.discover_bs(self.ue_id)
        data_rate = None

        if bs_id not in available_bs:
            print("[NO BASE STATION FOUND]: User ID %s has not found the selected base station (BS %s)" %(self.ue_id, bs_id))
            return False
        else:
            if bs_id not in self.bs_bitrate_allocation:
                print("[NO ALLOCATION FOR THIS BASE STATION FOUND]: User ID %s has not found any bitrate allocation for the selected base station (BS %s)" %(self.ue_id, bs_id))
                return False
            
            self.bs_id = bs_id
            data_rate = util.find_bs_by_id(bs_id).request_connection(self.ue_id, self.bs_bitrate_allocation[bs_id], available_bs)
            self.current_bs[bs_id] = data_rate
        print("[CONNECTION_ESTABLISHED]: User ID %s is now connected to base_station %s with a data rate of %s/%s Mbps" %(self.ue_id, bs_id, data_rate, self.requested_bitrate))
        return True

    def disconnect_from_bs(self, bs_id):
        if bs_id in self.current_bs:
            util.find_bs_by_id(bs_id).request_disconnection(self.ue_id)
            print("[CONNECTION_TERMINATED]: User ID %s is now disconnected from base_station %s" %(self.ue_id, bs_id))
            del self.current_bs[bs_id]
            del self.bs_bitrate_allocation[bs_id]
            return True
        return False
    
    def update_connection(self):
        if len(self.current_bs) == 0:
            print("UE_ID: ", self.ue_id, " NO CURRENT BS")
            return False

        available_bs = self.env.discover_bs(self.ue_id)
        #print("UE_ID: ", self.ue_id, " AVAILABLE BS: ", available_bs)
        if len(self.bs_bitrate_allocation) == 0:
            print("[NO BASE STATION FOUND]: User ID %s has not found any base station during connection update" %(self.ue_id))
            #print("UE_ID: ", self.ue_id, " NO BS AVAILABLE")
            return False

        if self.bs_id in available_bs:
            if self.current_bs[self.bs_id] == 0:
                print("UE_ID: ", self.ue_id, " NO CONNECTION TO BS: ", self.bs_id)
                self.connect_to_bs_id(self.bs_id)
                return False
            
            data_rate = util.find_bs_by_id(self.bs_id).update_connection(self.ue_id, self.bs_bitrate_allocation[self.bs_id], available_bs)
            self.current_bs[self.bs_id] = data_rate
            return True
        else:
            #in this case no current base station is anymore visible
            print("[BASE STATION LOST]: User ID %s has not found its base station during connection update" %(self.ue_id))
            self.disconnect_from_bs(self.bs_id)
            #print("[CONNECTION_UPDATE]: User ID %s has updated its connection to base_station %s with a data rate of %s/%s Mbps" %(self.ue_id, elem, self.current_bs[elem], self.bs_bitrate_allocation[elem]))
            return False
        
    def initial_timestep(self):
        rsrp = self.env.discover_bs(self.ue_id)

        for elem in rsrp:
            if util.find_bs_by_id(elem).bs_type == "nr":
                path_loss = util.compute_path_loss_cost_hata(self, util.find_bs_by_id(elem), self.env)
                if path_loss < 100:
                    self.bs_bitrate_allocation[elem] = self.requested_bitrate/(path_loss/(path_loss*0.9))

        #auto connect
        if len(self.bs_bitrate_allocation) != 0:
            self.connect_to_bs_id(list(self.bs_bitrate_allocation.keys())[0])
        randomizer = random.randint(98,102)
        randomizer = randomizer / 100
        self.users = self.users*randomizer
        if self.users < 1000:
            self.users = self.users*1.5

        #compute wardrop sigma
        #self.wardrop_sigma = (self.env.wardrop_epsilon)/(2*self.env.sampling_time*self.env.wardrop_beta*self.requested_bitrate*(len(rsrp)-1)*len(self.env.ue_list))

        return True

    def next_timestep(self):
        rsrp = self.env.discover_bs(self.ue_id)

        #remove the old BSs that are out of visibility
        for elem in list(self.bs_bitrate_allocation):
            if elem not in rsrp:
                del self.bs_bitrate_allocation[elem]

        #add the new BSs 
        for elem in rsrp:
            if util.find_bs_by_id(elem).bs_type == "nr":
                if elem not in self.bs_bitrate_allocation:
                    path_loss = util.compute_path_loss_cost_hata(self, util.find_bs_by_id(elem), self.env)
                    if path_loss < 100:
                        self.bs_bitrate_allocation[elem] = self.requested_bitrate/(path_loss/(path_loss*0.9))

        #auto connect
        if len(self.bs_bitrate_allocation) == 0 and len(self.current_bs) != 0:
            del self.current_bs[self.bs_id]
        elif len(self.current_bs) == 0 and len(self.bs_bitrate_allocation) != 0:
            self.connect_to_bs_id(list(self.bs_bitrate_allocation.keys())[0])
        
        randomizer = random.randint(98,102)
        randomizer = randomizer / 100
        self.users = self.users*randomizer
        if self.users < 1000:
            self.users = self.users*1.5
        

        # #core of the Wardrop algorithm
        # for p in self.bs_bitrate_allocation:
        #     for q in self.bs_bitrate_allocation:
        #         if p != q:
        #             bs_p = util.find_bs_by_id(p)
        #             l_p = bs_p.compute_latency(self.ue_id)


        #             bs_q = util.find_bs_by_id(q)
        #             l_q = bs_q.compute_latency(self.ue_id)
                    
        #             mu_pq = 1
        #             if (l_p - l_q) < self.env.wardrop_epsilon or bs_q.allocated_bitrate >= bs_q.total_bitrate - (self.env.wardrop_epsilon/(2*self.env.wardrop_beta)):
        #                 mu_pq = 0
                    
        #             mu_qp = 1
        #             if (l_q - l_p) < self.env.wardrop_epsilon or bs_p.allocated_bitrate >= bs_p.total_bitrate - (self.env.wardrop_epsilon/(2*self.env.wardrop_beta)):
        #                 mu_qp = 0

        #             r_pq = self.bs_bitrate_allocation[p]*mu_pq*self.wardrop_sigma
        #             r_qp = self.bs_bitrate_allocation[q]*mu_qp*self.wardrop_sigma


        #             self.bs_bitrate_allocation[p] += self.env.sampling_time * (r_qp - r_pq)          
        return True


    def reset(self):
        self.disconnect_from_bs(self.bs_id)
        del self.current_bs[self.bs_id]
        return True
