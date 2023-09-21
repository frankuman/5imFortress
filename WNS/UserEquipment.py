import random
import math

import WNS.util as util

#import matlab.engine

MAX_STEP = 2000

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

    def __init__ (self, requested_bitrate, service_class, ue_id, starting_position, env, speed, direction):
        self.ue_id = ue_id
        self.requested_bitrate = requested_bitrate
        self.current_position = (starting_position[0], starting_position[1])
        self.starting_position = (starting_position[0], starting_position[1])
        self.h_m = starting_position[2]
        self.env = env
        self.speed = speed #how much distance we made in one step
        self.direction = direction #in degrees from the x axis (0 horizontal movement, 90 vertical movement)
        self.old_position = (starting_position[0], starting_position[1])
        self.old_sevice_class = service_class
        self.service_class = service_class
        self.lambda_exp = ue_class_lambda[self.service_class]
        self.current_bs = {}
        self.actual_data_rate = 0
        self.last_action_t = 0

        self.bs_bitrate_allocation = {}
        self.wardrop_sigma = 0

           
    def move(self):
        if self.speed == 0:
            return self.current_position
        elif self.RANDOM == 1:
            return self.random_move()
        else:
            return self.line_move()

    def random_move(self):
        val = random.randint(1, 4)
        size = random.randint(0, MAX_STEP) 
        if val == 1: 
            if (self.current_position[0] + size) > 0 and (self.current_position[0] + size) < self.env.x_limit:
                self.current_position = (self.current_position[0] + size, self.current_position[1])
        elif val == 2: 
            if (self.current_position[0] - size) > 0 and (self.current_position[0] - size) < self.env.x_limit:
                self.current_position = (self.current_position[0] - size, self.current_position[1])
        elif val == 3: 
            if (self.current_position[1] + size) > 0 and (self.current_position[1] + size) < self.env.y_limit:
                self.current_position = (self.current_position[0], self.current_position[1] + size)
        else: 
            if (self.current_position[1] - size) > 0 and (self.current_position[1] - size) < self.env.y_limit:
                self.current_position = (self.current_position[0], self.current_position[1] - size)
        return self.current_position

    def line_move(self):
        new_x = self.current_position[0]+self.speed*math.cos(math.radians(self.direction))
        new_y = self.current_position[1]+self.speed*math.sin(math.radians(self.direction))
        
        #90-degrees bumping
        if new_x <= 0 and new_y <= 0:
            #bottom-left corner
            new_x = 0
            new_y = 0
            self.direction -= 180
        elif new_x <= 0 and new_y >= self.env.y_limit:
            #top-left corener
            new_x = 0
            new_y = self.env.y_limit
            self.direction += 180
        elif new_x >= self.env.x_limit and new_y >= self.env.y_limit:
            #top-right corner
            new_x = self.env.x_limit
            new_y = self.env.y_limit
            self.direction += 180
        elif new_x >= self.env.x_limit and new_y <= 0:
            #bottom-right corner
            new_x = self.env.x_limit
            new_y = 0
            self.direction -= 180
        elif new_x >= self.env.x_limit and self.direction != 90 and self.direction != 270:
            #bumping on the right margin
            new_x = self.env.x_limit
            if self.direction < 90 and self.direction > 0:
                self.direction += 90
            elif self.direction > 270 and self.direction < 360:
                self.direction -= 90
        elif new_x <= 0 and self.direction != 90 and self.direction != 270:
            #bumping on the left margin
            new_x = 0
            if self.direction > 180 and self.direction < 270:
                self.direction += 90
            elif self.direction > 90 and self.direction < 180:
                self.direction -= 90
        elif new_y <= 0 and self.direction != 0 and self.direction != 180:
            #bumping on the bottom margin
            new_y = 0
            self.direction = (360 - self.direction) % 360
        elif new_y >= self.env.y_limit and self.direction != 0 and self.direction != 180:
            #bumping on the top margin
            new_y = self.env.y_limit
            self.direction = (360 - self.direction) % 360

        self.direction = self.direction % 360
        self.current_position = (new_x, new_y)
        return self.current_position

    def do_action(self, t):
        '''
        if self.current_bs == None:
            self.connect_to_bs()
            return
        
        # compute the time spent in the service class
        #delta_t = (t+1) - (self.last_action_t+1)
        delta_t = 0
        if self.last_action_t > 0 and t + 1 - self.last_action_t > 40:
            if self.actual_data_rate < self.requested_bitrate/2:
                self.disconnect_from_bs()
                return
            else:
                self.disconnect_from_bs()
                self.connect_to_bs() 
                return
        elif self.last_action_t > 0:
            self.disconnect_from_bs()
            self.connect_to_bs()

        prob = 1 - (1 - math.exp(-self.lambda_exp * delta_t))
        if random.random() > prob:
            
            # it's time to change service class
            print("CHANGED SERVICE CLASS: User ID %s has now changed to class %s" %(self.ue_id, self.service_class))
            self.disconnect_from_bs()
            if self.service_class == 0:
                self.service_class = 1
            else:
                self.service_class = 0
            # apply new class parameters: requested bitrate, lambda, last action time
            self.requested_bitrate = ue_class[self.service_class]
            self.lambda_exp = ue_class_lambda[self.service_class]
            
            self.last_action_t = t + 1
            self.connect_to_bs()
        
        #just in scenario 1, otherwise comment
        else:
            self.disconnect_from_bs()
            self.connect_to_bs()
            #self.update_connection()
        '''
        return
    
    #deprecated
    def connect_to_bs_random(self):
        available_bs = self.env.discover_bs(self.ue_id)
        bs = None
        data_rate = None
        if len(available_bs) == 0:
            print("[NO BASE STATION FOUND]: User ID %s has not found any base station" %(self.ue_id))
            return
        elif len(available_bs) == 1:
            #this means there is only one available bs, so we have to connect to it
            #bs = list(available_bs.keys())[0]
            #self.actual_data_rate = util.find_bs_by_id(bs).request_connection(self.ue_id, self.requested_bitrate, available_bs)   
            bs , data_rate = self.env.request_connection(self.ue_id, self.requested_bitrate, available_bs)
            self.current_bs[bs] = data_rate
            self.actual_data_rate += data_rate

        else:
            if self.MATLAB == 1:
                #import function from matlab, in order to select the best action

                #eng = matlab.engine.start_matlab()
                #ret = eng.nomefunzione(arg1, arg2,...,argn)
                return
            else:
                bs, rsrp = random.choice(list(available_bs.items()))
                data_rate = util.find_bs_by_id(bs).request_connection(self.ue_id, self.requested_bitrate, available_bs)
                #self.current_bs, self.actual_data_rate = self.env.request_connection(self.ue_id, self.requested_bitrate, available_bs)
                self.current_bs[bs] = data_rate
                self.actual_data_rate += data_rate
        print("[CONNECTION_ESTABLISHED]: User ID %s is now connected to base_station %s with a data rate of %s/%s Mbps" %(self.ue_id, self.current_bs[bs], data_rate, self.requested_bitrate))
    
    #deprecated
    def connect_to_bs(self):
        available_bs = self.env.discover_bs(self.ue_id)
        bs = None
        data_rate = None
        if len(available_bs) == 0:
            print("[NO BASE STATION FOUND]: User ID %s has not found any base station" %(self.ue_id))
            return
        elif len(available_bs) == 1:
            #this means there is only one available bs, so we have to connect to it
            #bs = list(available_bs.keys())[0]
            #self.actual_data_rate = util.find_bs_by_id(bs).request_connection(self.ue_id, self.requested_bitrate, available_bs)   
            bs, data_rate = self.env.request_connection(self.ue_id, self.requested_bitrate, available_bs)
            self.current_bs[bs] = data_rate
            self.actual_data_rate += data_rate

        else:
            if self.MATLAB == 1:
                #import function from matlab, in order to select the best action

                #eng = matlab.engine.start_matlab()
                #ret = eng.nomefunzione(arg1, arg2,...,argn)
                return
            else:
                #bs = max(available_bs, key = available_bs.get)
                #self.actual_data_rate = util.find_bs_by_id(bs).request_connection(self.ue_id, self.requested_bitrate, available_bs)
                bs, data_rate = self.env.request_connection(self.ue_id, self.requested_bitrate, available_bs)
                self.current_bs[bs] = data_rate
                self.actual_data_rate += data_rate
                #self.current_bs = bs
        print("[CONNECTION_ESTABLISHED]: User ID %s is now connected to base_station %s with a data rate of %s/%s Mbps" %(self.ue_id, bs, data_rate, self.requested_bitrate))

    def connect_to_bs_id(self, bs_id):
        available_bs = self.env.discover_bs(self.ue_id)
        bs = None
        data_rate = None
        if bs_id not in available_bs:
            print("[NO BASE STATION FOUND]: User ID %s has not found the selected base station (BS %s)" %(self.ue_id, bs_id))
            return
        else:
            if bs_id not in self.bs_bitrate_allocation:
                print("[NO ALLOCATION FOR THIS BASE STATION FOUND]: User ID %s has not found any bitrate allocation for the selected base station (BS %s)" %(self.ue_id, bs_id))
                return
            elif self.bs_bitrate_allocation[bs_id] == 0:
                self.current_bs[bs_id] = 0
                return
            data_rate = util.find_bs_by_id(bs_id).request_connection(self.ue_id, self.bs_bitrate_allocation[bs_id], available_bs)
            self.current_bs[bs_id] = data_rate
            self.actual_data_rate += data_rate
        print("[CONNECTION_ESTABLISHED]: User ID %s is now connected to base_station %s with a data rate of %s/%s Mbps" %(self.ue_id, bs_id, data_rate, self.requested_bitrate))

    def connect_to_all_bs(self):
        for bs in self.env.bs_list:
            self.connect_to_bs_id(bs.bs_id)

    def disconnect_from_bs(self, bs_id):
        if bs_id in self.current_bs:
            util.find_bs_by_id(bs_id).request_disconnection(self.ue_id)
            #print("[CONNECTION_TERMINATED]: User ID %s is now disconnected from base_station %s" %(self.ue_id, bs_id))
            self.actual_data_rate -= self.current_bs[bs_id]
            del self.current_bs[bs_id]
        return
        
    def disconnect_from_all_bs(self):
        for bs in self.current_bs:
            util.find_bs_by_id(bs).request_disconnection(self.ue_id)
            #print("[CONNECTION_TERMINATED]: User ID %s is now disconnected from base_station %s" %(self.ue_id, bs))
        self.actual_data_rate = 0
        self.current_bs.clear()

    
    def update_connection(self):
        if len(self.current_bs) == 0:
            self.connect_to_bs()
            print("UE_ID: ", self.ue_id, " NO CURRENT BS")
            return

        available_bs = self.env.discover_bs(self.ue_id)
        #print("UE_ID: ", self.ue_id, " AVAILABLE BS: ", available_bs)
        #print(available_bs)
        if len(available_bs) == 0:
            #print("[NO BASE STATION FOUND]: User ID %s has not found any base station during connection update" %(self.ue_id))
            #print("UE_ID: ", self.ue_id, " NO BS AVAILABLE")
            return

        for elem in self.current_bs:
            if elem in available_bs:
                if self.current_bs[elem] == 0:
                    #print("UE_ID: ", self.ue_id, " NO CONNECTION TO BS", elem)
                    self.connect_to_bs_id(elem)
                    continue
                data_rate = util.find_bs_by_id(elem).update_connection(self.ue_id, self.bs_bitrate_allocation[elem], available_bs)
                
                self.actual_data_rate -= self.current_bs[elem]
                self.current_bs[elem] = data_rate
                self.actual_data_rate += self.current_bs[elem]

                #TODO update the connections according to the newly computed requested bitrates coming from the next_timestep() function
                '''
                if self.actual_data_rate < self.requested_bitrate:
                    print("[POOR BASE STATION]: User ID %s has a poor connection to its base station (actual data rate is %s/%s Mbps)" %(self.ue_id, self.actual_data_rate, self.requested_bitrate))
                    self.disconnect_from_bs(elem)
                    self.connect_to_bs()
                '''
                '''
                elif random.random() < self.epsilon:
                    print("[RANDOM DISCONNECTION]: User ID %s was randomly disconnected from its base station (actual data rate is %s/%s Mbps)" %(self.ue_id, self.actual_data_rate, self.requested_bitrate))
                    self.disconnect_from_bs()
                    self.connect_to_bs()
                '''
            else:
                #in this case no current base station is anymore visible
                #print("[BASE STATION LOST]: User ID %s has not found its base station during connection update" %(self.ue_id))
                self.disconnect_from_bs(elem)
                self.connect_to_bs()

            #print("[CONNECTION_UPDATE]: User ID %s has updated its connection to base_station %s with a data rate of %s/%s Mbps" %(self.ue_id, elem, self.current_bs[elem], self.bs_bitrate_allocation[elem]))

    def initial_timestep(self):
        rsrp = self.env.discover_bs(self.ue_id)
        '''bs = max(rsrp, key = rsrp.get)
        rsrp2 = {}
        for elem in rsrp:
            if elem != bs:
                rsrp2[elem] = rsrp[elem]
        bs2 = max(rsrp2, key = rsrp2.get)
        self.bs_bitrate_allocation[bs] = self.requested_bitrate/2
        self.bs_bitrate_allocation[bs2] = self.requested_bitrate/2
        '''
        n = len(rsrp)
        n1 = random.choice(list(rsrp))
        if self.ue_id == 1 or self.ue_id == 19:
            n1 = 0
        if 4 in rsrp and random.random() < 0.9:
            n1 = 4
        for elem in rsrp:
            if elem != n1:
                self.bs_bitrate_allocation[elem] = self.requested_bitrate/(n-1)
        if self.ue_id == 2:
                swap = self.bs_bitrate_allocation[0]*0.3
                self.bs_bitrate_allocation[0] = self.bs_bitrate_allocation[0]*0.7
                self.bs_bitrate_allocation[1] += swap
        for elem in rsrp:
            if elem not in self.bs_bitrate_allocation:
                #this means that it is the first time we encounter that base station
                self.bs_bitrate_allocation[elem] = 0
        
        #compute wardrop sigma
        self.wardrop_sigma = (self.env.wardrop_epsilon)/(2*self.env.sampling_time*self.env.wardrop_beta*self.requested_bitrate*(len(rsrp)-1)*len(self.env.ue_list))

        return

    def next_timestep(self):
        self.old_position = self.current_position
        self.move()

        #compute the next state variable x^i_p[k+1], considering the visible base stations
        rsrp = self.env.discover_bs(self.ue_id)

        #remove the old BSs that are out of visibility
        for elem in self.bs_bitrate_allocation:
            if elem not in rsrp:
                del self.bs_bitrate_allocation[elem]

        #add the new BSs 
        for elem in rsrp:
            if elem not in self.bs_bitrate_allocation:
                self.bs_bitrate_allocation[elem] = 0

        #core of the Wardrop algorithm
        for p in self.bs_bitrate_allocation:
            for q in self.bs_bitrate_allocation:
                if p != q:
                    bs_p = util.find_bs_by_id(p)
                    l_p = bs_p.compute_latency(self.ue_id)


                    bs_q = util.find_bs_by_id(q)
                    l_q = bs_q.compute_latency(self.ue_id)
                    
                    mu_pq = 1
                    if (l_p - l_q) < self.env.wardrop_epsilon or bs_q.allocated_bitrate >= bs_q.total_bitrate - (self.env.wardrop_epsilon/(2*self.env.wardrop_beta)):
                        mu_pq = 0
                    
                    mu_qp = 1
                    if (l_q - l_p) < self.env.wardrop_epsilon or bs_p.allocated_bitrate >= bs_p.total_bitrate - (self.env.wardrop_epsilon/(2*self.env.wardrop_beta)):
                        mu_qp = 0

                    r_pq = self.bs_bitrate_allocation[p]*mu_pq*self.wardrop_sigma
                    r_qp = self.bs_bitrate_allocation[q]*mu_qp*self.wardrop_sigma


                    self.bs_bitrate_allocation[p] += self.env.sampling_time * (r_qp - r_pq)          
        return


    def reset(self, t):
        self.disconnect_from_all_bs()
        self.actual_data_rate = 0
        self.current_position = self.starting_position
        #self.service_class = self.old_sevice_class
        #self.lambda_exp = ue_class_lambda[self.service_class]
        #self.requested_bitrate = ue_class[self.service_class]
        self.last_action_t = t

        

    
