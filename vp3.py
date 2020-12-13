# Solves 3SAT problems.

import itertools

def iscover(graph, cover):
    v_all = []
    v_covered = []
    for x in graph:
        if not x[0] in v_all:
            v_all.append(x[0])
        if not x[1] in v_all:
            v_all.append(x[1])

    for vertex in cover:
        if not vertex in v_covered:
            v_covered.append(vertex)
        for edge in graph:
            if edge[0] == vertex and not edge[1] in v_covered:
                v_covered.append(edge[1])

    return (len(v_all) == len(v_covered))

def reduce(sat3):
    all_vars = []
    graph = []
    for clause in sat3:
        for var in clause:
            if not var[0] in all_vars:
                all_vars.append(var[0])

    all_ts = []
    for x in all_vars:
        t0 = 't_' + x + '_0'
        t1 = 't_' + x + '_1'
        all_ts.append(t0)
        all_ts.append(t1)
        graph.append((t0, t1))
        graph.append((t1, t0))

    i = 0
    for clause in sat3:
        vars_this_clause = []
        for var in clause:
            node = str(i) + '_' + var[0] + '_' + str(var[1])
            vars_this_clause.append(node)
            i += 1
        for var in vars_this_clause:
            for other in vars_this_clause:
                if var != other:
                    graph.append((var, other))
            var_parts = var.split('_')
            for t in all_ts:
                t_parts = t.split('_')
                if t_parts[1] == var_parts[1] and t_parts[2] == var_parts[2]:
                    graph.append((var, t))
                    graph.append((t, var))
    return graph, int((len(all_ts)/2)+len(sat3)*2)

def search(graph, k):
    all_v = []
    for edge in graph:
        if not edge[0] in all_v:
            all_v.append(edge[0])
        if not edge[1] in all_v:
            all_v.append(edge[1])

    all_vars = []
    for edge in graph:
        p1 = edge[0].split('_')[1]
        p2 = edge[1].split('_')[1]
        if not p1 in all_vars:
            all_vars.append(p1)
        if not p2 in all_vars:
            all_vars.append(p2)
    
    n_vertices = len(all_v)
    if k <= 0:
        return []
    assert(k > 0)

    for group in itertools.combinations(all_v, r=k):
        # Discard Groups with the following criteria:
        # x=0 and x=1
        value_conflict = False
        for x in group:
            if x.startswith('t_'):
                if x.endswith('_0'):
                    x_other = x[:len(x)-2] + '_1'
                else:
                    x_other = x[:len(x)-2] + '_0'
                if x_other in group:
                    value_conflict = True
        if value_conflict:
            continue

        # 0 or 1 t_vals
        t_vals = {}
        for x in group:
            if x.startswith('t_'):
                parts = x.split('_')
                t_vals[parts[1]] = parts[2]

        
        if len(t_vals) < len(all_vars):
            continue

        # 3 nodes from a single group
        mods = {}
        for x in group:
            if x.startswith('t_'):
                continue
            parts = x.split('_')
            clause = int(parts[0]) // 3
            if clause in mods:
                mods[clause] += 1
            else:
                mods[clause] = 1
        mods_fine = True
        for x in mods:
            if mods[x] > 2:
                mods_fine = False
        if not mods_fine:
            continue
        
        # the node not contained in the group must be true
        mod2 = {}
        for x in group:
            if x.startswith('t_'):
                continue
            parts = x.split('_')
            clause = int(parts[0]) // 3
            if not clause in mod2:
                mod2[clause] = []
            mod2[clause].append(int(parts[0]) % 3)
        is_other_true = True
        for clause in mod2:
            if 0 in mod2[clause] and 1 in mod2[clause]:
                missing = 2
            elif 0 in mod2[clause] and 2 in mod2[clause]:
                missing = 1
            elif 1 in mod2[clause] and 2 in mod2[clause]:
                missing = 0
            missing_no = clause*3+missing
            for x in all_v:
                if x.startswith(str(missing_no)+'_'):
                    t_rel = x.replace(str(missing_no)+'_','t_', 1)
                    if t_rel not in group:
                        is_other_true = False
        if not is_other_true:
            continue
                
        if iscover(graph, group) == True:
            return group

    return []

def formatify(soln):
    s_dict = {}
    for x in soln:
        if x.startswith('t_'):
            parts = x.split('_')
            s_dict[parts[1]] = int(parts[2])
    return s_dict

def special(sat3):
    s_dict = {}
    for x in sat3[0]:
        if not x[0] in s_dict:
            s_dict[x[0]] = x[1]
    return s_dict

def solve(sat3):
    #if len(sat3) == 1:
    #    return special(sat3)
    graph, k = reduce(sat3)
    soln = search(graph, k)
    return formatify(soln)

if __name__ == '__main__':
    fig745 = [
        [('x1',0),('x1',0),('x2',0)],
        [('x1',1),('x2',1),('x2',1)],
        [('x1',1),('x2',0),('x2',0)]
    ]

    sat_1 = [
        [('a',0),('b',0),('c',0)]
    ]

    sat_2= [
        [('a',1),('a',1),('a',1)]
    ]

    sat_3 = [
        [('a',0),('b',0),('c',0)],
        [('a',1),('b',1),('c',1)]
    ]



    print(solve(fig745))
    print(solve(sat_1))
    print(solve(sat_2))
    print(solve(sat_3))
