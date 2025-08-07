import straindesign as sd
from gsm_bounds_from_mfa.make_rxn_expression import make_rxn_expression

# This function calculates the minimum and maximum flux values for a given set of reactions, 
# given a model and a constraint string. It does this by running FBA to maximize and minimize 
# the flux through the reaction based on the GSM reactions that are mapped to each of the MFA reactions.
def get_min_max_flux_expression_from_ids(model, reaction_ids, constraints):
    # Create constraint string from reaction IDs
    objective_string = make_rxn_expression(reaction_ids)

    # Calculate min and max values using FBA or another appropriate function
    sol_min = sd.fba(model, obj=objective_string, constraints=constraints, obj_sense='minimize')
    sol_max = sd.fba(model, obj=objective_string, constraints=constraints, obj_sense='maximize')

    # Check if solutions are optimal
    assert_optimal(sol_min, "minimization")
    assert_optimal(sol_max, "maximization")

    # Return the min and max values
    return sol_min.objective_value, sol_max.objective_value

def assert_optimal(solution, optimization_type):
    if solution.status == 'optimal':
        return
    else:
        raise RuntimeError(f'{optimization_type.capitalize()} did not find an optimal solution. The solution status is {solution.status}.')