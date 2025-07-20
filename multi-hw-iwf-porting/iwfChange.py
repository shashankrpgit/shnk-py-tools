#import libraries
import os
import re

#import variables
import user_inputs
import iwf_values
import iwf_strings_variables

#define variables
asil_iwf_lte_dl_string=iwf_strings_variables.asil_iwf_lte_dl_string
asil_iwf_lte_ul_string=iwf_strings_variables.asil_iwf_lte_ul_string
asil_queue_id=iwf_values.asil_queue_id
asil_event_queue_id=iwf_values.asil_event_queue_id
asil_mtype=iwf_values.asil_mtype

asib_iwf_lte_dl_string=iwf_strings_variables.asib_iwf_lte_dl_string
asib_iwf_lte_ul_string=iwf_strings_variables.asib_iwf_lte_ul_string
asib_queue_id=iwf_values.asib_queue_id
asib_event_queue_id=iwf_values.asib_event_queue_id
asib_mtype=iwf_values.asib_mtype

asim_iwf_lte_dl_string=iwf_strings_variables.asim_iwf_lte_dl_string
asim_iwf_lte_ul_string=iwf_strings_variables.asim_iwf_lte_ul_string
asim_iwf_lte_signalling=iwf_strings_variables.asim_iwf_lte_signalling
asim_queue_id=iwf_values.asim_queue_id
asim_mtype=iwf_values.asim_mtype

asim_iwf_wcdma_ingress_string=iwf_strings_variables.asim_iwf_wcdma_ingress_string
asim_iwf_wcdma_egress_string=iwf_strings_variables.asim_iwf_wcdma_egress_string



old_iwf_file = user_inputs.old_iwf_file
new_iwf_file = user_inputs.new_iwf_file
from_hardware = user_inputs.from_hardware
to_hardware = user_inputs.to_hardware
content = ""
write_file=False

def convert_from_lte_dl(hardware, line):
    # example
    # /opt/trs/bin/vtc iwf lte add-dl icom-type event-queue 1 2101842 28839 13348
    # /opt/trs/bin/vtc iwf add-dl icom-type event-queue 15 22020097 28839 13349
    teid = queueid = eventqueueid = mtype = function = None
    function = "add_dl"
    if hardware == "asil" or hardware == "asoe" or hardware == "asib":
        match = re.search(r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)$", line) # grep the details from the line
        if match:
            teid = str(match.group(1))
            queueid = str(match.group(2))
            eventqueueid = str(match.group(3))
            mtype = str(match.group(4))
            return function, teid # return the values
        else:
            print(f"{line}   >>>>  is not mapped as expected || func \"convert_from_lte_dl\" || HW {hardware}")
            return None, None
    elif hardware == 'asim':
        pattern = rf".*eNBTeid\s+(\d+)\s+queue_id\s+(\d+)\s+mtype\s+(\d+)\s+{asim_iwf_lte_signalling}$"
        match = re.search(pattern, line) # grep the details from the line
        if match:
            teid = int(match.group(1))
            queue_id = int(match.group(2))
            mtype = int(match.group(3))
            return function, teid # return the values
        else:
            print(f"{line}   >>>>  is not mapped as expected || func \"convert_from_lte_dl\" || HW asim")
            return None, None
    elif hardware == 'asog':
        # example
        # /usr/bin/trs-vppctl lte_iwf add_dl_table_entry eNBTeid 1 queue_id 5575251 mtype 13349 s1x2 0 unidir 1 icom_type 1
        pattern = rf".*eNBTeid\s+(\d+)\s+queue_id\s+(\d+)\s+mtype\s+(\d+)\s+{asog_iwf_lte_signalling}$"
        match = re.search(pattern, line) # grep the details from the line
        if match:
            teid = int(match.group(1))
            queue_id = int(match.group(2))
            mtype = int(match.group(3))
            return function, teid # return the values
        else:
            print(f"{line}   >>>>  is not mapped as expected || func \"convert_from_lte_dl\" || HW asog")
            return None, None
    else: return None, None
    
def convert_from_lte_ul(hardware,line):
    teid = queueid = eventqueueid = mtype = function = None
    function = "add_ul"
    if hardware == "asil" or hardware == "asoe" or hardware == "asib":
        ip_ver='None'
        #example
        #/opt/trs/bin/vtc iwf lte add-ul 1 18.18.18.18  50.50.50.11  1 46
        #/opt/trs/bin/vtc iwf lte add-ul 11 2aaa::aaaa 200a::0003 2 46
        #/opt/trs/bin/vtc iwf lte add-ul ccid sip dip teid dscp
        # /opt/trs/bin/vtc iwf  add-ul 15 11.19.157.2 11.19.157.100 15 10    ASIB
        match = re.search(r"(\d+)\s+([a-zA-Z\d.:]+)\s+([a-zA-Z\d.:]+)\s+(\d+)\s+(\d+)$", line) # grep the details from the line
        if match:
            ccid = str(match.group(1))
            src_ip = str(match.group(2))
            dst_ip = str(match.group(3))
            teid = str(match.group(4))
            dscp = str(match.group(5))
            return function, ccid, src_ip, dst_ip, teid, dscp, ip_ver
        else:
            print(f"{line}   >>>>  is not mapped as expected || func \"convert_from_lte_ul\" || HW asil / asoe")
            return None, None, None, None, None, None
    elif hardware =='asim':
        ip_ver='None'
        #example
        #/opt/trs/bin/trs-vppctl lte_iwf add_ul_table_entry ccid_ul 2 ip_ver 1 dst_ip 3001::100 src_ip 2003::10 teid_ul 2 dscp 46
        #/opt/trs/bin/trs-vppctl lte_iwf add_ul_table_entry ccid_ul 1 ip_ver 0 dst_ip 110.10.10.100 src_ip 110.10.10.10 teid_ul 1 dscp 46
        pattern = rf".*\s+ccid_ul\s+(\d+)\s+dst_ip\s+([a-zA-Z\d.:]+)\s+src_ip\s+([a-zA-Z\d.:]+)\s+teid_ul\s+(\d+)\s+dscp\s+(\d+)$"
        match = re.search(pattern, line) # grep the details from the line
        if match:
            ccid = str(match.group(1))
            dst_ip = str(match.group(2))
            src_ip = str(match.group(3))
            teid = str(match.group(4))
            dscp = str(match.group(5))
            return function, teid, src_ip, dst_ip, ccid, dscp, ip_ver
        else:
            print(f"{line}   >>>>  is not mapped as expected || func \"convert_from_lte_ul\" || HW asim")
            return None, None, None, None, None, None
    elif hardware =='asog':
        # example
        # /usr/bin/trs-vppctl lte_iwf add_ul_table_entry ccid_ul 1 ip_ver 1 dst_ip 200a:0000:0000:0000:0000:0000:0000:0002 src_ip 2000:0000:0000:0000:0000:0000:0000:200b teid_ul 1 dscp 43
        ip_ver='None'
        pattern = rf".*ccid_ul\s+(\d+)\s+ip_ver\s+(\d+)\s+dst_ip\s+([a-zA-Z\d.:]+)\s+src_ip\s+([a-zA-Z\d.:]+)\s+teid_ul\s+(\d+)\s+dscp\s+(\d+)$"
        match = re.search(pattern, line) # grep the details from the line
        if match:
            ccid = str(match.group(1))
            ip_ver = str(match.group(2))
            dst_ip = str(match.group(3))
            src_ip = str(match.group(4))
            teid = str(match.group(5))
            dscp = str(match.group(6))
            return function, teid, src_ip, dst_ip, ccid, dscp, ip_ver
        else:
            print(f"{line}   >>>>  is not mapped as expected || func \"convert_from_lte_ul\" || HW asog")
            return None, None, None, None, None, None, None

def convert_to_lte_dl(hardware,teid):
    if hardware == "asim":
        # example
        # /usr/bin/trs-vppctl lte_iwf add_dl_table_entry eNBTeid 187 queue_id 5575251 mtype 13349 s1x2 0 unidir 1 icom_type 1
        if teid:
            line = asim_iwf_lte_dl_string+" "+str(teid)
            line = line+" queue_id "+str(asim_queue_id)+" mtype "+str(asim_mtype)
            line = line+" "+asim_iwf_lte_signalling
            return line
    elif hardware == "asog":
        # example
        # /usr/bin/trs-vppctl lte_iwf add_dl_table_entry eNBTeid 1 queue_id 5575251 mtype 13349 s1x2 0 unidir 1 icom_type 1
        if teid:
            line = asog_iwf_lte_dl_string+" "+str(teid)
            line = line+" "+str(asog_queue_id)+" "+str(asog_mtype)
            line = line+" "+asog_iwf_lte_signalling
            return line
    elif hardware == "asil":
        # example
        # /opt/trs/bin/vtc iwf lte add-dl icom-type event-queue 1 22286930 28839  13349
        if teid:
            line = asil_iwf_lte_dl_string+" "+str(teid)
            line = line+" "+str(asil_queue_id)+" "+str(asil_event_queue_id)
            line = line+" "+str(asil_mtype)
            return line
    elif hardware == "asib":
        # example
        # /opt/trs/bin/vtc iwf add-dl icom-type event-queue 1 22286930 28839  13349
        if teid:
            line = asib_iwf_lte_dl_string+" "+str(teid)
            line = line+" "+str(asib_queue_id)+" "+str(asib_event_queue_id)
            line = line+" "+str(asib_mtype)
            return line
    elif hardware == "asoe":
        # example
        # /opt/trs/bin/vtc iwf lte add-dl icom-type event-queue 1 2101842 28839 13348
        if teid:
            line = asoe_iwf_lte_dl_string+" "+str(teid)
            line = line+" "+str(asoe_queue_id)+" "+str(asoe_event_queue_id)
            line = line+" "+str(asoe_mtype)
            return line
    else: return None

def convert_to_lte_ul(hardware, ccid, src_ip, dst_ip, teid, dscp, ip_ver):
    if hardware == "asim":
        # example
        # /usr/bin/trs-vppctl lte_iwf add_ul_table_entry ccid_ul 1 dst_ip 63.0.0.2 src_ip 63.0.0.1 teid_ul 1 dscp 10
        # /usr/bin/trs-vppctl lte_iwf add_ul_table_entry ccid_ul 2 ip_ver 1 dst_ip 3001::100 src_ip 3001::11 teid_ul 2 dscp 46
        # /usr/bin/trs-vppctl lte_iwf add_ul_table_entry ccid_ul 187 ip_ver 1 dst_ip 2a0d::200a src_ip 2a00::200a teid_ul 187 dscp 46
        if teid and dscp:
            if '.' in src_ip:
                line = asim_iwf_lte_ul_string+" "+ccid
                line = line+" dst_ip "+dst_ip+" src_ip "+src_ip+" teid_ul "+teid+" dscp "+dscp
            else:    
                line = asim_iwf_lte_ul_string+" "+ccid
                line = line+" ip_ver 1 "+"dst_ip "+dst_ip+" src_ip "+src_ip+" teid_ul "+teid+" dscp "+dscp
            return line
    if hardware == "asog":
        # example
        # /usr/bin/trs-vppctl lte_iwf add_ul_table_entry ccid_ul 1 ip_ver 1 dst_ip 200a:0000:0000:0000:0000:0000:0000:0002 src_ip 2000:0000:0000:0000:0000:0000:0000:200b teid_ul 1 dscp 43
        if teid and ip_ver:
            line = asog_iwf_lte_ul_string+" "+ccid
            line = line+" ip_ver "+ip_ver+" dst_ip "+dst_ip+" src_ip "+src_ip+" teid_ul "+teid+" dscp "+dscp
            return line
    elif hardware == "asil":
        # example
        # /opt/trs/bin/vtc iwf lte add-ul 1 18.18.18.18  50.50.50.11  1 46
        if teid and dscp:
            line = asil_iwf_lte_ul_string+" "+ccid
            line = line+" "+src_ip+" "+dst_ip+" "+teid+" "+dscp
            return line
    elif hardware == "asib":
        # example
        # /opt/trs/bin/vtc iwf add-ul 1 18.18.18.18  50.50.50.11  1 46
        if teid and dscp:
            line = asib_iwf_lte_ul_string+" "+ccid
            line = line+" "+src_ip+" "+dst_ip+" "+teid+" "+dscp
            return line
    elif hardware == "asoe":
        # example
        # /opt/trs/bin/vtc iwf lte add-ul 1 18.18.18.18  50.50.50.11  1 46
        if teid and dscp:
            line = asoe_iwf_lte_ul_string+" "+ccid
            line = line+" "+src_ip+" "+dst_ip+" "+teid+" "+dscp
            return line
    else: return None

#wcdma
def convert_from_wcdma_ingress(hardware, line):
    # example
    # /usr/bin/trs-vppctl wcdma_iwf set_ingress_wcdma_iwf udp_dst 49201 tx_nid 4115 rx_nid 4115 tx_cpid 32769 rx_cpid 32769 mtype 501
    # /opt/trs/bin/vtc wcdma iwf dl add 49201 4115 32769 4115 32769 501
    # /opt/trs/bin/vtc iwf wcdma add-dl 49205 4115 32775 4115 32775 501  ASIB
    tx_nid = rx_nid = tx_cpid = rx_cpid = mtype = None
    function = "add_ingress"
    if hardware == "asil" or hardware== "asoe" or hardware== "asib":
        match = re.search(r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)$", line) # grep the details from the line
        if match:
            udp_dst = str(match.group(1))
            tx_nid = str(match.group(2))
            tx_cpid = str(match.group(3))
            rx_nid = str(match.group(4))
            rx_cpid = str(match.group(5))
            mtype = str(match.group(6))            
            return function, udp_dst, tx_nid, tx_cpid, rx_nid, rx_cpid, mtype # return the values
        else:
            print(f"{line}   >>>>  is not mapped as expected || func \"convert_from_wcdma_ingress\" || HW {hardware}")
            return None, None, None, None, None, None, None

def convert_from_wcdma_egress(hardware,line):
    ccid_ul = dst_ip = dst_port = src_ip = src_port = dscp = ip_ver = function = None
    function = "add_egress"
    if hardware == "asil" or hardware== "asoe" or hardware== "asib":
        #example
        #/opt/trs/bin/vtc wcdma iwf ul add 32768 90.1.1.10 49200 90.1.1.1 49200 10
        #/opt/trs/bin/vtc iwf lte add-ul ccid sip dip teid dscp
        #/opt/trs/bin/vtc iwf wcdma add-ul 32775 142.33.157.41 49205 142.33.157.2 49205 1     ASIB
        match = re.search(r"(\d+)\s+([a-zA-Z\d.:]+)\s+(\d+)\s+([a-zA-Z\d.:]+)\s+(\d+)\s+(\d+)", line) # grep the details from the line
        if match:
            ccid_ul = str(match.group(1))
            dst_ip = str(match.group(2))
            dst_port = str(match.group(3))
            src_ip = str(match.group(4))
            src_port = str(match.group(5))
            dscp = str(match.group(6))
            ip_ver = ('0' if '.' in src_ip
                else '1'
            )
            return function, ccid_ul, src_ip, src_port, dst_ip, dst_port, dscp, ip_ver
        else:
            print(f"{line}   >>>>  is not mapped as expected || func \"convert_from_wcdma_egress\" || HW {hardware}")
            return None, None, None, None, None, None, None, None

def convert_to_wcdma_ingress(hardware, udp_dst, tx_nid, tx_cpid, rx_nid, rx_cpid, mtype):
    if hardware == "asim":
        # example
        # /usr/bin/trs-vppctl wcdma_iwf set_ingress_wcdma_iwf udp_dst 49201 tx_nid 4115 rx_nid 4115 tx_cpid 32769 rx_cpid 32769 mtype 501
        if udp_dst:
            line = asim_iwf_wcdma_ingress_string+" "+udp_dst+" tx_nid "+tx_nid+" rx_nid "+rx_nid
            line = line+" tx_cpid "+tx_cpid+" rx_cpid "+rx_cpid+" mtype "+mtype
            return line

def convert_to_wcdma_egress(hardware, ccid_ul, src_ip, src_port, dst_ip, dst_port, dscp, ip_ver):
    if hardware == "asim":
        # example
        # /usr/bin/trs-vppctl wcdma_iwf set_egress_wcdma_iwf ccid_ul 32770 dst_ip 41.0.0.10 dst_port 49202 src_ip 31.0.0.10 src_port 49202 dscp 46 is_ipv6 0
        if ccid_ul:
            line = asim_iwf_wcdma_egress_string+" "+ccid_ul+" ip_dst "+dst_ip+" dst_port "+dst_port
            line = line+" ip_src "+src_ip+" src_port "+src_port+" dscp "+dscp+" is_ipv6 "+ip_ver
            return line

# execution starts from here.
# open the old file and read it line by line. strip extra spaces and blank lines.
with open(old_iwf_file, 'r') as file:
    lines = [line.strip() for line in file if line.strip()]
for line in lines:
    function = 'None'
    print("************processing***************")
    print(line)
    if line.startswith("#") or line.startswith("echo"):
        content += line+"\n"
    elif "clean" in line or "reset" in line or 'del' in line:
        print("need to update")
    else:
        # get input required from "from hardware"
        if 'add' in line or 'ingress' in line:
            if 'dl' in line or 'ingress' in line:
                if 'lte' in line:
                    function, teid = convert_from_lte_dl(from_hardware, line)
                elif 'wcdma' in line:
                    function, udp_dst, tx_nid, tx_cpid, rx_nid, rx_cpid, mtype = convert_from_wcdma_ingress(from_hardware, line)
                else:
                    function, teid = convert_from_lte_dl(from_hardware, line)
            elif 'ul' in line or 'egress' in line:
                if 'lte' in line or 'add-ul' in line:
                    function, ccid, src_ip, dst_ip, teid, dscp, ip_ver = convert_from_lte_ul(from_hardware, line)
                elif 'wcdma' in line:
                    function, ccid_ul, src_ip, src_port, dst_ip, dst_port, dscp, ip_ver = convert_from_wcdma_egress(from_hardware, line)
        # pass above values obtained to "to hardware"
        if function == 'add_dl' or function == 'add-dl':
            to_hardware_iwf_entry = convert_to_lte_dl(to_hardware,teid)
            content += to_hardware_iwf_entry+"\n"
        elif function == 'add_ul' or function == 'add-ul':
            ip_ver = (
                'None' if to_hardware in ('asib', 'asoe')
                else '1' if ':' in src_ip
                else '0' if '.' in src_ip
                else ip_ver
            )
            to_hardware_iwf_entry = convert_to_lte_ul(to_hardware, ccid, src_ip, dst_ip, teid, dscp, ip_ver)
            content += to_hardware_iwf_entry+"\n"
        elif function == 'add_ingress':
            to_hardware_iwf_entry = convert_to_wcdma_ingress(to_hardware, udp_dst, tx_nid, tx_cpid, rx_nid, rx_cpid, mtype)
            content += to_hardware_iwf_entry+"\n"
        elif function == 'add_egress':
            to_hardware_iwf_entry = convert_to_wcdma_egress(to_hardware, ccid_ul, src_ip, src_port, dst_ip, dst_port, dscp, ip_ver)
            content += to_hardware_iwf_entry+"\n"
        #content += to_hardware_iwf_entry+"\n"
        print("***********converted to**************")
        print (to_hardware_iwf_entry+"\n")

#write content to new iwf file
if content:
    with open(new_iwf_file, "w") as file:
        file.write(content)
        write_file=True

if write_file: print (f"content written to the {new_iwf_file}")
else : print (f"content update failed to the {new_iwf_file}")