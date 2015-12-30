listData = []
ip_school = {}
school_list = []
place_list = []
def readSchoolCSV():
    with open('school.csv', 'r') as datafile:
        for line in datafile:
            school, ip, place = line.split()
            if school not in school_list:
                school_list.append(school)
            if place not in place_list:
                place_list.append(place)

            school_data = {'school': school, 'place': place}
            ip_seg = ip.split('.')
            length = len(ip_seg)
            
            if ip_seg[0] not in ip_school:
                ip_school[ip_seg[0]] = {}
            if ip_seg[1] not in ip_school[ip_seg[0]]:
                ip_school[ip_seg[0]][ip_seg[1]] = {}

            if length is 3:
                ip_school[ip_seg[0]][ip_seg[1]].update({
                    'school': school,
                    'place' : place
                })
            if length is 4:
                if "~" in ip_seg[2]:
                    fore, rear = ip_seg[2].split("~")
                    for i in range(int(fore), int(rear)+1):
                        ip_school[ip_seg[0]][ip_seg[1]][str(i)] = school_data
                else:
                    ip_school[ip_seg[0]][ip_seg[1]][ip_seg[2]] = school_data
            if length is 5:
                if ip_seg[2] not in ip_school[ip_seg[0]][ip_seg[1]]:
                    ip_school[ip_seg[0]][ip_seg[1]][ip_seg[2]] = {}
                ip_school[ip_seg[0]][ip_seg[1]][ip_seg[2]][ip_seg[3]] = school_data
readSchoolCSV()
# print ip_school['140']['112']

def findIP_School(ip):
    if type(ip) is not str:
        #print "encode unicode"
        ip = ip.encode('utf-8')
    #print "type of ip", type(ip)
    ip_seg = ip.split('.')
    temp_ip_school = ip_school
    for seg in ip_seg:
        if seg in temp_ip_school:
            if 'school' in temp_ip_school[seg]:
                return temp_ip_school[seg]
            else:
                temp_ip_school = temp_ip_school[seg]
        else:
            return {"school": "unknown", 'place': "unknown"}