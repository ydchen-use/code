import IPy


def if_ip_in_segment(ip, segment):
    if ip in IPy.IP(segment):
        return True
    else:
        return False

		
def if_ip_legal(ip):
	is_legal = False
	if IPy.IP(ip):
		is_legal = True
	return is_legal


if __name__ == "__main__":
    if if_ip_in_segment("172.32.53.4", "172.16.0.0/12"):
        print("1yes")
    if if_ip_in_segment("192.168.51.69", "192.168.0.0/16"):
        print("2yes")
    if if_ip_in_segment("192.168.51.22", "192.168.0.0/16"):
        print("3yes")
