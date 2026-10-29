import os 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
 
# Set random seed for reproducible noise 
np.random.seed(42) 
 
# --- 1. SETUP OUTPUT DIRECTORY --- 
output_dir = 'output_plots' 
os.makedirs(output_dir, exist_ok=True)  # Creates folder if it doesn't exist 
file_path = os.path.join(output_dir, 'bpsk_hello_simulation.png') 
 
# --- 2. TRANSMITTER (Tx) SETUP --- 
message = "hello" 
 
# Convert ASCII string to 8-bit binary stream 
binary_str = "".join(format(ord(char), '08b') for char in message) 
binary_data = np.array([int(b) for b in binary_str]) 
 
num_bits = len(binary_data)      # 5 characters * 8 bits = 40 bits total 
samples_per_bit = 40             # Samples per bit duration 
snr_db = 7                       # Signal-to-Noise Ratio (in dB)  
# BPSK Modulation (0 -> -1 V, 1 -> +1 V) 
bpsk_symbols = np.where(binary_data == 1, 1, -1) 
 
# Continuous time-domain representation for plotting 
t = np.linspace(0, num_bits, num_bits * samples_per_bit) 
binary_signal = np.repeat(binary_data, samples_per_bit)
tx_signal = np.repeat(bpsk_symbols, samples_per_bit) 
 
# --- 3. CHANNEL (AWGN) --- 
snr_linear = 10 ** (snr_db / 10.0) 
signal_power = np.mean(tx_signal ** 2) 
noise_power = signal_power / snr_linear 
noise = np.random.normal(0, np.sqrt(noise_power), len(tx_signal)) 


 
# Received Signal (Tx Signal + Channel Noise) 
rx_signal = tx_signal + noise 
 
# --- 4. RECEIVER (Rx) PROCESSING --- 
 
# Mid-bit sampling 
sample_indices = np.arange(samples_per_bit // 2, len(rx_signal), samples_per_bit)
rx_samples = rx_signal[sample_indices] 
 
# Decision Threshold at 0 V 
rx_bits = np.where(rx_samples > 0, 1, 0) 
 
# Reconstruct Text Message from Decoded Bits 
rx_binary_str = "".join(str(b) for b in rx_bits) 
decoded_chars = [ 
    chr(int(rx_binary_str[i:i+8], 2)) 
    for i in range(0, len(rx_binary_str), 8) 
] 
received_message = "".join(decoded_chars) 
 
# --- 5. RESULTS DISPLAY (Pandas) --- 
char_records = [] 
 
for i, char in enumerate(message): 
    orig_byte = binary_str[i * 8:(i + 1) * 8] 
    reco_byte = rx_binary_str[i * 8:(i + 1) * 8] 
 
    char_records.append({ 
        'Char': char, 
        'Original Binary': orig_byte, 
        'Decoded Binary': reco_byte, 
        'Reconstructed Char': decoded_chars[i], 
        'Status': 'Success' if char == decoded_chars[i] else 'Corrupted' 
    }) 
 
results_df = pd.DataFrame(char_records) 
 


print(f"Sent Message    : '{message}'") 
print(f"Received Message: '{received_message}'\n") 
 
print("--- Character Decoding Summary ---") 
print(results_df.to_string(index=False)) 
 
# ------------------------- 
# VISUALIZATION & SAVING 
# ------------------------- 
 
plt.figure(figsize=(15, 11)) 
 
# Overall title 
plt.suptitle( 
    f"Sent Message: '{message}'    |    Received Message: '{received_message}'", 
    fontsize=16, 
    fontweight='bold' 
) 
 
# ------------------------------------------------- 
# Subplot 1: Binary Bitstream 
# ------------------------------------------------- 
plt.subplot(4, 1, 1) 
 
plt.step( 
    t, 
    binary_signal, 
    where='post',     
    color='navy', 
    linewidth=1.5 
) 
 
plt.title(f'1. Input Binary Waveform ({num_bits} bits)') 
plt.xlabel('Time (bit periods)') 
plt.ylabel('Bit') 
plt.ylim(-0.2, 1.2) 
plt.grid(True) 
 


# ------------------------------------------------- 
# Subplot 2: BPSK Transmitted Signal 
# ------------------------------------------------- 
plt.subplot(4, 1, 2) 
 
plt.plot( 
    t,     
    tx_signal, 
    color='forestgreen', 
    linewidth=1.5 
) 
 
plt.title('2. BPSK Transmitted Waveform') 
plt.xlabel('Time (bit periods)') 
plt.ylabel('Voltage (V)') 
plt.ylim(-1.5, 1.5) 
plt.grid(True) 
 
# ------------------------------------------------- 
# Subplot 3: Received Noisy Signal 
# ------------------------------------------------- 
plt.subplot(4, 1, 3) 
 
plt.plot( 
    t, 
    rx_signal, 
    color='crimson', 
    alpha=0.6, 
    label='Received Signal' 
) 
 
plt.plot( 
    t, 
    tx_signal, 
    color='black',     
    linestyle='--', 
    linewidth=1, 
    label='Ideal Tx Signal' 


) 
 
plt.title(f'3. Received Signal with AWGN (SNR = {snr_db} dB)') 
plt.xlabel('Time (bit periods)') 
plt.ylabel('Voltage (V)') 
plt.legend(loc='upper right') 
plt.grid(True)  
# ------------------------------------------------- 
# Subplot 4: Sent vs Received Bit Comparison 
# ------------------------------------------------- 
plt.subplot(4, 1, 4) 
 
# Expand received bits for plotting 
rx_binary_signal = np.repeat(rx_bits, samples_per_bit) 
 
# Original transmitted bits 
plt.step( 
    t, 
    binary_signal + 0.15, 
    where='post',     color='blue', 
    linewidth=2, 
    label='Sent Bits' 
) 
 
# Received bits 
plt.step(     
    t, 
    rx_binary_signal - 0.15, 
    where='post', 
    color='red', 
    linestyle='--', 
    linewidth=2, 
    label='Received Bits' ) 
 
# Highlight bit errors 
error_locations = np.where(binary_data != rx_bits)[0] 
 
for idx in error_locations: 
    x = idx + 0.5 
    plt.axvline(x=x, color='magenta', linestyle=':', alpha=0.7) 
 
plt.title('4. Sent vs Received Bit Comparison') 
plt.xlabel('Time (bit periods)') 
plt.ylabel('Bit Value') 
plt.yticks([0, 1]) 
plt.ylim(-0.5, 1.5) 
plt.grid(True) 
plt.legend(loc='upper right') 
 
plt.tight_layout(rect=[0, 0, 1, 0.96]) 
 
# Save figure 
plt.savefig(file_path, dpi=300, bbox_inches='tight') 
 
print(f"\nPlot saved successfully to: {file_path}") 
plt.show() 

