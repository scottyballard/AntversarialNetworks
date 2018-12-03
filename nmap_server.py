from scapy.modules.nmap import  *
conf.nmap_base = 'nmap-os-fingerprints'

def add_fingerprint(host, fp, hosts):
    fingerprints = list[hosts]
    #dont care about replacement; always want the freshest test
    fingerprints[fp['number']] = fp["T%i" % fp['number']]
    del fp['number']
    if len(fingerprints) == 8:
        fp_list = {}
        for i in range(1,8):
            fp_list.append(fingerprints[i])
        return make_determination(fp_list)
    else:
        return None

def make_determination(fp_list):
    sigs = nmap_probes2sig(fp_list)
    return nmap_search(sigs)

def get_fingerprint():
    #logic to receive fp from ants