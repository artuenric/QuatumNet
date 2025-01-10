# Parâmetros das simulações
network_info = {
    'n_initial_qubits': 5,
    'n_initial_eprs': 5,
    'topology_name': 'Grade',
    'topology_params': (3, 4),
    'time_to_refill': 10,
}
controller_info = {
    'default_ttl': 50,
}
request_info = {
    'num_hosts': 12,
    'n_requests': 100,
    'traffic_type': 'mixed',
    'burst_probability': 0.3,
    'burst_size': 10,
    'requests_per_burst': 5,
    'fmin_range': (0.5, 1.0),
    'eprs_range': (1, 10),
}
proactive_params = {
    1 : { 'frange': (0.6, 0.9), 'neprs': 10 },
}