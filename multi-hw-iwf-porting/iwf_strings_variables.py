#asil lte
asil_iwf_lte_dl_string="/opt/trs/bin/vtc iwf lte add-dl icom-type event-queue"
asil_iwf_lte_ul_string="/opt/trs/bin/vtc iwf lte add-ul"

#asoe lte
asoe_iwf_lte_dl_string="/opt/trs/bin/vtc iwf lte add-dl icom-type event-queue"
asoe_iwf_lte_ul_string="/opt/trs/bin/vtc iwf lte add-ul"

#asim lte
asim_iwf_lte_dl_string="/usr/bin/trs-vppctl lte_iwf add_dl_table_entry eNBTeid"
asim_iwf_lte_ul_string="/usr/bin/trs-vppctl lte_iwf add_ul_table_entry ccid_ul"
asim_iwf_lte_signalling="s1x2 0 unidir 1 icom_type 1"

#asim wcdma
asim_iwf_wcdma_ingress_string="/usr/bin/trs-vppctl wcdma_iwf set_ingress_wcdma_iwf udp_dst"
asim_iwf_wcdma_egress_string="/usr/bin/trs-vppctl wcdma_iwf set_egress_wcdma_iwf ccid_ul"

#asog lte
asog_iwf_lte_dl_string="/usr/bin/trs-vppctl lte_iwf add_dl_table_entry eNBTeid"
asog_iwf_lte_ul_string="/usr/bin/trs-vppctl lte_iwf add_ul_table_entry ccid_ul"
asog_iwf_lte_signalling="s1x2 0 unidir 1 icom_type 1"

#asib lte
asib_iwf_lte_dl_string="/opt/trs/bin/vtc iwf add-dl icom-type event-queue"
asib_iwf_lte_ul_string="/opt/trs/bin/vtc iwf add-ul"

