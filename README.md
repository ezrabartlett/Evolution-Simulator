# Evolution-Simulator
Curiosity project. The goal will be to generate complex behavior and patterns by defining a few very simple rules.

I'm pushing some messy files from my personal computer as part of my initiative to organize my projects.

Currently, a shape is generated randomly. Every generation, 10 children are created, each one mutated from the parent using random values. Larger mutations have a smaller chance of happening, based on the percent point function. The "most fit" child, based on the desired shape, is chosen to be the next parent. The current shape very quickly moves towards the desired shape.

planned features-

	Each "Creature" currently has a brain, consisting of a simple neural network, whose weights can mutate the same way the shape does. I'd like to add movement functionality to the shape, and reward it for finding food. Eventually, the shapes should perform complicated actions and movements, if Darwin is to be believed.
	

If you want to run this project, you need to have pip and python 3. 
  
	Clone the repository, then run "pip install -r requirements.txt"
  
	In the root directory, run "python EvolutionSimMain.py"
