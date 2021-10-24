def process_data(result):
    res = result.get_counts(qc)  # Retrieves dictionary containing measurement outcomes as keys
                                 # number of times that outcome was obtained as values.
    count_shots = 0
    rho = np.zeros((2,2))  # Initializes density matrix (2x2 matrix)
    states = res.keys()  # Extracts all the obtained measurement outcomes on the state
    Xexp = 0

    for state in states:
        num = res.get(state)  # Obtains the number of time this outcome was measured
        if int(state[3])==0:
            count_shots += num
            X = np.array([[0,1],[1,0]])
            s1 = int(state[4])
            s2 = int(state[3])
            s3 = int(state[2])
            s4 = int(state[1])
            s5 = int(state[0])  # Extracts the measurement outcomes on qubits 1/3/5
            s_mod = (s1+s3) % 2  # Calculating s1 + s3 (mod 2) for applying correction later
            rho_vect_list = [1/np.sqrt(2)*np.array([1,1]), 1/np.sqrt(2)*np.array([1,-1])]  # |+> and |-> eigenstates
            if s_mod == 0:
                out = int(state[0])
                xtemp = out
                rho_out = rho_vect_list[xtemp] # if s_mod = 0, then output is |+> if s_5 = 0, |-> if s_5 = 1
            else:  # Final state is |->?
                out = int(state[0])
                xtemp = (out + 1)%2
                rho_out = rho_vect_list[xtemp] # if s_mod = 1, then output is |-> if s_5 = 0, |+> if s_5 = 1
            if xtemp == 0:
                Xexp += num
            else:
                Xexp -= num
            rho_temp = np.outer(rho_out, rho_out) # Take outer product of |out> with itself
            rho += num*rho_temp # Add to rho, weighted by the number of experimental outcomes with this value

    rho = rho/count_shots  # Divide by number of experiments
    Xexp = Xexp/count_shots
    return Xexp