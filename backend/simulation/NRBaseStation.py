import math
import random
from scipy import constants
from backend.simulation import environment
from frontend.datalogger import logger
from backend.simulation import util
import datetime
#Table 5.3.3-1: Minimum guardband [kHz] (FR1) and Table: 5.3.3-2: Minimum guardband [kHz] (FR2), 3GPPP 38.104
#number of prb depending on the numerology (0,1,2,3), on the frequency range (FR1, FR2) and on the base station bandwidth
NRbandwidth_prb_lookup = {
    0:[{
        5:25,
        10:52,
        15:79,
        20:106,
        25:133,
        30:160,
        40:216,
        50:270
    }, None],
    1:[{
        5:11,
        10:24,
        15:38,
        20:51,
        25:65,
        30:78,
        40:106,
        50:133,
        60:162,
        70:189,
        80:217,
        90:245,
        100:273
    }, None],
    2:[{
        10:11,
        15:18,
        20:24,
        25:31,
        30:38,
        40:51,
        50:65,
        60:79,
        70:93,
        80:107,
        90:121,
        100:135
    },
    {
        50:66,
        100:132,
        200:264
    }],
    3:[None, 
    {
        50:32,
        100:66,
        200:132,
        400:264
    }]
}

bs_status = {
    1: "UP",
    2:"DOWN"
}

class NRBaseStation:
    bs_type = "nr"

    def __init__(self, bs_id, total_prb, prb_bandwidth_size, number_subcarriers, numerology, antenna_power, antenna_gain, feeder_loss, carrier_frequency, total_bitrate, antenna_nr, position, env):
        if position[2] > 200 or position[2] < 30:
            raise Exception("COST-HATA model requires BS height in [30, 200]m")

        if (carrier_frequency < 150 or carrier_frequency > 2000):
            raise Exception("your results may be incorrect because your carrier frequency is outside the boundaries of COST-HATA path loss model")

        self.prb_bandwidth_size = prb_bandwidth_size
        self.total_prb = total_prb
        self.total_bitrate = total_bitrate #Mbps
        self.allocated_prb = 0
        self.allocated_bitrate = 0
        self.antenna_power = antenna_power
        if antenna_gain == 0:
            self.antenna_gain = 1
        else:
            self.antenna_gain = antenna_gain
        self.feeder_loss = feeder_loss
        self.bs_id = bs_id
        self.carrier_frequency = carrier_frequency
        self.fr = -1
        if (carrier_frequency <= 6000):  #below 6GHz
            self.fr = 0
        elif (carrier_frequency >= 24250 and carrier_frequency <= 52600): #between 24.25GHz and 52.6GHz
            self.fr = 1
        self.position = (position[0],position[1])
        self.h_b = position[2]
        self.number_subcarriers = number_subcarriers
        self.env = env
        self.numerology = numerology
        self.ue_pb_allocation = {}
        self.ue_bitrate_allocation = {}

        #Tower status for ON/OFF
        self.status = bs_status[1]

        #Tower antennas
        self.nr_antennas = antenna_nr
        self.antennas = [bs_status[1]] * self.nr_antennas

        self.ue_id = None
        self.connected_users = 0


    def bs_status(self):
        """
        Return status of base station (UP/DOWN).
        """
        return self.status

    def bs_change_status(self):
        """
        Change status of base station, change between UP or DOWN.
        If change from UP -> DOWN, then disconnect all ue connected to base station
        and remove base station from bs_list in environment.
        If change from DOWN -> UP, then add base station to bs_list again.
        """
        current_time = datetime.datetime.now()
        time_string = current_time.strftime('%H:%M:%S')

        if self.status == bs_status[1]: # status is UP
            print("[BASE_STATION_SHUTDOWN]: BASE STATION ID %s IS NOW DOWN" %(self.bs_id))
            log = f"({time_string})-[BASE_STATION_SHUTDOWN]: BASE STATION ID %s IS NOW DOWN" %(self.bs_id)
            logger.log(self.bs_id, log)
            environment.wireless_environment.bs_list.remove(self)
            self.status = bs_status[2] # change status to DOWN
            self.antennas = [bs_status[2]] * self.nr_antennas
            self.reset()
            
        else: # status is DOWN
            print("[BASE_STATION_POWER_UP]: BASE STATION ID %s IS NOW UP" %(self.bs_id))
            log = f"({time_string})-[BASE_STATION_POWER_UP]: BASE STATION ID %s IS NOW UP" %(self.bs_id)
            logger.log(self.bs_id, log)
            environment.wireless_environment.bs_list.insert(self.bs_id, environment.wireless_environment.all_bs_list[self.bs_id])
            self.status = bs_status[1] # change status to UP
            self.antennas = [bs_status[1]] * self.nr_antennas
        return self.status

    def change_antenna_status(self, index):
        status = self.antennas[index]
        if status == "UP":
            status = "DOWN"
            self.antennas[index] = status
        else: #status is DOWN for this antenna
            status = "UP"
            self.antennas[index] = status
        return status

    def change_gain(self, gain):
        self.antenna_gain = gain
        return True
    
    def compute_bitrate(self):
        self.allocated_bitrate = self.ue_bitrate_allocation[self.ue_id]*self.connected_users
        self.allocated_bitrate = self.allocated_bitrate*(((101-self.antenna_gain)/100))
        self.allocated_bitrate = int(self.allocated_bitrate)
        return True

    
    def compute_nprb_NR(self, data_rate, rsrp):
        #compute SINR
        interference = 0

        for elem in rsrp:
            if elem != self.bs_id and util.find_bs_by_id(elem).bs_type != "sat" and util.find_bs_by_id(elem).carrier_frequency == self.carrier_frequency:
                total, used = util.find_bs_by_id(elem).get_state()
                interference = interference + (10 ** (rsrp[elem]/10))*(used/total)*(self.allocated_prb/self.total_prb)

        #thermal noise is computed as k_b*T*delta_f, where k_b is the Boltzmann's constant, T is the temperature in kelvin and delta_f is the bandwidth
        #thermal_noise = constants.Boltzmann*293.15*list(NRbandwidth_prb_lookup[self.numerology][self.fr].keys())[list(NRbandwidth_prb_lookup[self.numerology][self.fr].values()).index(self.total_prb / (10 * 2**self.numerology))]*1000000*(self.compute_rbur()+0.001)
        thermal_noise = constants.Boltzmann*293.15*15*(2**self.numerology)*1000 # delta_F = 15*2^mu KHz each subcarrier since we are considering measurements at subcarrirer level (like RSRP)
        sinr = (10**(rsrp[self.bs_id]/10))/(thermal_noise + interference)
        
        r = self.prb_bandwidth_size*1000*math.log2(1+sinr) #bandwidth is in kHz
        #based on the numerology choosen and considered the frame duration of 10ms, we transmit 1ms for mu = 0, 0.5ms for mu = 1, 0.25ms for mu = 2, 0.125ms for mu = 3 for each PRB each 10ms
        #print(r)
        r = r / (10 * (2**self.numerology))
        #print(r)
        N_prb = math.ceil(data_rate*1000000 / r) #data rate is in Mbps
        return N_prb, r

    #this method will be called by an UE that tries to connect to this BS.
    #the return value will be the actual bandwidth assigned to the user
    def request_connection(self, ue_id, data_rate, rsrp):

        N_prb, r = self.compute_nprb_NR(data_rate, rsrp)
        self.ue_id = ue_id

        #check if there is enough bitrate, if not then do not allocate the user
        if self.total_bitrate - self.allocated_bitrate < r*N_prb/1000000:
            dr = self.total_bitrate - self.allocated_bitrate
            N_prb, r = self.compute_nprb_NR(dr, rsrp)

        #check if there are enough PRBs
        if self.total_prb - self.allocated_prb <= N_prb:
            N_prb = self.total_prb - self.allocated_prb

        if ue_id not in self.ue_pb_allocation:
            self.ue_pb_allocation[ue_id] = N_prb
            self.allocated_prb += N_prb
        else:
            self.allocated_prb -= self.ue_pb_allocation[ue_id]
            self.ue_pb_allocation[ue_id] = N_prb
            self.allocated_prb += N_prb 

        if ue_id not in self.ue_bitrate_allocation:
            self.ue_bitrate_allocation[ue_id] = r * N_prb / 1000000  
            self.allocated_bitrate += r * N_prb / 1000000
        else:
            # self.allocated_bitrate -= self.ue_bitrate_allocation[ue_id] #It shouldn't trigger this
            self.ue_bitrate_allocation[ue_id] = r * N_prb / 1000000
            self.allocated_bitrate += r * N_prb / 1000000
            current_time = datetime.datetime.now()

            time_string = current_time.strftime('%H:%M:%S')
            print("NEW BITRATE [debug]",self.allocated_bitrate,r,N_prb)
            log = str(f"({time_string})-[NEW_BITRATE(debugger)]"+self.allocated_bitrate+r+N_prb)
            logger.log(ue_id,log)

        self.connected_users = util.find_ue_by_id(self.ue_id).users
        self.compute_bitrate()

        return r*N_prb/1000000 #we want a data rate in Mbps, not in bps

    def request_disconnection(self, ue_id):
        N_prb = self.ue_pb_allocation[ue_id]
        self.allocated_prb -= N_prb
        del self.ue_pb_allocation[ue_id]
        del self.ue_bitrate_allocation[ue_id]
        self.allocated_bitrate = 0
        self.connected_users = 0
        self.ue_id = None


    def update_connection(self, ue_id, data_rate, rsrp):

        N_prb, r = self.compute_nprb_NR(data_rate, rsrp)
        diff = N_prb - self.ue_pb_allocation[ue_id]

        #check before if there is enough bitrate
        if  diff >= 0 and self.total_bitrate > self.allocated_bitrate and self.total_bitrate - self.allocated_bitrate < diff * r / 1000000:
            #print("BS_ID", self.bs_id, "UE_ID: ", ue_id ,"NO MORE BITRATE", self.total_bitrate - self.allocated_bitrate, diff * r / 1000000)
            #return self.ue_pb_allocation[ue_id] * r / 1000000
            dr = self.total_bitrate - self.allocated_bitrate
            N_prb, r = self.compute_nprb_NR(self.ue_bitrate_allocation[ue_id]+dr, rsrp)
            diff = N_prb - self.ue_pb_allocation[ue_id]


        if self.total_prb - self.allocated_prb >= diff:
            #there is the place for more PRB allocation (or less if diff is negative)
            self.allocated_prb += diff
            self.ue_pb_allocation[ue_id] += diff

            self.allocated_bitrate += diff * r / 1000000
            self.ue_bitrate_allocation[ue_id] += diff * r / 1000000
        else:
            #there is no room for more PRB allocation
            diff = self.total_prb - self.allocated_prb
            self.allocated_prb += diff
            self.ue_pb_allocation[ue_id] += diff

            self.allocated_bitrate += diff * r / 1000000
            self.ue_bitrate_allocation[ue_id] += diff * r / 1000000

        N_prb = self.ue_pb_allocation[ue_id]
        self.compute_bitrate()
        return N_prb*r/1000000 #remember that we want the result in Mbps 

    #things to do before moving to the next timestep
    def next_timestep(self):
        if self.ue_id is not None:
            self.compute_bitrate()

    def get_connected_ue(self):
        return self.ue_id
    
    def update_users(self, users):
        self.connected_users = users
        self.connected_users = self.connected_users*(1-0.25*self.antennas.count("DOWN"))
        return True
    
    def get_connected_users(self):
        return self.connected_users

    def reset(self):
        N_prb = self.ue_pb_allocation[self.ue_id]
        self.allocated_prb -= N_prb
        del self.ue_pb_allocation[self.ue_id]
        del self.ue_bitrate_allocation[self.ue_id]
        self.allocated_bitrate = 0
        self.connected_users = 0
        self.ue_id = None
