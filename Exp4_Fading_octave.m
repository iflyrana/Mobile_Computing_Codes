N = 10^6; % Number of bits or symbols

rand('state', 100); % Initializing the rand() function
randn('state', 200); % Initializing the randn() function

% Transmitter
ip = rand(1, N) > 0.5; % Generating 0,1 with equal probability
s = 2 * ip - 1; % BPSK modulation: 0 -> -1, 1 -> 1

n = 1/sqrt(2) * (randn(1, N) + 1j * randn(1, N)); % White Gaussian noise, 0 dB variance

Eb_NO_dB = -3:10; % Multiple Eb/No values

% Pre-allocate memory
nErr_AWGN = zeros(1, length(Eb_NO_dB));
nErr_Rayleigh = zeros(1, length(Eb_NO_dB));

for ii = 1:length(Eb_NO_dB)
    % Noise addition for AWGN channel
    y_AWGN = s + 10^(-Eb_NO_dB(ii) / 20) * n; % Additive White Gaussian Noise (AWGN)

    % Rayleigh channel
    h = 1/sqrt(2) * (randn(1, N) + 1j * randn(1, N)); % Rayleigh fading coefficients
    y_Rayleigh = h .* s + 10^(-Eb_NO_dB(ii) / 20) * n; % Signal through Rayleigh channel

    % Equalization in Rayleigh channel
    y_equalized = y_Rayleigh ./ h; % Compensating for channel effects

    % Receiver - hard decision decoding
    ipHat_AWGN = real(y_AWGN) > 0;
    ipHat_Rayleigh = real(y_equalized) > 0;

    % Counting the errors
    nErr_AWGN(ii) = sum(ip ~= ipHat_AWGN);
    nErr_Rayleigh(ii) = sum(ip ~= ipHat_Rayleigh);
end

% Simulated BER
simBer_AWGN = nErr_AWGN / N;
simBer_Rayleigh = nErr_Rayleigh / N;

% Theoretical BER
theoryBer_AWGN = 0.5 * erfc(sqrt(10.^(Eb_NO_dB / 10))); % AWGN theoretical BER
theoryBer_Rayleigh = 0.5 * (1 - sqrt(10.^(Eb_NO_dB / 10) ./ (1 + 10.^(Eb_NO_dB / 10)))); % Rayleigh theoretical BER

% Plot 1: BER for AWGN channel
figure;
semilogy(Eb_NO_dB, theoryBer_AWGN, 'b.-', 'LineWidth', 1.5); hold on;
semilogy(Eb_NO_dB, simBer_AWGN, 'mx-', 'LineWidth', 1.5);
axis([-3 10 10^-5 0.5]);
grid on;
legend('Theory (AWGN)', 'Simulation (AWGN)');
xlabel('Eb/No, dB');
ylabel('Bit Error Rate');
title('Bit error probability curve for BPSK modulation in AWGN channel');

% Plot 2: BER for both AWGN and Rayleigh channels
figure;
semilogy(Eb_NO_dB, theoryBer_AWGN, 'b.-', 'LineWidth', 1.5); hold on;
semilogy(Eb_NO_dB, simBer_AWGN, 'mx-', 'LineWidth', 1.5);
semilogy(Eb_NO_dB, theoryBer_Rayleigh, 'r.-', 'LineWidth', 1.5);
semilogy(Eb_NO_dB, simBer_Rayleigh, 'go-', 'LineWidth', 1.5);
axis([-3 10 10^-5 0.5]);
grid on;
legend('Theory (AWGN)', 'Simulation (AWGN)', 'Theory (Rayleigh)', 'Simulation (Rayleigh)');
xlabel('Eb/No, dB');
ylabel('Bit Error Rate');
title('Bit error probability curve for BPSK modulation in AWGN and Rayleigh channels');

