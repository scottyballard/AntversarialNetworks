from scapy.modules.nmap import  *
conf.nmap_base = 'nmap-os-fingerprints'


def add_fingerprint(host, fp, hosts):
    fingerprints = hosts[host]
    num = fp['number']
    del fp['number']
    # don't care about replacement; always want the freshest test
    fingerprints[num] = fp
    if len(fingerprints) == 8:
        fp_list = {}
        for i in range(1, 8):
            fp_list.update(fingerprints[i])
        return make_determination(fp_list)
    else:
        return None


def make_determination(fp_list):
    sigs = nmap_probes2sig(fp_list)
    return nmap_search(sigs)



