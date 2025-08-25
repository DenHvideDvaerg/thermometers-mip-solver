# Mathematical Model Documentation

This document provides a formal mathematical programming formulation of the Thermometers puzzle as a Mixed Integer Programming (MIP) problem.

## Problem Definition

Given:
- An **m × n** grid representing the puzzle board
- **Row mercury requirements** R = {r₁, r₂, ..., rₘ} where rᵢ is the required number of mercury-filled cells in row i
- **Column mercury requirements** C = {c₁, c₂, ..., cₙ} where cⱼ is the required number of mercury-filled cells in column j
- **Thermometer paths** T = {T₁, T₂, ..., Tₖ} where each Tᵢ is an ordered sequence of cell positions representing a thermometer

**Objective:** Find which cells to fill with mercury to satisfy all Thermometers puzzle rules.

## Sets and Indices

| Symbol | Definition |
|--------|------------|
| **I** | Set of row indices: I = {0, 1, ..., m-1} |
| **J** | Set of column indices: J = {0, 1, ..., n-1} |
| **T** | Set of thermometers: T = {T₁, T₂, ..., Tₖ} |
| **Tᵢ** | Ordered sequence of positions for thermometer i: Tᵢ = [(r₁,c₁), (r₂,c₂), ..., (rₗᵢ,cₗᵢ)] |

## Decision Variables

| Variable | Domain | Definition |
|----------|--------|------------|
| **x_{i,j}** | {0, 1} | 1 if cell (i,j) is filled with mercury, 0 otherwise |

## Objective Function

This is a constraint satisfaction problem where the goal is to find a feasible solution that satisfies all constraints without optimizing any particular objective. Therefore, we define the objective function as:

```
minimize 0
```

## Constraints

### 1. Row Sum Constraints
Each row must contain exactly the required number of mercury-filled cells:

```
Σⱼ x_{i,j} = rᵢ    ∀i ∈ I
```

### 2. Column Sum Constraints  
Each column must contain exactly the required number of mercury-filled cells:

```
Σᵢ x_{i,j} = cⱼ    ∀j ∈ J
```

### 3. Thermometer Continuity Constraints
For each thermometer, mercury must fill continuously from the bulb (first position). If position k+1 in the thermometer is filled, then position k must also be filled:

```
x_{rₖ₊₁,cₖ₊₁} ≤ x_{rₖ,cₖ}    ∀Tᵢ ∈ T, ∀k ∈ {1, 2, ..., |Tᵢ|-1}
```

Where (rₖ,cₖ) and (rₖ₊₁,cₖ₊₁) are consecutive positions in thermometer Tᵢ.

## Complete MIP Formulation

**Variables:**
```
x_{i,j} ∈ {0,1}    ∀i ∈ I, ∀j ∈ J
```

**Objective:**
```
minimize 0
```

**Subject to:**
```
Σⱼ x_{i,j} = rᵢ                                    ∀i ∈ I         (Row sums)

Σᵢ x_{i,j} = cⱼ                                    ∀j ∈ J         (Column sums)

x_{rₖ₊₁,cₖ₊₁} ≤ x_{rₖ,cₖ}                          ∀Tᵢ ∈ T, ∀k    (Thermometer continuity)

x_{i,j} ∈ {0,1}                                    ∀i ∈ I, ∀j ∈ J (Binary variables)
```

## Implementation Notes

- **Mathematical indexing**: This formulation uses 0-based indexing for consistency with Python implementation (rows 0 to m-1, columns 0 to n-1)
- **Thermometer representation**: Thermometers are defined using waypoints that automatically expand to complete paths
- **Constraint types**: The model uses only three essential constraint types for efficient solving
- **Solver backend**: Implemented using Google OR-Tools with SCIP optimizer by default
- **Complexity**: The model scales linearly with grid size and number of thermometers
