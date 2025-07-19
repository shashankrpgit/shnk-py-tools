*** Keywords ***
Verify Interface 
    [Arguments]    @{int}
    sleep    20s
    Remote Command Execute and Verify    rm -rf /tmp/monitor_dump.txt; rm -rf /tmp/monitor.txt    section_name=dut
    @{int}    Split String    @{int}    ,
    ${length}    Get Length    ${int}
    comment    verify if interfaces are enabled
    Remote Command Execute and Verify    cat /tmp/ethd.ini | grep -e SMOD- -e enabled > /tmp/eth_verify.txt; sed -Ei 's/\]//g' /tmp/eth_verify.txt; sed -Ei 's/\[SMOD-//g' /tmp/eth_verify.txt ; sed -Ei 's/enabled=//g' /tmp/eth_verify.txt ; tr '\n' ' ' < /tmp/eth_verify.txt > /tmp/test    section_name=dut
    : FOR    ${i}    IN RANGE    0    ${length}
    \    log    ${int[${i}]}
    \    ${status}=    Run Keyword And Return Status    Remote Command Execute and Verify    cat /tmp/test | grep -i "${int[${i}]} yes" \ | wc -l=>1    section_name=dut
    \    Run Keyword If    not ${status}    Run Keyword And Continue On Failure    Fail    interface is not enabled
    Log    Verifying if interfaces are UP
    Remote Command Execute and Verify    /opt/trs/bin/trs-eth-d -f /tmp/ethd.ini -s /tmp/ethd.sock monitor > /tmp/monitor_dump.txt &    section_name=dut
    sleep    5s
    Remote Command Execute and Verify    cat /tmp/monitor_dump.txt | head -n 7 > /tmp/monitor.txt    section_name=dut
    Remote Command Execute and Verify    cat /tmp/monitor.txt    section_name=dut
    : FOR    ${i}    IN RANGE    0    ${length}
    \    ${status}=    Run Keyword And Return Status    Remote Command Execute and Verify    cat /tmp/monitor.txt | grep -i LINK_UP | grep -i ${int[${i}]} \ | wc -l=>1
    \    Run Keyword If    not ${status}    Fail    Interface is not up
