import sys
from geolite2 import geolite2


def main():
    try:
        with open(sys.argv[1]) as file:
            # open and read the file
            filestring = file.read()

            # parse IPs
            stringarray = filestring.split("Failed password for root from ")
            ips = []
            for string in stringarray:
                string = string.split(" ")
                string = string[0]
                ips.append(string)
            ips = ips[1:]

            # count instances of each ip
            ipdict = {}
            for ip in ips:
                if ip in ipdict.keys():
                    ipdict[ip] += 1
                else:
                    ipdict[ip] = 1

            # remove all less than 10
            keystopop = []
            for key in ipdict.keys():
                if ipdict[key] < 10:
                    keystopop.append(key)
            for key in keystopop:
                ipdict.pop(key)

            # get countries, organize data
            finaldata = []
            reader = geolite2.reader()
            for key in ipdict:
                finaldata.append((key, ipdict[key], reader.get(key)["country"]["names"]["en"]))

            # final print
            for data in finaldata:
                print(str(data[0]) + " tried to log in " + str(data[1]) + " times from " + str(data[2]))
    except FileNotFoundError:
        print("File not found")
        exit(1)
    except IndexError:
        print("File not specified")
        exit(1)
main()
