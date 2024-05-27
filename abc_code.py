import random
import matplotlib.pyplot as plt  # Import matplotlib for plotting

# Define the dimensions and population size
dimensions = 4
population_size = 20
search_boundaries = [(-10, 10), (-100, 100), (-200, 200),(-500,500)]  # Different search boundaries to test

# Define the objective function (sphere function)
def sphere_function(vector):
    return sum(x ** 2 for x in vector)
# Employee Bee Phase
def employee_bee_phase(population, objective_func, trial_counts, phi = 0.3):
    for idx, bee_vector in enumerate(population):
        neighbor_vectors = population[:idx] + population[idx + 1:]  # Exclude current vector
        random_neighbor = random.choice(neighbor_vectors)
        
        modified_vector = []# modify every variable 
        for dim_idx, dim_value in enumerate(bee_vector):
            modified_value = dim_value + random.uniform(-1, 1) * (dim_value - random_neighbor[dim_idx])
            modified_vector.append(modified_value)
        
        if objective_func(bee_vector) < objective_func(modified_vector):
            trial_counts[idx] += 1
        else:
            population[idx] = modified_vector
            trial_counts[idx] = 0
    
    return population, trial_counts

# Onlooker Bee Phase
def onlooker_bee_phase(population, objective_func, trial_counts, phi = 0.3):
    probabilities = [1 / (1 + objective_func(bee_vector)) for bee_vector in population]
    total_prob = sum(probabilities)
    probabilities = [prob / total_prob for prob in probabilities]
    
    for idx, bee_vector in enumerate(population):
        if random.random() < probabilities[idx]:
            neighbor_vectors = population[:idx] + population[idx + 1:]  # Exclude current vector
            random_neighbor = random.choice(neighbor_vectors)
            
            modified_vector = []
            for dim_idx, dim_value in enumerate(bee_vector):
                modified_value = dim_value + random.uniform(-1, 1) * (dim_value - random_neighbor[dim_idx])
                modified_vector.append(modified_value)
            
            if objective_func(bee_vector) < objective_func(modified_vector):
                trial_counts[idx] += 1
            else:
                population[idx] = modified_vector
                trial_counts[idx] = 0
    
    return population, trial_counts

# Scout Bee Phase
def scout_bee_phase(population, trial_counts, search_bounds, limit=3):
    for idx, trials in enumerate(trial_counts):
        if trials > limit:
            trial_counts[idx] = 0
            population[idx] = [random.uniform(bounds[0], bounds[1]) for bounds in search_bounds]
    
    return population  
#Artificial Bee Colony algorithm
def artificial_bee_colony(dimensions, search_bounds, objective_func, limit=4, population_size=20, runs=100, tolerance=1e-6):
    convergence_data = []  # Store convergence data for each search bound

    for bounds in search_bounds:
        print(f"Running ABC for search bounds: {bounds}")
        best_solution = None
        best_fitness = float('inf')
        global_best_fitness = float('inf')  # Initialize global best fitness

        population = [[random.uniform(bound[0], bound[1]) for bound in [bounds] * dimensions] for _ in range(population_size)]
        trial_counts = [0 for _ in range(population_size)]

        iteration_numbers = []  # List to store iteration numbers
        fitness_values = []  # List to store best fitness values

        convergence_iteration = -1  # Store the iteration when convergence occurs

        for iteration in range(runs):
            population, trial_counts = employee_bee_phase(population, objective_func, trial_counts)
            population, trial_counts = onlooker_bee_phase(population, objective_func, trial_counts)
            population = scout_bee_phase(population, trial_counts, [bounds] * dimensions, limit)

            current_best_vector = min(population, key=objective_func)
            current_best_fitness = objective_func(current_best_vector)

            if current_best_fitness < best_fitness:
                best_solution = current_best_vector
                best_fitness = current_best_fitness

            iteration_numbers.append(iteration + 1)
            fitness_values.append(best_fitness)

            if best_fitness < global_best_fitness:
                global_best_fitness = best_fitness

            # Check for convergence
            if len(fitness_values) > 1 and abs(fitness_values[-1] - fitness_values[-2]) < tolerance:
                convergence_iteration = iteration + 1
                break  # Exit the loop if convergence is detected

        convergence_data.append((bounds, iteration_numbers, fitness_values, convergence_iteration))

    return convergence_data

# Run the ABC algorithm for different search bounds
convergence_data = artificial_bee_colony(dimensions, search_boundaries, sphere_function, limit=50, population_size=population_size, runs=100)

# Plotting the convergence data
plt.figure(figsize=(10, 6))
for data in convergence_data:
    plt.plot(data[1], data[2], label=f"Search Bounds: {data[0]}")

plt.xlabel('Iteration Number')
plt.ylabel('Best Fitness Value')
plt.title('Convergence Analysis of ABC with Different Search Bounds')
plt.legend()
plt.grid(True)
plt.show()

# Print the global minimum and convergence iteration of all search bounds
global_minimums = [min(data[2]) for data in convergence_data]
convergence_iterations = [data[3] for data in convergence_data]
print("Global Minimums for Different Search Bounds:", global_minimums)
print("Convergence Iterations for Different Search Bounds:", convergence_iterations)
