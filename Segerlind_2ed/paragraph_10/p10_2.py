import numpy as np

filename_mesh = 'p10_2.mesh'

num = 1835/(3000*5000-2000*1000/2)*200*200  # sink is shared by more than one vertices

materials = {
    'coef1': ({'val': 15},),
    'coef2': ({'val': 1500/num},),
}


def incline(coors, domain=None):
    shift=1
    
    X=coors[:,0]
    Y=coors[:,1]
    
    y = -1/2*X + 4500-shift
    
    return np.where(Y>y)[0]


functions = {
    'my_incline': (incline,),
}

regions = {
    'Omega' : 'all', 
    'Gamma_Left': ('vertices in (x < 0.00001)', 'facet'),
    'Gamma_Right': ('vertices in (x > 4999.99999)&(y<1999.1)', 'facet'),
    'Gamma_Down': ('vertices in (y < 0.00001)', 'facet'),
    'Gamma_Up': ('vertices in (y > 2999.99999)&(x<2999.1)', 'facet'),
    'Gamma_Inc': ('vertices by my_incline', 'facet'),
    # 'Sink': 'cell 20',
    'Sink': 'vertices in (y > 1400)&(y<1600)&(x>1900)&(x<2100)',
}

fields = {
    'piezohead': ('real', 1, 'Omega', 1)
}

variables = {
    't': ('unknown field', 'piezohead', 0),
    's': ('test field', 'piezohead', 't'),
}

ebcs = {
    't1': ('Gamma_Left', {'t.0': 200}),
    't2': ('Gamma_Right', {'t.0': 200}),
#     't3': ('Gamma_Up', {'t.0': 0}),
#     't4': ('Gamma_Down', {'t.0': 0}),
#     't5': ('Gamma_Inc', {'t.0': 0}),
}

integrals = {
    'i':  2,
}

equations = {
    'Temperature': """dw_laplace.i.Omega(coef1.val, s, t ) + 
    dw_volume_integrate.i.Sink(coef2.val, s) = 0""",
}

solvers = {
    'ls': ('ls.scipy_direct', {}),
    'newton': ('nls.newton',
               {'i_max': 1,
                'eps_a': 1e-6,
                'eps_r': 1.0,
                })
}

options = {
    'nls' : 'newton',
    'ls' : 'ls',
    'refinement_level' : 0,
}


# TODO - the answer is not the same as in the book