import Challenge
open SplitProperStarColouring
example : targetWitness (⟨4, [(0,1),(1,2),(2,3)]⟩,2) [0,1,0,1] = false := by native_decide
example : targetWitness (⟨4, [(0,1),(1,2),(2,3)]⟩,3) [0,1,0,2] = true := by native_decide
