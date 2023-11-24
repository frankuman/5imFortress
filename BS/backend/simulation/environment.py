from BS.backend.simulation import NRBaseStation as NRbs
from BS.backend.simulation import UserEquipment as ue
from BS.backend.simulation import Satellite as SATbs
from BS.backend.simulation import util

class wireless_environment:
    #List of all active BS in environment
    bs_list = []
    #List of all BS active/inactive in environment
    all_bs_list = []
    #List of all UE in environment
    ue_list = []
    x_limit = None
    y_limit = None
    env_type = util.EnvType.URBAN

    def __init__(self, n, m = None):
        if m is not None:
            self.y_limit = m
        else:
            self.y_limit = n
        self.x_limit = n

    def insert_ue(self, ue_class, starting_position, users):
        if (starting_position[2] > 10 or starting_position[2] < 1):
            raise Exception("COST-HATA model requires UE height in [1,10]m")
        elif ue_class not in ue.ue_class:
            raise Exception("Invalid service class for the UE, available service classes are: %s" %(ue.ue_class.keys()))
        ue_id = -1

        if None in self.ue_list:
            ue_id = self.ue_list.index(None)
        else:
            ue_id = len(self.ue_list)

        new_ue = ue.user_equipment(ue.ue_class[ue_class], ue_class, ue_id, starting_position, users, self)

        if (ue_id == len(self.ue_list)):
            self.ue_list.append(new_ue)
        else:
            self.ue_list[ue_id] = new_ue
        return new_ue.ue_id

    def remove_ue(self, ue_id):
        self.ue_list[ue_id] = None

    def place_SAT_base_station(self, total_bitrate, position):       
        new_bs = SATbs.Satellite(len(self.bs_list), total_bitrate, position, self)

        self.bs_list.append(new_bs)
        self.all_bs_list.append(new_bs)
        return new_bs.bs_id

    def place_NR_base_station(self, position, carrier_frequency, numerology, antenna_power, antenna_gain, feeder_loss, available_bandwidth, total_bitrate, antenna_nr):
        #check if the bandwith is in line with the specified numerology and specified carrier frequency
        fr = -1
        if (carrier_frequency <= 6000):  #below 6GHz
            fr = 0
        elif (carrier_frequency >= 24250 and carrier_frequency <= 52600): #between 24.25GHz and 52.6GHz
            fr = 1
        else:
            raise Exception("NR frequency outside admissible ranges")

        if available_bandwidth in NRbs.NRbandwidth_prb_lookup[numerology][fr]:
            prb_size = 15*(2**numerology)*12 #15KHz*12subcarriers for numerology 0, 30KHz*12subcarriers for numerology 1, etc.
            #  NRbandwidth_prb_lookup defines the number of blocks of 180KHz available in the specified bandwidth with a certain numerology,
            #  so we have to multiply by the number of time slots (sub-frames in LTE terminology) in a time frame
            new_bs = NRbs.NRBaseStation(len(self.bs_list), NRbs.NRbandwidth_prb_lookup[numerology][fr][available_bandwidth] * (10 * 2**numerology), prb_size, 12, numerology, antenna_power, antenna_gain, feeder_loss, carrier_frequency, total_bitrate, antenna_nr, position, self)
        else:
            raise Exception("The choosen bandwidth is not present in 5G NR standard with such numerology and frequency range")

        self.bs_list.append(new_bs)
        self.all_bs_list.append(new_bs)
        return new_bs.bs_id

    #this method shall be called by an UE
    #that wants to have a measure of the RSRP associated to each BS
    #And to search for active BS around UE
    def discover_bs(self, ue_id):
        rsrp = dict()

        for i in range(0, len(self.bs_list)):
            if self.bs_list[i].bs_type == "nr":
                path_loss = util.compute_path_loss_cost_hata(self.ue_list[ue_id], self.bs_list[i], self)
                if path_loss <= 100:
                    res = util.compute_rsrp(self.ue_list[ue_id], self.bs_list[i], self)
                    if res > util.MIN_RSRP:
                        rsrp[self.bs_list[i].bs_id] = res
        return rsrp

    def initial_timestep(self):
        #call each initial_timestep function in order to set the initial conditions for each commodity in terms of bitrate
        #to be requested to each BS
        for ue in self.ue_list:
            ue.initial_timestep()
        return True

    def next_timestep(self):
        for ues in self.ue_list:
            ues.next_timestep()
        for bss in self.bs_list:
            bss.next_timestep()

    def reset(self, cycle):
        for ues in self.ue_list:
            ues.reset(cycle)
        for bs in self.bs_list:
            bs.reset()
