## Overview


## Workflow Routing

### `./CLAUDE.md`
Only the most important information is stored here, as it is always loaded in context. Directs to other files?


## Project Scoping

### `./project/DESIGN.md`
Contains big-picture ideas about the project goals and design principles
- Purpose and Scope
- Function Families
- Conventions
- Design Principles
	+ Guiding Principles numbered with GP prefix (GP1)
	+ Inviolable Principles numbered with IP prefix (IP1)


## Milestone Tracking

### `./project/milestones/ACTIVE.md`

### `./project/milestones/CANDIDATES.md`

### `./project/milestones/ARCHIVED.md`


## Decision Tracking

### `./project/DECISIONS.md`

## Review Materials

### `./project/reviews`


## Reference Materials

### `./project/references`


## Skills and User Workflow

### /milestone-plan

### /milestone-implement

### /milestone-review


## Model and Agent Strategy

For now, the baseline model should be Opus acting as orchestrator. It has explicit permission to spin up Opus and Sonnet subagents to complete (sub)tasks as needed; Haiku should never be used. The orchestrator is also encouraged to consider when a Review by Fable is needed to ensure accuracy/rigor. In such cases, it should request this of the user with a short rationale; if approved, it would then prepare a Review Brief document in .project/reviews numbered chronologically with the RB prefix (e.g., RB1.md) providing a mostly self-contained prompt for Fable. The user would then be alerted and given a chip to manually run this RB file in a new Fable session. The Fable session would be instructed in the brief to write its findings into a Review Report with the same number but the RR prefix (e.g., RR1.md)


## Priorities

1. The system should be efficient (it avoids redundant work but doesn't store unhelpful minutiae)
2. The system should be reliable (it doesn't become stale easily and self-corrects as it goes)
3. The system should be 
