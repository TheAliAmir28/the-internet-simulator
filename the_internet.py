"""
Description:
  This program aims to replicate the internet. Functions include creating servers, creating connections between servers, 
  setting a server for navigation, creating a path from the set server to the server desired and more.
"""

def create_server(info, servers): #Function to create a server
    if len(info) == 3: # Check if the input has exactly 3 parts: command, server name, and IP address
        server_name = info[1]
        ip = info[2]
        valid_ip = True
        ip_exists = False
        server_exists = False

        address = ip.split(".") # Split the IP address into parts to validate it
        j = 0

        if len(address) == 4: #If the ip has the correct length
            while j < len(address) and valid_ip: #Validate IP address
                if int(address[j]) < 0 or int(address[j]) > 255: # Each part of the IP must be between 0 and 255
                    valid_ip = False
                    return "Error: Invalid IPv4 address."
                j += 1
        else:
            valid_ip = False
            return "Error: Invalid IPv4 address."
    
        if not valid_ip: #If ip is not valid, return the bools and exit
            ip_exists, server_exists = True, True
            return [ip_exists, server_exists]
                    
        if (server_name not in servers): #Check if server name doesn't already exist
            for value in servers.values():
                if value["ip"] != ip: #Check if ip doesn't exists already
                    continue
                else:
                    ip_exists = True
                    return "Error! Ip address already exists."
        else:
            server_exists = True
            return "Error: Server name already exists!"
        
        if ip_exists == server_exists == False: # If everything is valid, add the server to the dictionary
            servers[server_name] = {"ip": ip, "connections": {}, "visited": False} #Create the server in the dicionary
            return f"Success: A server with name {server_name} was created at ip {ip}" #Appropriate message
    else:
        return "Error: Invalid input. Please format as such: create-connection [server_1] [server_2] [connect_time]"
 
def create_connection(info, servers): #Function that creates a bi-directional connection between 2 servers.
    if len(info) == 4:
        server1 = info[1]
        server2 = info[2]
        route_num = info[3]

        if (server1 in servers) and (server2 in servers): #Check if both servers exist in the dicitionary
            server1_characteristics = servers[server1]
            connections = server1_characteristics['connections'] #Access connections dicionary
            server2_characteristics = servers[server2]
            connection2 = server2_characteristics['connections'] #Access connections dicionary

            if int(route_num) > 0: #Ensure the route time is positive
                if server2 not in connections and server1 not in connection2:
                    connections[server2] = route_num # Add connections if they don't already exist
                    connection2[server1] = route_num
                    return f"Success: A server with the name {server1} is now connected to {server2}"
                else:
                    return "Error: Connection is already established with the servers."
            else:
               return "Error: route must be positive"
        else:
            return "Error: One or both servers do not exist."
    else:
        return "Error: Invalid input. Please format as such: create-connection [server_1] [server_2] [connect_time]"

def set_server(info, servers, current_server): # Function to set a server
    if len(info) == 2:
        server_to_set = info[1]
        if server_to_set in servers:
            current_server = server_to_set
        else:
            for key, value in servers.items(): # Allow setting the server using its IP address
                if value['ip'] == server_to_set:
                    current_server = key
        if current_server == None:
            return f"Error: {server_to_set} does not exist."
        return [f"Server {current_server} selected.", current_server]
    else:
        return "Error: Invalid input. Please format as such: set-server [server_name or ip_v4_address]"

def ping(info, servers, current_server, command): # Function to handle the ping command
    if len(info) == 2:
        target_server = info[1]
        execution = command

        if current_server == None: # Check if a current server is set
            return f"Error: No server selected. Please set a current server using the 'set-server' command."
            
        server_exists = False 
        for server_name, details in servers.items(): # Verify if the target server exists
            if server_name == target_server or details['ip'] == target_server:
                server_exists = True
                target_server = server_name

        if not server_exists:
            return f"Error: Server {target_server} does not exist."

        for server in servers.values(): # Reset visited status for all servers
            server['visited'] = False

        result = ping_trace_rec(servers, current_server, target_server, execution)
        time = result[0]
        if time == -1:
            return f"Server {target_server} is not reachable."
        return f"Reply from {current_server} time = {time} ms."
    
    else:
        return f"Error: Invalid input. Please format as such: ping [server_name or ip_v4_address]"

def traceroute(info, servers, current_server, command): # Function to handle the traceroute command
    if len(info) != 2:
        return "Error: Please format as such: tracerout [server_name or ip_v4_address]"
    if current_server == None:
        return f"Error: No server selected. Please set a current server using the 'set-server' command."
    
    execution = command
    tracing_server = info[1]
    server_exists = False

    for server, details in servers.items(): # Check if the tracing server exists
        if server == tracing_server or details['ip'] == tracing_server:
            tracing_server = server
            server_exists = True

    if not server_exists:
        return f"Error: Server {tracing_server} does not exist."

    for server in servers.values(): # Reset visited status for all servers
            server['visited'] = False

    result = ping_trace_rec(servers, current_server, tracing_server, execution) # Get the path using the recursive function
    time, path = result

    if time == -1:
        return f"Unable to route to target system name {tracing_server}"
    
    output = f"Tracing route to {tracing_server}:\n" # Generate the traceroute output
    route_time = 0

    for i in range(len(path)):
        at_server = path[i]
        ip = servers[at_server]["ip"]

        if i == 0:
            route_time = 0
        else:
            previous_server = path[i - 1]
            route_time = servers[previous_server]["connections"][at_server]
        
        output += f"{i}  {route_time}  [{ip}]  {at_server}\n"

    output += "Trace complete."
    return output

def ping_trace_rec(servers, current_server, target_server, execution, time_accumulated=0): # Recursive function for ping and traceroute

    if current_server == target_server: #Base case: If target server is reached
        if execution == "traceroute" or execution == "tracert":
            return time_accumulated, [current_server]
        return time_accumulated, []

    servers[current_server]['visited'] = True # Mark the current server as visited

    server_connections = servers[current_server]['connections']  # Explore all connections of the current server
    for next_server, connection_time in server_connections.items():
        if servers[next_server]['visited']:
            continue

        result = ping_trace_rec(servers, next_server, target_server, execution, time_accumulated + int(connection_time)) # Recursive call for the next server

        if result[0] != -1:
            if execution == "traceroute" or execution == "tracert":
                return result[0], [current_server] + result[1]
            return result
        
    return -1, []

def ip_config(info, servers, current_server): #Function to handle the ip-config command
    if len(info) != 1:
        return f"Error: Please format as such: [ip-config]"
    if current_server == None: #Check if a server is set
        return f"Error: No server selected. Please set a current server using the 'set-server' command."
    
    return f"{current_server}   {servers[current_server]['ip']}" #Return the name and ip or set-server

def display_servers(info, servers): #Function to handle the display-servers command
    if len(info) != 1:
        print(f"Error: Please format as such: [display-servers]")
    if not servers: #Check if no servers exist
        print(f"Error: No servers exist. Please add servers using the 'create-server' command.")

    for server, details in servers.items(): #Display all servers
        print(f"{server}   {details['ip']}")
        for connection, time in details['connections'].items(): #Display their connections in tab-format
            print(f"\t{connection}  {servers[connection]['ip']}  {time}")

def main(servers, current_server): #Main function to handle user input
    user_choice = input(">>> ")

    while user_choice != "quit":
        split_input = user_choice.split()
        command = split_input[0]

        if command == "create-server":
            print(create_server(split_input, servers))
        elif command == "create-connection":
            print(create_connection(split_input, servers))
        elif command == "set-server":
            combined = set_server(split_input, servers, current_server)
            message, current_server = combined[0], combined[1]
            print(message)
        elif command == "ping":
            print(ping(split_input, servers, current_server, command))
        elif command == "traceroute" or command == "tracert":
            print(traceroute(split_input, servers, current_server, command))
        elif command == "ip-config":
            print(ip_config(split_input, servers, current_server))
        elif command == "display-servers":
            display_servers(split_input, servers)
        else:
            print("Error: Command not recognized.")

        user_choice = input(">>> ")

if __name__ == "__main__": #Execution
    servers = {}
    current_server = None
    main(servers, current_server)
