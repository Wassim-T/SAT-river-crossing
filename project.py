from pysat.solvers import Minicard
from pysat.formula import IDPool

def gen_solution(chicken_times: list[int], boat_capacity: int, max_time: int) -> list[tuple[int, list[int]]] | None:
    """
    Cherche une solution pour faire traverser les poules en un temps <= max_time.
    Retourne une liste d'étapes [(t, [poule1, poule2]), ...] ou None.
    """
    vpool = IDPool()
    solver = Minicard() 
    
    num_chickens = len(chicken_times)
    possible_durations = sorted(list(set(chicken_times)))
    chickens = range(num_chickens)
    
    # contrainte d'etat initial

    # initialisation poules : (tout le monde sur A en mettant B a faux)
    for p in chickens:
        solver.add_clause([-vpool.id(("B", p, 0))])
    
    # initialisation de la barque du cote A
    solver.add_clause([vpool.id(("side", 0))])

    # boucle sur chaque instant t jusqu'a max_time
    for t in range(max_time + 1):
        
      
        # defininion variable de départ
        dep = []
        for p in chickens:
            #les sens (0=aller, 1=retour)
            for s in [0, 1]: 
                var_dep = vpool.id(("dep", t, p, s))
                dep.append(var_dep)
                # clause pour dire si quelqu'un part alors il y a un depart a l instant t
                solver.add_clause([-var_dep, vpool.id(("DEP", t))]) 
        # dans l autre sens car c est une equivalence la contrainte
        solver.add_clause([-vpool.id(("DEP", t))] + dep)

        dur = []
        for d in possible_durations:
            var_dur = vpool.id(("dur", t, d))
            dur.append(var_dur)
            
            # contrainte interdiction d avoir un chicken plus lent que le temps de traversée
            for p in chickens:
                if chicken_times[p] > d:
                    for s in [0, 1]:
                        solver.add_clause([-var_dur, -vpool.id(("dep", t, p, s))])
            
            # contrainte qui s assure qu'un chicken a une durée d de traversée si il part
            check_time_chicken = []
            for p in chickens:
                if chicken_times[p] == d:
                    check_time_chicken.append(vpool.id(("dep", t, p, 0)))
                    check_time_chicken.append(vpool.id(("dep", t, p, 1)))
            solver.add_clause([-var_dur] + check_time_chicken)

            # contrainte qui s'assure que si il y a une traversée alors la variable DEP est a faux pour ne plus permettre de nouvelles traversées avant la fin de celle ci
            arrival_time = t + d
            if arrival_time <= max_time:
                for k in range(1, d):
                    if t + k <= max_time:
                        solver.add_clause([-var_dur, -vpool.id(("DEP", t + k))])

        # contrainte inverse car c est une equivalence
        solver.add_clause([-vpool.id(("DEP", t))] + dur)

      
        
        # contrainte sur le nombre de depart de poules simultanés car il y a une capacité maximale sur le bateau
        solver.add_atmost(dep, boat_capacity)

        # contrainte sur ou se trouve la barque en fonction de si c'est un aller ou un retour
        for p in chickens:
            solver.add_clause([-vpool.id(("dep", t, p, 0)), vpool.id(("side", t))])   #side a vrai = barque A
            solver.add_clause([-vpool.id(("dep", t, p, 1)), -vpool.id(("side", t))])  #side a faux = barque B

        # contrainte pour mettre a jour la position de la barque en regardant les departs passés et leurs durées
        for d in possible_durations:
            start_t = t - d
            if start_t >= 0:
                var_dur_past = vpool.id(("dur", start_t, d))
                for p in chickens:
                    # aller passé + durée OK -> side faux maintenant
                    solver.add_clause([-vpool.id(("dep", start_t, p, 0)), -var_dur_past, -vpool.id(("side", t))])
                    # retour passé + durée OK -> side vrai maintenant
                    solver.add_clause([-vpool.id(("dep", start_t, p, 1)), -var_dur_past, vpool.id(("side", t))])

      

        # contrainte pour s'assurer qu'une poule est sur la bonne berge en fonction de son départ
        for p in chickens:
            solver.add_clause([-vpool.id(("dep", t, p, 0)), -vpool.id(("B", p, t))]) # Aller -> Pas sur B
            solver.add_clause([-vpool.id(("dep", t, p, 1)), vpool.id(("B", p, t))])  # Retour -> Sur B

        # contrainte de mise a jour de la position des poules en fonction des departs passés et de leurs durées
        for d in possible_durations:
            start_t = t - d
            if start_t >= 0:
                var_dur_past = vpool.id(("dur", start_t, d))
                for p in chickens:
                    solver.add_clause([-vpool.id(("dep", start_t, p, 0)), -var_dur_past, vpool.id(("B", p, t))])
                    solver.add_clause([-vpool.id(("dep", start_t, p, 1)), -var_dur_past, -vpool.id(("B", p, t))])

        
        #contrainte pour s assurer qu une poule arrive vraiment a destination
        if t > 0:
            boat_causes_change_to_B = []
            boat_causes_change_to_A = []
            
            for p in chickens:
                chick_causes_arrive_B = []
                chick_causes_arrive_A = []
                
                for d in possible_durations:
                    start_t = t - d
                    if start_t >= 0:
                        var_dur = vpool.id(("dur", start_t, d))
                        
                        # pour l aller (vers B)
                        var_dep_aller = vpool.id(("dep", start_t, p, 0))
                        # Création variable auxilliaire : "Poule p arrive vraiment sur B à t grâce à un trajet de durée d"
                        aux_arr_B = vpool.id(("aux_arr_B", t, p, d))
                        
                       
                        solver.add_clause([-aux_arr_B, var_dep_aller])
                        solver.add_clause([-aux_arr_B, var_dur])
                        
                        chick_causes_arrive_B.append(aux_arr_B)
                        boat_causes_change_to_B.append(aux_arr_B) # Si une poule arrive sur B, le bateau aussi

                        # pour le retour (vers A)
                        var_dep_retour = vpool.id(("dep", start_t, p, 1))
                        aux_arr_A = vpool.id(("aux_arr_A", t, p, d))
                        
                        solver.add_clause([-aux_arr_A, var_dep_retour])
                        solver.add_clause([-aux_arr_A, var_dur])
                        
                        chick_causes_arrive_A.append(aux_arr_A)
                        boat_causes_change_to_A.append(aux_arr_A) # Si une poule arrive sur A, le bateau aussi

                # Inertie de la Poule
                # Si sur a avant et sur b maintenant => Arrivée B
                solver.add_clause([vpool.id(("B", p, t-1)), -vpool.id(("B", p, t))] + chick_causes_arrive_B)
                # Si sur b avant et sur a maintenant => Arrivée A
                solver.add_clause([-vpool.id(("B", p, t-1)), vpool.id(("B", p, t))] + chick_causes_arrive_A)

            # Inertie de la Barque
            # Si A(Vrai) -> B(Faux) => Arrivée d'un Aller
            solver.add_clause([-vpool.id(("side", t-1)), vpool.id(("side", t))] + boat_causes_change_to_B)
            # Si B(Faux) -> A(Vrai) => Arrivée d'un Retour
            solver.add_clause([vpool.id(("side", t-1)), -vpool.id(("side", t))] + boat_causes_change_to_A)

    # contrainte de victoire
    solver.add_clause([vpool.id(("ALL", max_time))]) 
    for p in chickens:
        solver.add_clause([vpool.id(("B", p, max_time))]) # Force tout le monde sur B

    # resolution du SAT
    if solver.solve():
        model = solver.get_model()
        solution = []
        for t in range(max_time + 1):
            traveling_chickens = []
            if (vpool.id(("DEP", t)) in model):
                for p in chickens:
                    if vpool.id(("dep", t, p, 0)) in model:
                        traveling_chickens.append(p + 1)
                    elif vpool.id(("dep", t, p, 1)) in model:
                        traveling_chickens.append(p + 1)
                
                if traveling_chickens:
                    solution.append((t, sorted(traveling_chickens)))
        return solution
    else:
        return None


def find_duration(chicken_times: list[int], boat_capacity: int) -> int:
    """
    Trouve la durée minimale T nécessaire pour que toutes les poules traversent.
    Utilise une recherche dichotomique pour minimiser les appels au solveur.
    """
    if not chicken_times:
        return 0
        
    # Borne inférieure : le temps de la poule la plus lente
    low = max(chicken_times)
    
   
    # Borne supérieure : une estimation grossière
    high = sum(chicken_times) * 2 + 100 
    
    best_t = high
    
    while low <= high:
        mid = (low + high) // 2
        solution = gen_solution(chicken_times, boat_capacity, mid)
        
        if solution is not None:
            # Si ca marche, on essaie de trouver mieux (plus petit)
            best_t = mid
            high = mid - 1
        else:
            # Si ca rate, il faut plus de temps
            low = mid + 1
            
    return best_t