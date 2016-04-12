import sys
import re
#s = "alpha.C(usto)mer[cus_Y4o9qMEZAugtnW] ..."
#m = re.search(r"\(([A-Za-z0-9_]+)\)", s)
#print m.group(1)

if(len(sys.argv)<2):
    exit()
    print "Error Usage: mediaExtract.py pcapFileName"
ifile=sys.argv[1];
import subprocess
proc =subprocess.Popen(["videosnarf -i"+ifile+" | grep added"],stdout=subprocess.PIPE,shell=True)
(out,err)=proc.communicate()
li=out.split("\n")

proc =subprocess.Popen(["rm -rf *.264 *.wav *.opus"],stdout=subprocess.PIPE,shell=True)
(out,err)=proc.communicate()
#print li
opus_extracted=False
src_ip={}
dst_ip={}
for line in li:
    #print line
    if line != "":

        l1=line.split(":")
        l2=l1[1].split(" ")
        if l2[5] == "6e":
            if  False==opus_extracted:
                proc =subprocess.Popen(["../opus_extract/opusrtp --extract "+ifile+" 1>out.log 2>&1"],stdout=subprocess.PIPE,shell=True)
                print "Found opus codec id is : "+l2[5]
                opus_extracted=True
                proc=subprocess.Popen(["rm out.log"],stdout=subprocess.PIPE,shell=True)
            continue
        if l2[5] == "7d":
            #print "found h225 which is not a media codec"
            continue

        m1= line.split(" to ")
        ipp1 = re.search(":(.+?\()", m1[0])
        ipp2 = re.search("(.+?\()", m1[1])
        #print "Source IP: "+src_ip.group(1)+" Destication IP: "+dst_ip.group(1)
        ip1=ipp1.group(1).split("(")[0]
        ip2=ipp2.group(1).split("(")[0]

        m = re.search(r"\(([A-Za-z0-9_]+)\)", m1[0])
        port1=m.group(1)
        m = re.search(r"\(([A-Za-z0-9_]+)\)", m1[1])
        port2=m.group(1)

        if True==dst_ip.has_key(ip1):
            if src_ip.get(ip2)==port2 and dst_ip.get(ip1)==port1:
                print "Found codec id is      : "+l2[5]
                filter1=" -f"+"\"udp src port "+port1+"\" -o "+ip1+"_To_"+ip2
                proc =subprocess.Popen(["videosnarf -i"+ifile+filter1],stdout=subprocess.PIPE,shell=True)
                filter1=" -f"+"\"udp src port "+port2+"\" -o "+ip2+"_To_"+ip1
                piroc =subprocess.Popen(["videosnarf -i"+ifile+filter1],stdout=subprocess.PIPE,shell=True)

        src_ip[ip1]=port1
        dst_ip[ip2]=port2

        #print src_ip
        #print dst_ip

