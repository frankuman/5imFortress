from enum import Enum
import math
from simulation import environment

class EnvType (Enum):
    RURAL = 0
    SUBURBAN = 1
    URBAN = 2

MIN_RSRP = -120 # -140 #dB

def compute_rsrp(ue, bs, env):
    if bs.bs_type == "sat":
        return bs.sat_eirp - bs.path_loss - bs.atm_loss - bs.ut_G_T
    else:
        #nr case
        path_loss = compute_path_loss_cost_hata(ue, bs, env)
        subcarrier_power = 10*math.log10(bs.antenna_power*1000 / ((bs.total_prb/(10*2**bs.numerology))*bs.number_subcarriers))
        return subcarrier_power + bs.antenna_gain - bs.feeder_loss - path_loss

def compute_path_loss_cost_hata(ue, bs, env, save = None):
    #compute distance first
    dist = math.sqrt((ue.current_position[0]-bs.position[0])**2 + (ue.current_position[1]-bs.position[1])**2 + (ue.h_m - bs.h_b)**2)
    if dist == 0:   #just to avoid log(0) in path loss computing
        dist = 0.01
    #compute C_0, C_f, b(h_b), a(h_m) and C_m with the magic numbers defined by the model
    if bs.carrier_frequency <= 1500 and bs.carrier_frequency >= 150 :
        C_0 = 69.55
        C_f = 26.16
        b = 13.82*math.log10(bs.h_b)
        if env.env_type == EnvType.URBAN:
            C_m = 0
        elif env.env_type == EnvType.SUBURBAN:
            C_m = -2*((math.log10(bs.carrier_frequency/28))**2) - 5.4
        else:
            C_m = -4.78*((math.log10(bs.carrier_frequency))**2) + 18.33*math.log10(bs.carrier_frequency) - 40.94
    else:  
        C_0 = 46.3
        C_f = 26.16
        b = 13.82*math.log10(bs.h_b)
        if env.env_type == EnvType.URBAN:
            C_m = 3
        elif env.env_type == EnvType.SUBURBAN:
            C_m = 0
        else:
            raise Exception("COST-HATA model is not defined for frequencies in 1500-2000MHz with RURAL environments")

    if env.env_type == EnvType.SUBURBAN or env.env_type == EnvType.RURAL:
        a = (1.1*math.log10(bs.carrier_frequency) - 0.7)*ue.h_m - 1.56*math.log10(bs.carrier_frequency) + 0.8
    else:
        if bs.carrier_frequency >= 150 and bs.carrier_frequency <= 300:
            a = 8.29*(math.log10(1.54*ue.h_m)**2) - 1.1
        else:
            a = 3.2*(math.log10(11.75*ue.h_m)**2) - 4.97
    
    path_loss = C_0 + C_f * math.log10(bs.carrier_frequency) - b - a + (44.9-6.55*math.log10(bs.h_b))*math.log10(dist/1000) + C_m
    if (save is not None):
        save = path_loss
    return path_loss

def find_bs_by_id(bs_id):
    return environment.wireless_environment.all_bs_list[bs_id]

def find_ue_by_id(ue_id):
    return environment.wireless_environment.ue_list[ue_id]


# run = 0

# def plot(ue, bs, env):
#     global ax
#     global fig
#     global run
#     if run == 0:
#         plt.ion()
#         fig, ax = plt.subplots()
#         run = 1

    
#     x_ue = []
#     y_ue = []
#     x_bs = []
#     y_bs = []

#     plt.cla()

#     #ax.set_xlim(0, env.x_limit)
#     #ax.set_ylim(0, env.y_limit)

#     colors = cm.rainbow(np.linspace(0, 1, len(bs)))

#     for j in bs:
#         x_bs.append(find_bs_by_id(j).position[0])
#         y_bs.append(find_bs_by_id(j).position[1])

#     for i in range(0, len(ue)):
#         x_ue.append(find_ue_by_id(ue[i]).current_position[0])
#         y_ue.append(find_ue_by_id(ue[i]).current_position[1])

#     for i in range(0, len(ue)):
#         for j in range(0, len(bs)):
#             if find_ue_by_id(ue[i]).current_bs == j:
#                 ax.scatter(x_ue[i], y_ue[i], color = colors[j])
#                 break
#         else:
#             ax.scatter(x_ue[i], y_ue[i], color = "tab:grey")

#     for i in range(0, len(ue)):
#         ax.annotate(str(ue[i]), (x_ue[i], y_ue[i]))

#     for j in range(0, len(bs)):
#         if find_bs_by_id(j).bs_type == "drone_relay":
#             ax.scatter(x_bs[j], y_bs[j], color = colors[j], label = "BS", marker = "^", s = 400, edgecolor = colors[find_bs_by_id(j).linked_bs], linewidth = 3)
#         elif find_bs_by_id(j).bs_type == "drone_bs":
#             ax.scatter(x_bs[j], y_bs[j], color = colors[j], label = "BS", marker = "^", s = 400)
#         else:
#             ax.scatter(x_bs[j], y_bs[j], color = colors[j], label = "BS", marker = "s", s = 400)
    
#     for j in range(0, len(bs)):
#         ax.annotate("BS"+str(j), (x_bs[j], y_bs[j]))

#     ax.grid(True)
#     ax.set_ylabel("[m]")
#     ax.set_xlabel("[m]")
#     fig.canvas.draw()
