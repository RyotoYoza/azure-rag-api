below are some of the useful windows bash command for some initial trouble shooting
1. net user <username> /domain 
this to create, modify, delete, and view user accounts on a local machine or an Active Directory domain
2. ipconfig /all
to display detailed network configuration details. It provides comprehensive information for all active network adapters, including IPv4/IPv6 addresses, MAC (Physical) addresses, subnet masks, default gateways, and DNS servers
3. netsh wlan show interface
List all saved networks: netsh wlan show profiles Find a Wi-Fi password: netsh wlan show profile name="ProfileName" key=clear (look for Key Content) Scan nearby Wi-Fi networks: netsh wlan show networks mode=bssid Check adapter details: netsh wlan show interfaces Disconnect current Wi-Fi: netsh wlan disconnect Delete a saved profile: netsh wlan delete profile
