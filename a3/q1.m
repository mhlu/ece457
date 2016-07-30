POPULATION_SIZE = 50;
GENERATIONS = 150;
CROSSOVER_PROB = 0.6;
MUTATION_PROB = 0.25;

% Initialize population
population = zeros(POPULATION_SIZE, 3);
for i = 1:POPULATION_SIZE
    Kp = 2 + rand()*(18 - 2);
    Ti = 1.05 + rand()*(9.42 - 1.05);
    Tp = 0.26 + rand()*(2.37 - 0.26);
    population(i, :) = [Kp Ti Tp];
end

% Best fitness vector for each generation
best = zeros(GENERATIONS, 1);

% Iterate over all generations
for generation = 1:GENERATIONS
    parents = zeros(POPULATION_SIZE, 3);
    offspring = zeros(POPULATION_SIZE, 3);

    % Select Parents using FPS with sum of measures as fitness function
    fitness_values = zeros(POPULATION_SIZE, 1);
    for i = 1:POPULATION_SIZE
        fitness_values(i) = -sum(perffcn(transpose(population(i,:))));
    end
    total_fitness = sum(fitness_values);
    shift_value = -min(fitness_values) + 1;
    FPS_weight = zeros(POPULATION_SIZE, 1);
    for i = 1:POPULATION_SIZE
        FPS_weight(i) = (fitness_values(i) + shift_value) / (total_fitness + POPULATION_SIZE*shift_value);
    end
    
    parents_ind = randsample(1:POPULATION_SIZE, POPULATION_SIZE, true, FPS_weight);
    for i = 1:POPULATION_SIZE
        parents(i,:) = population(parents_ind(i),:);
    end

    % Crossover Operator: Pick random gene and apply single arithmetic crossover
    alpha = 0.5;
    for i = 1:POPULATION_SIZE/2
        parent1 = parents(i*2-1,:);
        parent2 = parents(i*2,:);
        if rand() < CROSSOVER_PROB
            child1 = parent1;
            child2 = parent2;
            k = randi(3);
            child1(k) = alpha * parent1(k) + (1-alpha) * parent2(k);
            child2(k) = alpha * parent2(k) + (1-alpha) * parent1(k);
            offspring(i*2-1,:) = child1;
            offspring(i*2,:) = child2;
        else
            offspring(i*2-1,:) = parent1;
            offspring(i*2,:) = parent2;
        end
    end

    % Mutatate Offspring by selecting random gene and modify randomly within bounds
    for i = 1:POPULATION_SIZE
        if rand() < MUTATION_PROB
            offspring(i, 1) = 2 + rand()*(18 - 2);
        end
        if rand() < MUTATION_PROB
            offspring(i, 2) = 1.05 + rand()*(9.42 - 1.05);
        end
        if rand() < MUTATION_PROB
            offspring(i, 3) =  0.26 + rand()*(2.37 - 0.26);
        end
    end

    % Replace current generation with new population but retain best 2 individuals
    sorted = sort(fitness_values);
    elite1 = find(fitness_values == sorted(end), 1);
    elite2 = find(fitness_values == sorted(end-1), 1);
    offspring(elite1,:) = population(elite1,:);
    offspring(elite2,:) = population(elite2,:);
    population = offspring;

    % Keep track of best fitness value for this generation
    best(generation) = sorted(end);
end

plot(1:GENERATIONS, best)
