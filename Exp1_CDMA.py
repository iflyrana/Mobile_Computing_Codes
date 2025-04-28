import numpy as np

# Function to generate Walsh code matrix of size 2^n x 2^n
def generate_walsh_matrix(n):
    if n == 1:
        return np.array([[1, 1], [1, -1]])
    else:
        smaller_matrix = generate_walsh_matrix(n - 1)
        top = np.hstack((smaller_matrix, smaller_matrix))
        bottom = np.hstack((smaller_matrix, -smaller_matrix))
        return np.vstack((top, bottom))

# Function to calculate SNR (Ratio, NOT in dB)
def calculate_snr(transmitted_signal, walsh_code):
    signal_power = (np.dot(transmitted_signal, walsh_code) / len(walsh_code))**2  # Signal strength

    noise_components = transmitted_signal - walsh_code * (np.dot(transmitted_signal, walsh_code) / len(walsh_code))
    noise_power = np.var(noise_components)  # Variance of noise

    snr = signal_power / noise_power if noise_power > 0 else float('inf')  # SNR as a ratio
    return snr, noise_power

# Function to simulate CDMA encoding and decoding
def cdma_simulation():
    num_subscribers = 4  # Number of users (must be power of 2)
    log2_n = int(np.log2(num_subscribers))  

    # Generate Walsh codes
    walsh_matrix = generate_walsh_matrix(log2_n)
    print(f"\n--- Step 1: Generated Walsh Code Matrix ({num_subscribers}x{num_subscribers}) ---")
    print(walsh_matrix)

    # Simulate messages (each user sends either -1 or 1)
    messages = np.random.choice([-1, 1], num_subscribers)
    print(f"\n--- Step 2: Original Messages Sent by Users ---")
    for i in range(num_subscribers):
        print(f"User {i+1}: {messages[i]}")

    # Encode messages with Walsh codes
    encoded_signals = np.array([messages[i] * walsh_matrix[i] for i in range(num_subscribers)])
    
    print(f"\n--- Step 3: Encoded Signals (Each User's Message × Walsh Code) ---")
    for i in range(num_subscribers):
        print(f"User {i+1}: {encoded_signals[i]}")

    # Transmit all encoded signals together (sum them up)
    transmitted_signal = np.sum(encoded_signals, axis=0)
    print(f"\n--- Step 4: Transmitted Signal (Summed Up Encoded Signals) ---")
    print(transmitted_signal)

    # Compute SNR
    snr_values, noise_power = calculate_snr(transmitted_signal, walsh_matrix[0])  # Example: Compute SNR for User 1
    print(f"\n--- Step 5: Signal-to-Noise Ratio (SNR as a Ratio) ---")
    print(f"SNR: {snr_values}, Noise Power: {noise_power}")

    # Decode messages
    decoded_messages = []
    print(f"\n--- Step 6: Decoding Messages Using Walsh Codes ---")
    for i in range(num_subscribers):
        correlation = np.dot(transmitted_signal, walsh_matrix[i]) / num_subscribers
        decoded_messages.append(round(correlation))
        print(f"User {i+1}: Decoded {decoded_messages[i]} (Original: {messages[i]})")

    # Verify correctness
    if np.array_equal(messages, decoded_messages):
        print("\n✅ Decoding successful! Users correctly received their messages.\n")
    else:
        print("\n❌ Decoding failed! Errors detected in transmission.\n")

    # Check unintended users (random interference)
    print("--- Step 7: Checking Signals for Unintended Receivers ---")
    unintended_indices = np.random.choice(range(num_subscribers), size=3, replace=False)
    for idx in unintended_indices:
        random_code = np.random.choice([-1, 1], num_subscribers)
        correlation = np.dot(transmitted_signal, random_code) / num_subscribers
        print(f"Unintended Code {random_code}: Correlation {correlation:.2f} (interpreted as noise)")

# Run the simulation
cdma_simulation()
