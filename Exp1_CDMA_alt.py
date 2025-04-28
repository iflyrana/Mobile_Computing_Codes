import numpy as np
import random

def generate_walsh_matrix(n):
    if n == 1:
        return np.array([[1, 1], [1, -1]])
    W = generate_walsh_matrix(n - 1)
    top = np.hstack((W, W))
    bottom = np.hstack((W, -W))
    return np.vstack((top, bottom))

def simulate_cdma(num_users=8, num_bits=16, noise_std=0.5):
    walsh_size = int(np.log2(num_users))
    walsh_codes = generate_walsh_matrix(walsh_size)

    print("Walsh Matrix:")
    print(walsh_codes)
    print("=" * 50)

    subscribed_idx = random.randint(0, num_users - 1)
    message_bits = [1,1,0,1,4]
    code = walsh_codes[subscribed_idx]
    encoded_signal = np.array([bit * code for bit in message_bits])
    noise = np.random.normal(0, noise_std, size=encoded_signal.shape)
    received_signal = encoded_signal + noise

    print(f"Intended User: {subscribed_idx + 1}, Transmitting bit: {message_bits}")
    print("Transmitted Signal (before noise):")
    print(code * message_bits[0])
    print("Noise Added:")
    print(noise[0])
    print("Received Signal (with noise):")
    print(received_signal[0])
    print("=" * 50)

    print(f"{'User':<5}{'Type':<12}{'Correlation':>15}{'Signal Power':>15}{'Noise Power':>15}{'SNR (dB)':>15}")
    print("-" * 80)

    intended_corr = None
    intended_snr = None
    intended_sigp = None
    intended_noisep = None
    unintended_corrs = []
    unintended_snrs = []
    unintended_sigp = []
    unintended_noisep = []

    for i in range(num_users):
        user_code = walsh_codes[i]
        corr = np.dot(received_signal[0], user_code) / len(user_code)
        sig_power = corr ** 2
        noise_power = np.var(received_signal[0] - corr * user_code)
        snr_db = float('inf') if 10 * np.log10(sig_power / noise_power) < 0 else 10 * np.log10(sig_power / noise_power)

        user_type = "Intended" if i == subscribed_idx else "Unintended"

        # Printing the user information in a nicely formatted manner
        print(f"{i+1:<5}{user_type:<12}{corr:+15.4f}{sig_power:>15.6f}{noise_power:>15.6f}"
              f"    {snr_db if np.isfinite(snr_db) else '-inf':>15}")

        if user_type == "Intended":
            intended_corr = corr
            intended_snr = snr_db
            intended_sigp = sig_power
            intended_noisep = noise_power
        else:
            unintended_corrs.append(corr)
            unintended_snrs.append(snr_db)
            unintended_sigp.append(sig_power)
            unintended_noisep.append(noise_power)

    print("=" * 50)
    print("SUMMARY RESULTS:")
    print(f"Intended User {subscribed_idx + 1}:")
    print(f"- Correlation: {intended_corr:+.4f}")
    print(f"- SNR: {intended_snr:.2f} dB")
    print(f"- Signal Power: {intended_sigp:.6f}")
    print(f"- Noise Power: {intended_noisep:.6f}")
    print("Average Unintended User:")
    avg_corr = np.mean(unintended_corrs)
    avg_snr = '-inf' if not any(np.isfinite(unintended_snrs)) else f"{np.mean(unintended_snrs):.2f}"
    print(f"- Avg Correlation: {avg_corr:+.6f}")
    print(f"- Avg SNR: {avg_snr} dB")
    print(f"- Avg Signal Power: {np.mean(unintended_sigp):.6f}")
    print(f"- Avg Noise Power: {np.mean(unintended_noisep):.6f}")
    print("=" * 50)

simulate_cdma(8,1)