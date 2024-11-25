import pyshark
import pandas as pd

# Define the input PCAP file and output CSV file
pcap_file = 's7comm_merged.pcap'  # Replace with your PCAP file path
csv_file = 's7_output.csv'  # Replace with your desired output CSV file path

# Read the PCAP file using pyshark
cap = pyshark.FileCapture(pcap_file, display_filter='s7comm')

# Create an empty list to hold packet data
packet_data = []

# Iterate over each packet and extract required information
for packet in cap:
    try:
        # Extract common fields
        timestamp = packet.sniff_time
        src_ip = packet.ip.src
        dst_ip = packet.ip.dst
        length = packet.length
        
        # Extract S7 protocol specific fields if available
        if 's7comm' in packet:
            s7_fields = packet.s7comm.field_names
            s7_values = {field: getattr(packet.s7comm, field) for field in s7_fields}

            # Prepare a combined dictionary with both common and S7-specific fields
            packet_info = {
                'Timestamp': timestamp,
                'Source IP': src_ip,
                'Destination IP': dst_ip,
                'Length': length
            }
            packet_info.update(s7_values)

            # Append the extracted data to the list
            packet_data.append(packet_info)

    except AttributeError:
        # If a packet doesn't have the required fields, skip it
        continue

# Create a DataFrame from the packet data
df = pd.DataFrame(packet_data)

# Write the DataFrame to a CSV file
df.to_csv(csv_file, index=False)

print(f"Data successfully extracted to {csv_file}")
